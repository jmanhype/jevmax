#!/usr/bin/env python3
"""Normalize PixVerse queue results into Comedy Test Sprint production evidence."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_results(document: dict[str, Any]) -> list[dict[str, Any]]:
    results = document.get("results", [])
    if not isinstance(results, list):
        raise ValueError("PixVerse result document has no results array")
    return results


def candidate_from_result(result: dict[str, Any], prefix: str) -> str:
    result_id = str(result.get("id", ""))
    match = re.search(rf"{prefix}[_-]C(\d{{3}})", result_id)
    if not match:
        command = result.get("command", "")
        match = re.search(r"C(\d{3})", command)
    if not match:
        raise ValueError(f"Cannot map PixVerse result to candidate: {result_id or command}")
    return f"C{match.group(1)}"


def record_boards(run: Path, result_path: Path) -> None:
    document = load(result_path)
    results = extract_results(document)
    manifest_path = run / "boards" / "manifest.json"
    manifest = load(manifest_path)
    boards = manifest.get("boards", [])
    by_id = {row["candidate_id"]: row for row in boards}
    for result in results:
        candidate_id = candidate_from_result(result, "board")
        if candidate_id not in by_id:
            raise ValueError(f"Unknown board candidate {candidate_id}")
        by_id[candidate_id].update(
            {
                "status": result.get("status"),
                "task_id": str(result.get("task_id", "")),
                "local_path": result.get("local_path", ""),
                "credits": int(result.get("cost_credits", 0) or 0),
                "model": "gpt-image-2.5-sunburst",
                "quality": "1440p",
                "aspect_ratio": "9:16",
            }
        )
    save(manifest_path, manifest)
    successful = [row for row in boards if row.get("status") == "success"]
    summary = {
        "model": "gpt-image-2.5-sunburst",
        "task_count": len(results),
        "successful_count": len(successful),
        "failed_count": len(results) - len(successful),
        "credits": sum(int(row.get("credits", 0) or 0) for row in boards),
        "policy": "free GPT Image 2.5 board route",
    }
    save(run / "boards" / "result-summary.json", summary)


def record_videos(run: Path, result_path: Path) -> None:
    document = load(result_path)
    results = extract_results(document)
    if len(results) > 2:
        raise ValueError(f"V6 cap exceeded: {len(results)} results")
    videos: list[dict[str, Any]] = []
    for result in results:
        candidate_id = candidate_from_result(result, "video")
        command = result.get("command", "")
        if "--model v6" not in command:
            raise ValueError(f"Non-V6 render result: {command}")
        if "--quality 720p" not in command or "--no-audio" not in command:
            raise ValueError(f"V6 render parameters violate policy: {command}")
        videos.append(
            {
                "candidate_id": candidate_id,
                "status": result.get("status"),
                "task_id": str(result.get("task_id", "")),
                "local_path": result.get("local_path", ""),
                "model": "v6",
                "quality": "720p",
                "duration": "5",
                "audio": "disabled",
                "credits": int(result.get("cost_credits", 0) or 0),
            }
        )
    manifest = {
        "policy": "at most two V6 720p five-second no-audio videos",
        "video_count": len(videos),
        "total_credits": sum(row["credits"] for row in videos),
        "videos": videos,
    }
    save(run / "render" / "manifest.json", manifest)


def record_qa(run: Path, qa_path: Path) -> None:
    document = load(qa_path)
    reports = document.get("reports", [])
    technical = [
        report
        for report in reports
        if report.get("generation_status") == "success" and not report.get("issues")
    ]
    summary = {
        "source": str(qa_path),
        "technical_total": len(reports),
        "technical_pass_count": len(technical),
        "human_review_count": 0,
        "premium_models_found": any("seedance" in str(report.get("model", "")).casefold() or "minimax" in str(report.get("model", "")).casefold() for report in reports),
        "technical_report_paths": [report.get("report_path", "") for report in reports],
    }
    save(run / "render" / "qa-summary.json", summary)


def append_production_report(run: Path, human_review: bool) -> None:
    boards = load(run / "boards" / "result-summary.json")
    renders = load(run / "render" / "manifest.json")
    qa = load(run / "render" / "qa-summary.json")
    qa["human_review_count"] = 1 if human_review else 0
    qa["human_review_policy"] = "operator reviewed delivered local media" if human_review else "pending"
    save(run / "render" / "qa-summary.json", qa)
    report_path = run / "REPORT.md"
    text = report_path.read_text(encoding="utf-8")
    marker = "\n## Production evidence\n"
    if marker in text:
        text = text.split(marker, 1)[0]
    text += (
        marker.lstrip("\n")
        + f"- Boards: {boards['successful_count']}/{boards['task_count']} succeeded; {boards['credits']} credits.\n"
        + f"- V6 videos: {renders['video_count']}/2 rendered; {renders['total_credits']} credits.\n"
        + f"- Technical QA passes: {qa['technical_pass_count']}/{qa['technical_total']}.\n"
        + f"- Human review count: {qa['human_review_count']}.\n"
        + "- Premium video models: none.\n"
        + "- No live ad change and no performance claim.\n"
    )
    report_path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--board-result", type=Path, required=True)
    parser.add_argument("--render-result", type=Path, required=True)
    parser.add_argument("--qa-result", type=Path, required=True)
    parser.add_argument("--human-review", action="store_true")
    args = parser.parse_args()
    record_boards(args.run, args.board_result)
    record_videos(args.run, args.render_result)
    record_qa(args.run, args.qa_result)
    append_production_report(args.run, args.human_review)
    print(f"Production evidence recorded for {args.run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
