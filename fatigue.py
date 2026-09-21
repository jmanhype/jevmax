#!/usr/bin/env python3
"""Workflow #5 — Catch fatigue early.

Code owns the arithmetic: it flags ads where frequency went UP and CTR went DOWN.
Jev owns the judgment: for each flagged ad it picks replace / refresh / leave.

Per the TypeSafe skill + Confidence docs:
- All flagged ads go in ONE request (independent questions over one state).
- Calls are banded by risk: confidence >= --act-above -> act on the call;
  below that -> REVIEW (a human decides). Pausing/replacing live ads is a
  medium-stakes, recoverable action, so the default bar is 0.5.

Usage:
    python3 fatigue.py ads.csv [--out fatigue_decisions.csv] [--act-above 0.5]

Expected CSV columns: ad_id, name (optional), frequency_delta, ctr_delta
"""
import argparse
import csv
import sys

from typesafe import ask


def question(field):
    return {
        "type": "choice",
        "instructions": f"For the flagged ad `{field}`, choose the right call.",
        "criteria": {
            "leave": "Numbers moved but not enough to act; still learning or within noise",
            "refresh": "Concept still works but this execution is worn out — new creative, same angle",
            "replace": "The angle itself is exhausted — new concept needed",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--out", default="fatigue_decisions.csv")
    ap.add_argument("--act-above", type=float, default=0.5,
                    help="Confidence at or above which the call is acted on; below -> REVIEW")
    args = ap.parse_args()

    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    # Code does the filtering; the model never sees unflagged ads.
    flagged = [r for r in rows if float(r["frequency_delta"]) > 0 and float(r["ctr_delta"]) < 0]
    print(f"{len(flagged)} of {len(rows)} ads flagged (frequency up + CTR down)")
    if not flagged:
        print("Nothing to judge.")
        return

    # One request: all ads in one state, one question per ad, all independent.
    state, questions = {}, {}
    for i, r in enumerate(flagged):
        field = f"ad_{i}"
        state[field] = {
            "id": r["ad_id"],
            "name": r.get("name", ""),
            "frequency_change": r["frequency_delta"],
            "ctr_change_pp": r["ctr_delta"],
        }
        questions[f"{field}_call"] = question(field)

    answers, usage = ask(state, questions)

    out_rows = []
    for i, r in enumerate(flagged):
        a = answers[f"ad_{i}_call"]
        call, conf = a["choice"], a.get("confidence", 0.0)
        band = "ACT" if conf >= args.act_above else "REVIEW"
        out = dict(r)
        out["call"] = call
        out["confidence"] = f"{conf}"
        out["band"] = band
        out_rows.append(out)
        print(f"  {r['ad_id']:>12}  {call:<8} conf {conf:.2f}  -> {band}")

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    print(f"Written: {args.out}")
    print(f"Usage: {usage['input_tokens']} in / {usage['output_tokens']} out tokens "
          f"in 1 request ({len(rows) - len(flagged)} healthy ads cost zero tokens)")


if __name__ == "__main__":
    sys.exit(main())
