#!/usr/bin/env python3
"""Workflow #7 — Score every lead.

Rates each form fill 0–100 against your ideal customer profile, so the good
ones get fast follow-up and conversion value can flow back to Google/Meta
(offline conversions / value-based bidding).

Usage:
    python3 score_leads.py leads.csv --icp "YOUR ICP DESCRIPTION" [--out scored_leads.csv]
"""
import argparse
import csv
import sys

from typesafe import ask_batch

ICP_LEVELS = [
    "0–10: spam, bot, or competitor recon",
    "11–20: student or job seeker, no buying capacity",
    "21–30: wrong segment entirely",
    "31–40: tangentially related, no budget authority signals",
    "41–50: plausible but vague; needs heavy qualification",
    "51–60: fits segment loosely; timing or size unclear",
    "61–70: real fit with most ICP markers present",
    "71–80: strong fit, clear need, plausible timeline",
    "81–90: near-perfect ICP match, actionable urgency",
    "91–100: textbook ideal customer, reach out today",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--icp", required=True, help="Ideal customer profile description")
    ap.add_argument("--out", default="scored_leads.csv")
    args = ap.parse_args()

    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    lead_fields = [c for c in rows[0].keys() if c.strip()]

    state = {"icp": args.icp}
    questions = {}
    for i, row in enumerate(rows):
        state[f"l{i}"] = {c: row[c] for c in lead_fields}
        questions[f"l{i}_quality"] = {
            "type": "score",
            "instructions": f"Rate lead `l{i}` against the ideal customer profile: how good a potential customer is this form fill?",
            "criteria": ICP_LEVELS,
        }

    print(f"Scoring {len(rows)} lead(s)...")
    all_answers, usage = ask_batch([(state, questions)])

    out_rows = []
    for i, row in enumerate(rows):
        a = all_answers[0][f"l{i}_quality"]
        out = dict(row)
        out["lead_score_0_100"] = round(a["score"] * 100 / 9)  # weighted position on 0-9 levels -> 0-100
        out["confidence"] = f"{a.get('confidence', '')}"
        out_rows.append(out)

    out_rows.sort(key=lambda r: r["lead_score_0_100"], reverse=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    for r in out_rows:
        print(f"  {r['lead_score_0_100']:>3}  (conf {r['confidence']})  {[v for v in r.values()][0]}")
    print(f"Usage: {usage['input_tokens']} in / {usage['output_tokens']} out tokens")


if __name__ == "__main__":
    sys.exit(main())
