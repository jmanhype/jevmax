#!/usr/bin/env python3
"""Build the internal Category Signal Sprint deliverable from current artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_report(
    scan: dict,
    account: dict,
    ranked_concepts: list[dict],
    manifest: list[dict],
    render_log: list[dict],
) -> str:
    completed_v002 = [
        row for row in render_log
        if row["variant_id"].startswith("V002-") and row["status"] == "completed"
    ]
    v002_ids = {row["variant_id"] for row in completed_v002}
    v002_assets = [row for row in manifest if row["variant_id"] in v002_ids]
    render_by_id = {row["variant_id"]: row for row in completed_v002}

    top_advertisers = ", ".join(
        f"{name} ({count})" for name, count in scan["top_advertisers"][:5]
    )
    hook_mix = ", ".join(
        f"{name} {count}" for name, count in scan["hook_mix"].items()
    )
    offer_mix = ", ".join(
        f"{name} {count}" for name, count in scan["offer_mix"].items()
    )

    concept_lines = []
    for row in ranked_concepts[:4]:
        concept_lines.append(
            f"- **{row['title']}** — {row['tagline']}  \n"
            f"  Style: {row['style_family']}  \n"
            f"  Eyecandy technique: {row['eyecandy_technique']}  \n"
            f"  Gate score: {row['total']}"
        )

    campaign_lines = []
    for campaign in account["campaigns"]:
        campaign_lines.append(
            f"- {campaign['name']}: {campaign['status']}"
        )

    asset_lines = []
    for asset in v002_assets:
        local_file = render_by_id[asset["variant_id"]]["local_file"]
        asset_lines.append(
            f"- `{asset['variant_id']}` — {asset['aspect']}, {asset['duration_s']}s, "
            f"video: `{local_file}`"
        )

    return f"""# Category Signal Sprint — Internal Dogfood Deliverable

## Executive summary

This package combines the current AirPods-category signal, live account audit,
Lost Future/Eyecandy concept gate, and the existing V6-only creative batch into
one client-facing deliverable. No new generation credits were spent while
assembling this report.

## Category signal

- Unique ads in current bounded sample: **{scan['unique_ad_count']}**
- Tagged ads: **{scan['tagged_ad_count']}**
- Top advertisers: {top_advertisers}
- Hook mix: {hook_mix}
- Offer mix: {offer_mix}

This is a bounded sample, not a whole-library census.

## Account readiness

Account **{account['account']['name']}** ({account['account']['id']}) is
{account['account']['status']}.

Campaigns:

{chr(10).join(campaign_lines)}

Pixel status:

- {account['pixels'][0]['name']}: {'active' if account['pixels'][0]['ever_fired'] else 'never fired'}

Page status:

- {account['pages'][0]['name']}: lead-gen ToS {'accepted' if account['pages'][0]['leadgen_tos_accepted'] else 'not accepted'}

## Creative system

Top concepts from the Jev gate:

{chr(10).join(concept_lines)}

## V6 asset manifest

The following V6-only variants are already on disk:

{chr(10).join(asset_lines)}

## Decision

The current package is strong enough to show a client, but two account issues
should be fixed before paid launch:

1. Install and fire the pixel.
2. Accept lead-gen ToS if lead campaigns are in scope.

## Next actions

1. Refresh the category sample next Monday.
2. Keep the current 8-variant V6 batch as the dogfood creative set.
3. Use the winning Lost Future concept as the next paid-test candidate.
4. Re-run the account audit after pixel and ToS fixes.

## Cost note

Assembling this deliverable used existing artifacts only. The historical V6
batch cost is already recorded in the render log. Future V6-only production
should use the currently measured 40-credit/no-audio route rather than the
older 50-credit/audio route.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", required=True)
    parser.add_argument("--account", required=True)
    parser.add_argument("--concepts", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--render-log", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    report = build_report(
        load_json(Path(args.scan)),
        load_json(Path(args.account)),
        load_csv(Path(args.concepts)),
        load_csv(Path(args.manifest)),
        load_csv(Path(args.render_log)),
    )
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(report, encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
