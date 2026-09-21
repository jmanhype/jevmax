#!/usr/bin/env python3
"""Create the internal studio productization backlog in Paivot/nd."""

from __future__ import annotations

import argparse
import json
import subprocess


PRODUCTS = [
    (
        "Category Signal Audit package",
        """Create the Category Signal Audit product package with reusable template, manifest, measured evidence, and portfolio summary.

Acceptance criteria:
- TEMPLATE.md is client-ready and reusable.
- MANIFEST.json validates and links only existing artifacts.
- EVIDENCE.md records measured cost and QA evidence.
- PORTFOLIO.md states outcome, inclusions, exclusions, timeline, and next route.""",
    ),
    (
        "Brand Identity System package",
        """Create the Brand Identity System product package around the approved Ava identity system.

Acceptance criteria:
- TEMPLATE.md is client-ready and reusable.
- MANIFEST.json validates and links only existing artifacts.
- EVIDENCE.md records identity, seed, cost, and QA evidence.
- PORTFOLIO.md states outcome, inclusions, exclusions, timeline, and next route.""",
    ),
    (
        "Creative Test Sprint package",
        """Create the Creative Test Sprint package using existing V6-only videos and the measured 40-credit no-audio route.

Acceptance criteria:
- TEMPLATE.md is client-ready and reusable.
- MANIFEST.json validates and links only existing artifacts.
- EVIDENCE.md records historical and current V6 cost, QA, and limitations.
- PORTFOLIO.md states outcome, inclusions, exclusions, timeline, and next route.""",
    ),
    (
        "Paid Launch Kit package",
        """Create the Paid Launch Kit package with hero asset, copy variants, disclosure, measurement, and approval gates.

Acceptance criteria:
- TEMPLATE.md is client-ready and reusable.
- MANIFEST.json validates and links only existing artifacts.
- EVIDENCE.md records zero-new-generation dogfood cost and QA evidence.
- PORTFOLIO.md states outcome, inclusions, exclusions, timeline, and next route.""",
    ),
    (
        "Growth Loop package",
        """Create the Growth Loop package with weekly and monthly operating cadence, snapshot survival rules, and refresh gates.

Acceptance criteria:
- TEMPLATE.md is client-ready and reusable.
- MANIFEST.json validates and links only existing artifacts.
- EVIDENCE.md records the current snapshot and automation evidence.
- PORTFOLIO.md states outcome, inclusions, exclusions, timeline, and next route.""",
    ),
    (
        "Studio portfolio validator and routing index",
        """Create the portfolio-wide routing index and deterministic validator.

Acceptance criteria:
- INDEX.md routes a client to the correct product.
- validate_portfolio.py checks all five product packages.
- Every artifact referenced by every manifest exists.
- Premium generation policy is encoded.
- Offline regression remains 36/36.""",
    ),
]


def run(args: list[str]) -> dict:
    result = subprocess.run(
        ["pvg", *args],
        check=True,
        text=True,
        capture_output=True,
    )
    if not result.stdout.strip():
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout.strip()}


def create_issue(title: str, body: str, **flags: str) -> dict:
    args = [
        "issues",
        "create",
        title,
        "--body",
        body,
        "--json",
    ]
    for key, value in flags.items():
        args.extend([f"--{key.replace('_', '-')}", value])
    return run(args)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epic-title", default="Jevmax Studio internal dogfood portfolio")
    args = parser.parse_args()

    existing_epics = run(["issues", "list", "--type", "epic", "--json"])
    epic = next(
        (
            item
            for item in existing_epics
            if item.get("Title") == args.epic_title or item.get("title") == args.epic_title
        ),
        None,
    )
    if epic is None:
        epic = create_issue(
            args.epic_title,
            """Productize Jevmax Studio into five verified client-facing deliverables with templates, manifests, measured evidence, portfolio summaries, routing, and deterministic verification.

Policy: free GPT Image 2.5 and 40-credit V6 720p videos are pre-approved; other paid generation requires explicit operator approval.""",
            type="epic",
            priority="P0",
            labels="studio,dogfood,productization",
        )
    print(json.dumps(epic, indent=2))
    epic_id = epic.get("id") or epic.get("ID") or epic.get("issue", {}).get("id")
    if not epic_id:
        raise RuntimeError(f"Could not parse epic id from response: {epic}")

    created = []
    for index, (title, body) in enumerate(PRODUCTS, start=1):
        issue = create_issue(
            title,
            body,
            type="task",
            priority=f"P{min(index, 3)}",
            parent=epic_id,
            labels="studio,dogfood",
        )
        created.append(issue)
        print(json.dumps(issue, indent=2))

    output = {
        "epic": epic_id,
        "stories": [item.get("id") or item.get("ID") for item in created],
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
