#!/usr/bin/env python3
"""Deterministic validation for the Jevmax Studio product portfolio."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


EXPECTED = [
    ("category-signal-audit", 1, "brand-identity-system"),
    ("brand-identity-system", 2, "creative-test-sprint"),
    ("creative-test-sprint", 3, "paid-launch-kit"),
    ("paid-launch-kit", 4, "growth-loop"),
    ("growth-loop", 5, "creative-test-sprint"),
]

REQUIRED_FILES = ("TEMPLATE.md", "MANIFEST.json", "EVIDENCE.md", "PORTFOLIO.md")
REQUIRED_MANIFEST_KEYS = {
    "schema",
    "product_id",
    "name",
    "status",
    "route_order",
    "client_question",
    "next_product",
    "reusable_template",
    "portfolio_summary",
    "evidence",
    "artifacts",
    "measured_cost",
    "qa",
    "policy",
}
REQUIRED_TEMPLATE_SECTIONS = {
    "inputs",
    "output",
    "qa",
    "delivery checklist",
}


def fail(messages: list[str]) -> int:
    for message in messages:
        print(f"ERROR: {message}", file=sys.stderr)
    return 1 if messages else 0


def validate_product(root: Path, slug: str, order: int, next_slug: str) -> list[str]:
    errors: list[str] = []
    directory = root / "products" / f"{order:02d}-{slug}"
    if not directory.is_dir():
        return [f"missing product directory {directory}"]

    for filename in REQUIRED_FILES:
        path = directory / filename
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"{slug}: missing or empty {filename}")

    manifest_path = directory / "MANIFEST.json"
    manifest = {}
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{slug}: invalid MANIFEST.json: {exc}")

    missing_keys = sorted(REQUIRED_MANIFEST_KEYS - set(manifest))
    if missing_keys:
        errors.append(f"{slug}: manifest missing keys {missing_keys}")

    if manifest.get("schema") != "jevmax-studio-product-v1":
        errors.append(f"{slug}: wrong manifest schema")
    if manifest.get("product_id") != slug:
        errors.append(f"{slug}: product_id mismatch")
    if manifest.get("status") != "dogfood_verified":
        errors.append(f"{slug}: status is not dogfood_verified")
    if manifest.get("route_order") != order:
        errors.append(f"{slug}: route_order should be {order}")
    if manifest.get("next_product") != next_slug:
        errors.append(f"{slug}: next_product should be {next_slug}")

    for key in ("reusable_template", "portfolio_summary", "evidence"):
        value = manifest.get(key)
        if value not in REQUIRED_FILES:
            errors.append(f"{slug}: manifest {key} must reference a required package file")
        elif not (directory / value).is_file():
            errors.append(f"{slug}: manifest {key} does not exist")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(f"{slug}: artifacts must be a non-empty list")
    else:
        for index, artifact in enumerate(artifacts, start=1):
            if not isinstance(artifact, dict):
                errors.append(f"{slug}: artifact {index} is not an object")
                continue
            if not artifact.get("role"):
                errors.append(f"{slug}: artifact {index} missing role")
            path_value = artifact.get("path")
            if not path_value:
                errors.append(f"{slug}: artifact {index} missing path")
                continue
            artifact_path = (directory / path_value).resolve()
            if not artifact_path.exists():
                errors.append(f"{slug}: artifact {index} path does not exist: {path_value}")

    measured = manifest.get("measured_cost")
    if not isinstance(measured, dict) or "credits" not in measured or "basis" not in measured:
        errors.append(f"{slug}: measured_cost must contain credits and basis")

    qa = manifest.get("qa")
    if not isinstance(qa, dict) or qa.get("status") not in {"pass", "pass_with_limits"}:
        errors.append(f"{slug}: qa.status must be pass or pass_with_limits")

    policy = manifest.get("policy")
    if not isinstance(policy, dict):
        errors.append(f"{slug}: policy must be an object")
    else:
        if policy.get("live_ad_changes") is not False:
            errors.append(f"{slug}: policy.live_ad_changes must be false")
        if policy.get("premium_generation") is not False:
            errors.append(f"{slug}: policy.premium_generation must be false")

    template_path = directory / "TEMPLATE.md"
    if template_path.is_file():
        template = template_path.read_text(encoding="utf-8").lower()
        for section in REQUIRED_TEMPLATE_SECTIONS:
            if section not in template:
                errors.append(f"{slug}: TEMPLATE.md missing required concept: {section}")

    evidence_path = directory / "EVIDENCE.md"
    if evidence_path.is_file():
        evidence = evidence_path.read_text(encoding="utf-8").lower()
        if not any(word in evidence for word in ("credit", "token", "cost")):
            errors.append(f"{slug}: EVIDENCE.md lacks measured cost language")
        if "qa" not in evidence:
            errors.append(f"{slug}: EVIDENCE.md lacks QA evidence")

    return errors


def validate_index(root: Path) -> list[str]:
    errors: list[str] = []
    index = root / "INDEX.md"
    if not index.is_file():
        return ["missing studio/INDEX.md"]
    text = index.read_text(encoding="utf-8")
    for _, order, _ in EXPECTED:
        slug = EXPECTED[order - 1][0]
        if slug not in text:
            errors.append(f"INDEX.md missing route for {slug}")
    if "validate_portfolio.py" not in text or "benchmark.py" not in text:
        errors.append("INDEX.md must document both verification commands")
    if "explicit approval" not in text.lower():
        errors.append("INDEX.md must state explicit approval for premium generation")
    return errors


def validate_claim_discipline(root: Path) -> list[str]:
    errors: list[str] = []
    banned_patterns = (
        r"\b30x\b",
        r"\b90% (?:cost|performance)",
        r"whole[- ]library",
        r"guaranteed ROAS",
        r"production ROAS lift",
    )
    for path in sorted((root / "products").glob("*/*.md")):
        text_lines = path.read_text(encoding="utf-8").splitlines()
        exclusion_section = False
        for line in text_lines:
            if line.startswith("#"):
                heading = line.lower()
                exclusion_section = any(
                    phrase in heading
                    for phrase in ("not included", "excluded", "exclusions", "out of scope")
                )
            if exclusion_section:
                continue
            for pattern in banned_patterns:
                if re.search(pattern, line, flags=re.IGNORECASE):
                    if not any(negation in line.lower() for negation in ("not", "no ", "never", "without")):
                        errors.append(f"unsupported claim in {path}: {line.strip()}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--studio-root", default=Path(__file__).parent)
    args = parser.parse_args()
    root = Path(args.studio_root).resolve()

    errors: list[str] = []
    for slug, order, next_slug in EXPECTED:
        errors.extend(validate_product(root, slug, order, next_slug))
    errors.extend(validate_index(root))
    errors.extend(validate_claim_discipline(root))

    if errors:
        return fail(errors)

    print(
        json.dumps(
            {
                "status": "PASS",
                "products": len(EXPECTED),
                "required_files_each": len(REQUIRED_FILES),
                "all_manifest_artifacts_exist": True,
                "claim_discipline": "PASS",
                "verification": "Run benchmark.py --min-pass-rate 0.99 for the required 36/36 offline gate.",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
