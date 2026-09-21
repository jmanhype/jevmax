#!/usr/bin/env python3
"""Bridge: Meta Ads MCP `ads_library_search` output -> ad_library_scan.py input.

Route decision (verified 2026-09-20): the Ads MCP Server we dogfooded this
session exposes ads_library_search, which returns live ads with page, link
title, and ad_delivery_start_time — enough for #1 indexing/tagging and
days_running, with zero credentials beyond the existing MCP login. The
anonymous browser scrape stays as the fallback for full body copy, which the
MCP listing payload does NOT carry (title only, no CTA/domain/format).

MCP search order is newest-first and the tool exposes no cursor, so keyword
and page queries surface fresh ads. Survival (#2) therefore needs either
recurring scans building a longitudinal dataset or the official Ad Library
API's deep pagination for the 60-day+ tail.

Usage: python3 mcp_to_raw.py [mcp_sample.json...] [--out ad_library_mcp_raw.json]
"""
import argparse
import json
from datetime import datetime, timezone


def convert(ad):
    start = datetime.fromtimestamp(ad["ad_delivery_start_time"], tz=timezone.utc)
    return {
        "id": str(ad["id"]),
        "started": start.strftime("%b %d, %Y"),
        "advertiser": ad.get("page_name"),
        "copy": ad.get("ad_creative_link_title") or None,
        "domain": None,
        "cta": None,
        "currency": ad.get("currency"),
        "snapshot_url": ad.get("ad_snapshot_url"),
        "mcp_fields": sorted(k for k in ad if k != "id"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", help="JSON arrays as returned by ads_library_search")
    ap.add_argument("--out", default="ad_library_mcp_raw.json")
    args = ap.parse_args()

    seen, ads = set(), []
    for path in args.inputs:
        with open(path, encoding="utf-8") as f:
            for ad in json.load(f):
                if ad["id"] not in seen:
                    seen.add(ad["id"])
                    ads.append(convert(ad))

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(ads, f, indent=1)
    print(f"{sum(1 for p in args.inputs for _ in [0])} file(s) -> {len(ads)} unique ads -> {args.out}")


if __name__ == "__main__":
    main()
