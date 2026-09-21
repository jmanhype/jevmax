#!/usr/bin/env python3
"""Regression benchmark for the local Jevmax workflows.

This is deliberately offline: it evaluates already-recorded demo outputs against
semantic expected labels. It does **not** claim blind predictive accuracy and it
does not call TypeSafe or Meta.

Usage:
  python3 benchmark.py [--json benchmark_results.json] [--md benchmark_report.md]
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def confusion(actual: list[str], expected: list[str]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for a, e in zip(actual, expected):
        out[e][a] += 1
    return {e: dict(vals) for e, vals in out.items()}


def search_terms() -> dict:
    actual_rows = read_csv(ROOT / "decisions.csv")
    expected_rows = read_csv(ROOT / "benchmarks/expected_search_terms.csv")
    expected = {r["query"]: r["expected_verdict"] for r in expected_rows}
    matched, missing = [], []
    for row in actual_rows:
        if row["query"] not in expected:
            missing.append(row["query"])
        else:
            matched.append((row, expected[row["query"]]))
    correct = [r for r, e in matched if r["verdict"] == e]
    errors = [
        {"query": r["query"], "expected": e, "actual": r["verdict"], "p_buyer": r["p_buyer"]}
        for r, e in matched
        if r["verdict"] != e
    ]
    probabilities = {
        verdict: [float(r["p_buyer"]) for r, _ in matched if r["verdict"] == verdict]
        for verdict in ("KEEP", "WATCH", "NEGATIVE")
    }
    return {
        "name": "Workflow #4 — buyer-intent search-term sorting",
        "n": len(matched),
        "pass": len(correct),
        "accuracy": len(correct) / len(matched) if matched else 0,
        "confusion": confusion([r["verdict"] for r, _ in matched], [e for _, e in matched]),
        "mean_p_buyer": {k: (sum(v) / len(v) if v else None) for k, v in probabilities.items()},
        "errors": errors,
        "unlabeled_actual_rows": missing,
    }


def page_match() -> dict:
    data = json.loads((ROOT / "match.json").read_text())
    passed = (
        data.get("delivers_promise") <= 0.20
        and data.get("match_score_0_4", 99) <= 1.50
        and data.get("biggest_gap") == "offer_mismatch"
        and data.get("match_confidence", 0) >= 0.70
    )
    return {
        "name": "Workflow #6 — ad/page promise match",
        "n": 1,
        "pass": int(passed),
        "accuracy": float(passed),
        "checks": {
            "delivers_promise_at_most_0_20": data.get("delivers_promise") <= 0.20,
            "match_score_at_most_1_50": data.get("match_score_0_4", 99) <= 1.50,
            "gap_is_offer_mismatch": data.get("biggest_gap") == "offer_mismatch",
            "confidence_at_least_0_70": data.get("match_confidence", 0) >= 0.70,
        },
        "error": None if passed else "Engineered offer mismatch was not identified strongly enough",
    }


def fatigue() -> dict:
    rows = read_csv(ROOT / "fatigue_decisions.csv")
    expected_calls = {"1001": "refresh", "1002": "leave", "1003": "refresh", "1005": "review", "1007": "refresh"}
    correct = []
    errors = []
    for row in rows:
        expected = expected_calls.get(row["ad_id"])
        actual = row["band"].lower() if row["ad_id"] == "1005" else row["call"]
        ok = actual == expected
        if ok:
            correct.append(row["ad_id"])
        else:
            errors.append({"ad_id": row["ad_id"], "expected": expected, "actual": actual})
    review_rows = [r for r in rows if float(r["confidence"]) < 0.50]
    return {
        "name": "Workflow #5 — creative fatigue decision bands",
        "n": len(rows),
        "pass": len(correct),
        "accuracy": len(correct) / len(rows) if rows else 0,
        "human_review_count": len(review_rows),
        "errors": errors,
    }


def leads() -> dict:
    rows = read_csv(ROOT / "scored_leads.csv")
    expected_ranges = {
        "Northwind Digital": (85, 100),
        "BrightPath Consulting": (75, 92),
        "Jake R.": (0, 25),
    }
    correct, errors = [], []
    for row in rows:
        low, high = expected_ranges[row["company"]]
        score = int(row["lead_score_0_100"])
        if low <= score <= high:
            correct.append(row["company"])
        else:
            errors.append({"company": row["company"], "expected_range": [low, high], "actual": score})
    return {
        "name": "Workflow #7 — lead quality scoring",
        "n": len(rows),
        "pass": len(correct),
        "accuracy": len(correct) / len(rows) if rows else 0,
        "errors": errors,
    }


def briefs() -> dict:
    rows = read_csv(ROOT / "ranked_briefs.csv")
    if not rows:
        return {"name": "Workflow #3 — brief scoring", "n": 0, "pass": 0, "accuracy": 0, "error": "no rows"}
    concrete = max(rows, key=lambda r: float(r["total"]))
    hype = next(r for r in rows if "AI" in r["brief"] and "synerg" in r["brief"])
    passed = concrete["brief"].startswith("Your agency") and float(hype["total"]) < 3.0
    return {
        "name": "Workflow #3 — brief scoring",
        "n": 1,
        "pass": int(passed),
        "accuracy": float(passed),
        "top_brief_total": float(concrete["total"]),
        "vague_brief_total": float(hype["total"]),
        "error": None if passed else "Concrete brief did not dominate vague AI-hype brief",
    }


def survival_selftest() -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "survival.py"), "selftest"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return {
        "name": "Workflow #2 — survival boundary selftest",
        "n": 1,
        "pass": int(proc.returncode == 0),
        "accuracy": float(proc.returncode == 0),
        "stdout": proc.stdout.strip(),
        "error": None if proc.returncode == 0 else proc.stderr.strip(),
    }


def recorded_usage() -> dict:
    manifest = json.loads((ROOT / "benchmarks/usage_manifest.json").read_text())
    out = {}
    for name, row in manifest["recorded_runs"].items():
        total = row["input_tokens"] + row["output_tokens"]
        out[name] = {
            **row,
            "total_tokens": total,
            "tokens_per_item": round(total / row["items"], 2),
        }
    return out


def build_results() -> dict:
    suites = [search_terms(), page_match(), fatigue(), leads(), briefs(), survival_selftest()]
    total_n = sum(x["n"] for x in suites)
    total_pass = sum(x["pass"] for x in suites)
    return {
        "benchmark_version": "0.1.0",
        "mode": "offline regression against recorded demo outputs",
        "all_passed": all(x["accuracy"] == 1.0 for x in suites),
        "total_cases": total_n,
        "total_passed": total_pass,
        "aggregate_pass_rate": total_pass / total_n if total_n else 0,
        "suites": suites,
        "recorded_usage": recorded_usage(),
        "limits": [
            "This is not a blind holdout; expected labels document the intended semantics of the demo fixtures.",
            "No TypeSafe API calls are made by benchmark.py.",
            "30x, 90%, and whole-library claims are intentionally absent because they are not measured here.",
        ],
    }


def markdown(results: dict) -> str:
    lines = [
        "# Jevmax offline regression benchmark",
        "",
        f"- Mode: {results['mode']}",
        f"- Cases: {results['total_passed']} / {results['total_cases']} passed",
        f"- Aggregate pass rate: {results['aggregate_pass_rate']:.0%}",
        f"- Overall: {'PASS' if results['all_passed'] else 'FAIL'}",
        "",
        "| Workflow | Cases | Passed | Pass rate |",
        "|---|---:|---:|---:|",
    ]
    for suite in results["suites"]:
        lines.append(f"| {suite['name']} | {suite['n']} | {suite['pass']} | {suite['accuracy']:.0%} |")
    lines += ["", "## Measured recorded usage", "", "| Run | Items | Tokens/item |", "|---|---:|---:|"]
    for name, row in results["recorded_usage"].items():
        lines.append(f"| {name} | {row['items']} | {row['tokens_per_item']:.0f} |")
    lines += ["", "## Limitations", ""]
    lines += [f"- {x}" for x in results["limits"]]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="benchmark_results.json")
    ap.add_argument("--md", default="benchmark_report.md")
    ap.add_argument("--min-pass-rate", type=float, default=0.99)
    args = ap.parse_args()
    results = build_results()
    (ROOT / args.json).write_text(json.dumps(results, indent=2) + "\n")
    (ROOT / args.md).write_text(markdown(results))
    print(markdown(results))
    return 0 if results["aggregate_pass_rate"] >= args.min_pass_rate else 1


if __name__ == "__main__":
    raise SystemExit(main())
