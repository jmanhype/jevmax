#!/usr/bin/env python3
"""Workflows #1 + #2 — Scan the Meta Ad Library, find the patterns that survive.

#1: tags every live ad by hook type and offer type (Jev judgments).
#2: survival analysis — ads still live after 60+ days, grouped by tag, so you
    know what lasts before you test it.

Input: ad_library_raw.json (records scraped from the public Ad Library —
anonymous browser session; for scheduled/full runs use Meta's Ads MCP Server).

Usage: python3 ad_library_scan.py [--raw ad_library_raw.json] [--out ad_library_tagged.csv]
"""
import argparse
import csv
import json
from datetime import datetime

from typesafe import ask_batch

TODAY = datetime.now()

HOOK_QUESTION = {
    "type": "choice",
    "instructions": "What is the primary hook type of this ad copy?",
    "criteria": {
        "pain_question": "Opens on the buyer's pain, often as a question (\"Struggling to...?\")",
        "proof_stats": "Leads with numbers, rankings, results, or named social proof",
        "feature_list": "Enumeration of features/capabilities with checkmarks or lists",
        "founder_story": "First-person narrative or relatable founder/owner story",
        "curiosity_claim": "Curiosity gap or bold claim (\"stupid simple system for $15k\")",
        "direct_offer": "Straight product/offer statement with no real hook",
    },
}

OFFER_QUESTION = {
    "type": "choice",
    "instructions": "What is the primary offer of this ad?",
    "criteria": {
        "demo_or_trial": "Book a demo, free trial, get started free",
        "content_download": "Download a guide/report/ROI material (lead magnet)",
        "saas_subscription": "Buy/subscribe to software, implicit",
        "education_degree": "University program, course, certification",
        "recruiting": "Job posting or hiring",
        "other_product": "Physical product or non-SaaS offer",
    },
}


def days_since(date_str):
    return (TODAY - datetime.strptime(date_str, "%b %d, %Y")).days


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="ad_library_raw.json")
    ap.add_argument("--out", default="ad_library_tagged.csv")
    args = ap.parse_args()

    with open(args.raw, encoding="utf-8") as f:
        ads = json.load(f)
    for a in ads:
        a["days_running"] = days_since(a["started"])

    with_copy = [a for a in ads if a.get("copy")]
    print(f"{len(ads)} ads scraped, {len(with_copy)} with taggable copy")

    # --- Workflow #1: tag by hook and offer (batched, one question set per ad)
    jobs = []
    for chunk_start in range(0, len(with_copy), 20):
        chunk = with_copy[chunk_start : chunk_start + 20]
        state, questions = {}, {}
        for i, a in enumerate(chunk):
            state[f"a{i}"] = a["copy"]
            questions[f"a{i}_hook"] = {"type": "choice", "instructions": f"What is the primary hook type of ad copy `a{i}`?", "criteria": HOOK_QUESTION["criteria"]}
            questions[f"a{i}_offer"] = {"type": "choice", "instructions": f"What is the primary offer of ad copy `a{i}`?", "criteria": OFFER_QUESTION["criteria"]}
        jobs.append((state, questions))

    all_answers, usage = ask_batch(jobs)

    for idx, a in enumerate(with_copy):
        answers = all_answers[idx // 20]
        i = idx % 20
        a["hook"] = answers[f"a{i}_hook"]["choice"]
        a["offer"] = answers[f"a{i}_offer"]["choice"]

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "advertiser", "started", "days_running", "hook", "offer", "copy", "domain", "cta"])
        w.writeheader()
        w.writerows([{k: a.get(k) for k in w.fieldnames} for a in ads])
    print(f"Written: {args.out}")
    print(f"Usage: {usage['input_tokens']} in / {usage['output_tokens']} out tokens "
          f"for {len(with_copy)} tagged ads ({len(jobs)} requests)")

    # --- Workflow #2: survival analysis
    def table(group_key):
        groups = {}
        for a in ads:
            key = a.get(group_key) or "(untagged)"
            groups.setdefault(key, []).append(a["days_running"] >= 60)
        rows = []
        for key, flags in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            rows.append((key, len(flags), sum(flags) / len(flags)))
        return rows

    survivors = [a for a in ads if a["days_running"] >= 60]
    print(f"\n=== SURVIVAL: {len(survivors)}/{len(ads)} ads live after 60+ days "
          f"({len(survivors)/len(ads):.0%}) ===")
    for label, key in (("BY HOOK", "hook"), ("BY OFFER", "offer")):
        print(f"\n{label} (n, % live 60d+):")
        for key_name, n, pct in table(key):
            print(f"  {key_name:<16} n={n:<3} {pct:.0%}")

    print("\nMarathon ads (180+ days live):")
    for a in sorted(ads, key=lambda x: -x["days_running"])[:8]:
        tag = f"{a.get('hook', '?')}/{a.get('offer', '?')}" if a.get("copy") else "(no copy captured)"
        print(f"  {a['days_running']:>3}d  {a['advertiser']:<28} {tag}")


if __name__ == "__main__":
    main()
