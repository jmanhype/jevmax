#!/usr/bin/env python3
"""Workflow #3 — Score briefs before you shoot.

Reads ad briefs (CSV with a brief/text column), scores each on hook strength,
brand fit, and survival odds, ranks them. Only the top ones deserve production.

Usage:
    python3 score_briefs.py briefs.csv --brand "Breeze: PM SaaS for agencies, no-nonsense tone" \
        [--out ranked_briefs.csv]
"""
import argparse
import csv
import sys

from typesafe import ask_batch

BRAND_COLUMNS = ["brief", "text", "concept", "description", "idea"]


def find_col(fieldnames):
    for cand in BRAND_COLUMNS:
        for f in fieldnames:
            if f.strip().lower() == cand:
                return f
    return fieldnames[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--brand", required=True, help="Brand/offer/tone context")
    ap.add_argument("--out", default="ranked_briefs.csv")
    args = ap.parse_args()

    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        col = find_col(reader.fieldnames)
        rows = list(reader)

    state = {"brand": args.brand}
    questions = {}
    for i, row in enumerate(rows):
        state[f"b{i}"] = row[col].strip()
        questions[f"b{i}_hook"] = {
            "type": "score",
            "instructions": f"How strong is the opening hook of brief `b{i}` for paid social — would it stop a scrolling buyer?",
            "criteria": [
                "Ignorable: generic opener, no tension, no promise",
                "Weak: mild interest, easily scrolled past",
                "Decent: clear promise but familiar pattern",
                "Strong: specific tension or contrarian claim, demands resolution",
                "Exceptional: pattern-interrupt, instantly legible to the target buyer",
            ],
        }
        questions[f"b{i}_fit"] = {
            "type": "noul",
            "instructions": f"Does brief `b{i}` fit the brand — its offer, audience, and tone?",
            "criteria": {
                "true": "Could plausibly ship as this brand's ad without repositioning",
                "false": "Wrong audience, wrong promise, off-tone, or overclaims",
            },
        }
        questions[f"b{i}_survive"] = {
            "type": "score",
            "instructions": f"How likely is brief `b{i}` to still be running as a live ad after 60 days — i.e., to survive contact with real spend?",
            "criteria": [
                "Likely dead in days: gimmick, fatigue-prone, or claims that burn out",
                "Short runway: one angle, quick saturation",
                "Moderate: solid core idea with limited variants",
                "Durable: evergreen angle with natural variant space",
                "Built to last: compounding angle, endlessly refreshable",
            ],
        }

    print(f"Scoring {len(rows)} brief(s)...")
    all_answers, usage = ask_batch([(state, questions)])

    out_rows = []
    for i, row in enumerate(rows):
        a = all_answers[0]
        out = dict(row)
        out["hook"] = f"{a[f'b{i}_hook']['score']:.2f}"
        out["brand_fit"] = f"{a[f'b{i}_fit']['noul']:.2f}"
        out["survival"] = f"{a[f'b{i}_survive']['score']:.2f}"
        out["total"] = f"{a[f'b{i}_hook']['score'] + a[f'b{i}_survive']['score'] + 5 * a[f'b{i}_fit']['noul']:.2f}"
        out_rows.append(out)

    out_rows.sort(key=lambda r: float(r["total"]), reverse=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    for r in out_rows:
        print(f"  total {r['total']:>5}  hook {r['hook']}  fit {r['brand_fit']}  survive {r['survival']}  | {r[col][:70]}")
    print(f"Usage: {usage['input_tokens']} in / {usage['output_tokens']} out tokens")


if __name__ == "__main__":
    sys.exit(main())
