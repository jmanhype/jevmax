#!/usr/bin/env python3
"""Workflow #6 — Check ad-to-landing-page match.

Scores whether the landing page delivers what the ad promised — usually the
cheapest CVR fix in an account. Paste the ad copy and the page text (or a
faithful summary of it).

Usage:
    python3 page_match.py --ad "AD COPY..." --page-file page.txt [--out match.json]
"""
import argparse
import json
import sys

from typesafe import ask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ad", required=True, help="The ad's promise (headline + body copy)")
    ap.add_argument("--page-file", required=True, help="Text file with the landing page content")
    ap.add_argument("--out", default="match.json")
    args = ap.parse_args()

    with open(args.page_file, encoding="utf-8") as f:
        page = f.read().strip()

    state = {"ad_promise": args.ad, "page_content": page}
    questions = {
        "delivers": {
            "type": "noul",
            "instructions": (
                "Does `page_content` deliver the specific promise made in "
                "`ad_promise` — the offer, price/terms, and outcome a clicker "
                "expects to find above the fold?"
            ),
            "criteria": {
                "true": "The promised offer is visible and terms match",
                "false": "Offer missing, buried, changed, or contradicted",
            },
        },
        "match_score": {
            "type": "score",
            "instructions": "How tightly does `page_content` match `ad_promise`?",
            "criteria": [
                "Bait and switch: page sells something else",
                "Loose: same product, different offer or audience",
                "Partial: promise present but buried or softened",
                "Tight: promise delivered clearly, minor friction",
                "Exact: message match, offer terms identical, frictionless",
            ],
        },
        "biggest_gap": {
            "type": "choice",
            "instructions": "What is the single biggest gap between `ad_promise` and `page_content`?",
            "criteria": {
                "offer_mismatch": "The promised offer/pricing is absent or different",
                "message_mismatch": "Right offer, wrong framing or audience",
                "buried_value": "Promise present but below the fold or diluted",
                "trust_gap": "Missing proof the ad implied (social proof, guarantee)",
                "no_gap": "Page delivers cleanly",
            },
        },
    }

    answers, usage = ask(state, questions)
    result = {
        "delivers_promise": answers["delivers"]["noul"],
        "match_score_0_4": answers["match_score"]["score"],
        "match_confidence": answers["match_score"].get("confidence"),
        "biggest_gap": answers["biggest_gap"]["choice"],
        "usage": usage,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
