#!/usr/bin/env python3
"""Workflow #4 — Sort search terms: "is this query from a buyer?"

Reads a Google Ads search-terms export (CSV), asks Jev one Noul question per
query, and splits rows into negatives / watch / keepers. Prints token usage so
real cost can be measured, not asserted.

Usage:
    python3 sort_search_terms.py input.csv \
        --context "Breeze: project-management SaaS for agencies, $12/user/mo" \
        [--out decisions.csv] [--negative-below 0.30] [--keep-above 0.60] [--chunk 25]
"""
import argparse
import csv
import sys

from typesafe import ask_batch

QUERY_COLUMNS = ["query", "search term", "search terms report", "search query", "term"]

def buyer_question(field):
    return {
        "type": "noul",
        "instructions": (
            f"Was the search query `{field}` typed by someone with commercial "
            "intent as a potential customer of the advertiser — someone who "
            "could realistically become a paying customer? Job seekers, "
            "students, people researching a concept, people looking for a "
            "different business with a similar name, and freebie hunters with "
            "no purchase path are NOT customers."
        ),
        "criteria": {
            "true": "Query shows customer/purchase intent for the advertiser's category",
            "false": "Query is informational, unrelated, a job/salary search, a name collision, or otherwise not a potential customer",
        },
    }


def find_query_column(fieldnames):
    for cand in QUERY_COLUMNS:
        for f in fieldnames:
            if f.strip().lower() == cand:
                return f
    return fieldnames[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--context", required=True, help="What the advertiser sells (goes to the model as state)")
    ap.add_argument("--out", default="decisions.csv")
    ap.add_argument("--negative-below", type=float, default=0.30)
    ap.add_argument("--keep-above", type=float, default=0.60)
    ap.add_argument("--chunk", type=int, default=25, help="Queries per API request")
    args = ap.parse_args()

    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        qcol = find_query_column(reader.fieldnames)
        rows = list(reader)
    print(f"Read {len(rows)} rows (query column: {qcol!r})")

    chunks = [rows[i : i + args.chunk] for i in range(0, len(rows), args.chunk)]
    jobs = []
    for chunk in chunks:
        state = {"advertiser": args.context}
        questions = {}
        for j, row in enumerate(chunk):
            state[f"q{j}"] = row[qcol].strip()
            questions[f"q{j}_buyer"] = buyer_question(f"q{j}")
        jobs.append((state, questions))

    print(f"Sending {len(jobs)} request(s), {args.chunk} questions each...")
    all_answers, usage = ask_batch(jobs)

    out_rows, counts = [], {"KEEP": 0, "WATCH": 0, "NEGATIVE": 0}
    for chunk, answers in zip(chunks, all_answers):
        for j, row in enumerate(chunk):
            p = answers[f"q{j}_buyer"]["noul"]
            verdict = "KEEP" if p >= args.keep_above else ("NEGATIVE" if p <= args.negative_below else "WATCH")
            counts[verdict] += 1
            out = dict(row)
            out["p_buyer"] = f"{p:.2f}"
            out["verdict"] = verdict
            out_rows.append(out)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    with open("negatives.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows([r for r in out_rows if r["verdict"] == "NEGATIVE"])

    total_in, total_out = usage["input_tokens"], usage["output_tokens"]
    print(f"\nVerdicts: {counts['KEEP']} keep / {counts['WATCH']} watch / {counts['NEGATIVE']} negative")
    print(f"Written: {args.out}, negatives.csv")
    print(f"Usage: {total_in} in / {total_out} out tokens for {len(rows)} queries")
    print(f"Rate: ~{(total_in + total_out) / len(rows):.0f} tokens/query "
          f"-> 50,000 queries ≈ ~{(total_in + total_out) / len(rows) * 50000:,} tokens")


if __name__ == "__main__":
    sys.exit(main())
