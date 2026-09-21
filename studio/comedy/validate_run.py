#!/usr/bin/env python3
"""Validate a Comedy Test Sprint run and its production-policy evidence."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PERSONAS = {"absurdist", "cynic", "worrier", "innocent", "status", "antimarketing"}
RATIONALES = {
    "specific_tension",
    "social_recognition",
    "strong_pattern_interrupt",
    "product_organic",
    "weak_generic",
    "unclear_mapping",
}
BANNED_PUBLIC_CLAIMS = (
    r"guaranteed\s+ROAS",
    r"production\s+performance\s+lift",
    r"whole[- ]library\s+(?:census|coverage)",
    r"\b30x\b",
    r"\b90%\s+(?:cost|performance)",
)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require(paths: list[Path]) -> list[str]:
    return [f"missing artifact: {path}" for path in paths if not path.is_file()]


def validate_selection(run: Path) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    expected_paths = [
        run / "brief.json",
        run / "premises.all.csv",
        run / "premises.filtered.csv",
        run / "premises.rejected.csv",
        run / "filter_report.json",
        run / "round1.json",
        run / "round1.scores.csv",
        run / "round1.survivors.csv",
        run / "mutation_report.json",
        run / "round1.mutated.csv",
        run / "round2.json",
        run / "round2.scores.csv",
        run / "round2.finalists.csv",
        run / "REPORT.md",
    ]
    errors.extend(require(expected_paths))
    if errors:
        return {}, errors

    premises = load_csv(run / "premises.all.csv")
    if len(premises) != 120:
        errors.append(f"premise count expected 120, found {len(premises)}")
    persona_counts = Counter(row.get("persona") for row in premises)
    if set(persona_counts) != PERSONAS or any(count != 20 for count in persona_counts.values()):
        errors.append(f"persona matrix expected six personas x 20, found {dict(persona_counts)}")
    if len({row["premise_id"] for row in premises}) != len(premises):
        errors.append("premise IDs are not unique")
    if len({row["text"].casefold().strip() for row in premises}) != len(premises):
        errors.append("premise texts are not unique")
    lengths = [len(row["text"]) for row in premises]
    if min(lengths) < 25 or max(lengths) > 240:
        errors.append(f"premise length out of bounds: {min(lengths)}..{max(lengths)}")
    if any(not row.get("product_tension", "").strip() for row in premises):
        errors.append("a premise is missing product tension")

    filter_report = load_json(run / "filter_report.json")
    if filter_report.get("input_count") != 120:
        errors.append("filter report input_count is not 120")
    if filter_report.get("ordering") != "filter precedes TypeSafe tournament":
        errors.append("filter ordering evidence is missing")
    filtered = load_csv(run / "premises.filtered.csv")
    if len(filtered) != filter_report.get("accepted_count"):
        errors.append("filtered premise count does not reconcile")

    for round_number, expected_in, expected_out, output_path in (
        (1, len(filtered), 24, "round1.survivors.csv"),
        (2, 24, 8, "round2.finalists.csv"),
    ):
        report_path = run / f"round{round_number}.json"
        scores_path = run / f"round{round_number}.scores.csv"
        report = load_json(report_path)
        scores = load_csv(scores_path)
        if report.get("model") != "jev-latest":
            errors.append(f"round {round_number} did not record jev-latest")
        if report.get("input_count") != expected_in:
            errors.append(f"round {round_number} input_count expected {expected_in}, found {report.get('input_count')}")
        if report.get("survivor_count") != expected_out:
            errors.append(f"round {round_number} survivor_count expected {expected_out}, found {report.get('survivor_count')}")
        if not isinstance(report.get("input_tokens"), int) or report.get("input_tokens", -1) < 0:
            errors.append(f"round {round_number} input token usage missing")
        if not isinstance(report.get("output_tokens"), int) or report.get("output_tokens", -1) < 0:
            errors.append(f"round {round_number} output token usage missing")
        if len(scores) != expected_in:
            errors.append(f"round {round_number} scores rows expected {expected_in}, found {len(scores)}")
        selected = [row for row in scores if row.get("selected") == "true"]
        if len(selected) != expected_out:
            errors.append(f"round {round_number} selected rows expected {expected_out}, found {len(selected)}")
        if any(row.get("rationale_code") not in RATIONALES for row in scores):
            errors.append(f"round {round_number} has an unknown rationale code")
        if any(not row.get("rationale", "").strip() for row in scores):
            errors.append(f"round {round_number} has a missing rationale")
        survivors = load_csv(run / output_path)
        if len(survivors) != expected_out:
            errors.append(f"{output_path} row count expected {expected_out}, found {len(survivors)}")

    mutated = load_csv(run / "round1.mutated.csv")
    survivors1 = load_csv(run / "round1.survivors.csv")
    survivor_ids = {row["premise_id"] for row in survivors1}
    if len(mutated) != 24:
        errors.append(f"mutated rows expected 24, found {len(mutated)}")
    if any(row.get("mutated_from") not in survivor_ids for row in mutated):
        errors.append("mutation row does not trace to a first-round survivor")
    if any(row["persona"] not in PERSONAS for row in mutated):
        errors.append("mutation has an invalid persona")
    if any(not re.search(r"\b(earbuds?|audio|calls?|sound|wire|listen|voice)\b", row["text"], re.I) for row in mutated):
        errors.append("mutation lost product link")

    report = (run / "REPORT.md").read_text(encoding="utf-8")
    for pattern in BANNED_PUBLIC_CLAIMS:
        for line in report.splitlines():
            if re.search(pattern, line, re.I) and not any(token in line.casefold() for token in ("no ", "not ", "never")):
                errors.append(f"unsupported report claim: {line}")
    return {"premises": len(premises), "personas": dict(persona_counts)}, errors


def validate_production(run: Path) -> list[str]:
    errors: list[str] = []
    board_path = run / "boards" / "manifest.json"
    render_path = run / "render" / "manifest.json"
    qa_path = run / "render" / "qa-summary.json"
    errors.extend(require([board_path, render_path, qa_path]))
    if errors:
        return errors

    board_manifest = load_json(board_path)
    boards = board_manifest.get("boards", [])
    if len(boards) != 8:
        errors.append(f"board count expected 8, found {len(boards)}")
    for board in boards:
        if board.get("model") != "gpt-image-2.5-sunburst":
            errors.append(f"non-free board model: {board.get('model')}")
        if board.get("quality") != "1440p" or board.get("aspect_ratio") != "9:16":
            errors.append(f"invalid board parameters: {board}")
        if not (run / board.get("prompt_path", "missing")).is_file():
            errors.append(f"missing board prompt: {board.get('prompt_path')}")
        local = board.get("local_path")
        if local and not Path(local).is_file():
            errors.append(f"missing board image: {local}")

    render_manifest = load_json(render_path)
    videos = render_manifest.get("videos", [])
    if len(videos) > 2:
        errors.append(f"V6 video cap exceeded: {len(videos)}")
    for video in videos:
        if video.get("model") != "v6":
            errors.append(f"non-V6 video model: {video.get('model')}")
        if video.get("quality") != "720p":
            errors.append(f"non-720p video: {video}")
        if video.get("duration") != "5":
            errors.append(f"non-five-second video: {video}")
        if video.get("audio") != "disabled":
            errors.append(f"audio not disabled: {video}")
        if not Path(video.get("local_path", "missing")).is_file():
            errors.append(f"missing video: {video.get('local_path')}")
    if any(video.get("model") not in {"v6"} for video in videos):
        errors.append("premium video route found")
    if not videos:
        errors.append("no V6 video rendered")

    qa = load_json(qa_path)
    if qa.get("technical_pass_count", 0) < 1:
        errors.append("no V6 video passed technical QA")
    if qa.get("human_review_count", 0) < 1:
        errors.append("no V6 video received human review")
    if qa.get("premium_models_found", False):
        errors.append("QA summary reports a premium model")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    parser.add_argument("--full", action="store_true", help="Also validate boards, V6 renders, and QA.")
    args = parser.parse_args()
    run = args.run.resolve()
    selection, errors = validate_selection(run)
    if args.full:
        errors.extend(validate_production(run))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": "PASS",
                "mode": "full" if args.full else "selection",
                **selection,
                "policy": "free boards + at most two V6 videos",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
