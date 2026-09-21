#!/usr/bin/env python3
"""Validate public-safe Jevmax Studio go-to-market claims and artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = {
    "README.md",
    "CASE_STUDY.md",
    "SALES_KIT.md",
    "OUTREACH_PLAYBOOK.md",
    "PILOT_TRACKER_SCHEMA.md",
    "EVIDENCE_MANIFEST.json",
}

PRIVATE_PATTERNS = (
    r"49852068",
    r"6273184009976",
    r"6273182924776",
    r"straughterguthrie@gmail\.com",
    r"apikey_[A-Za-z0-9_-]+",
    r"Bearer\s+[A-Za-z0-9._-]+",
)

CLAIM_PATTERNS = (
    r"guaranteed\s+ROAS",
    r"production\s+performance\s+lift",
    r"whole[- ]library\s+(?:census|coverage)",
    r"\b30x\b",
    r"\b90%\s+(?:cost|performance)",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def claim_is_excluded(lines: list[str], index: int) -> bool:
    heading = ""
    for line in lines[: index + 1]:
        if line.startswith("#"):
            heading = line.lower()
    if any(
        term in heading
        for term in ("not included", "excluded", "exclusions", "out of scope", "claim discipline", "rules", "poor fit")
    ):
        return True
    line = lines[index].lower()
    return any(term in line for term in ("no ", "not ", "never", "without", "do not"))


def validate_public_safety(gtm: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(gtm.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            for pattern in PRIVATE_PATTERNS:
                if re.search(pattern, line, flags=re.IGNORECASE):
                    errors.append(f"{path.name}: private identifier exposed: {line.strip()}")
            for pattern in CLAIM_PATTERNS:
                if re.search(pattern, line, flags=re.IGNORECASE) and not claim_is_excluded(lines, index):
                    errors.append(f"{path.name}: unsupported claim: {line.strip()}")
    return errors


def validate_manifest(gtm: Path) -> tuple[dict, list[str]]:
    errors: list[str] = []
    path = gtm / "EVIDENCE_MANIFEST.json"
    try:
        manifest = load_json(path)
    except json.JSONDecodeError as exc:
        return {}, [f"invalid EVIDENCE_MANIFEST.json: {exc}"]

    required = {
        "schema",
        "case_study",
        "sales_kit",
        "outreach_playbook",
        "pilot_tracker_schema",
        "public_safe_rules",
        "measured_facts",
        "source_artifacts",
    }
    missing = sorted(required - set(manifest))
    if missing:
        errors.append(f"manifest missing keys: {missing}")
    if manifest.get("schema") != "jevmax-studio-gtm-evidence-v1":
        errors.append("wrong GTM manifest schema")
    for key in ("case_study", "sales_kit", "outreach_playbook", "pilot_tracker_schema"):
        if not (gtm / str(manifest.get(key, ""))).is_file():
            errors.append(f"manifest document missing: {key}")
    for rel in manifest.get("source_artifacts", []):
        if not (gtm / rel).resolve().exists():
            errors.append(f"source artifact missing: {rel}")

    expected = {
        "estimated_active_ads": 6792,
        "returned_bounded_scan": 50,
        "current_only_ids": 29,
        "prior_sample_overlap": 21,
        "longitudinal_snapshot_ids": 103,
        "gpt_image_25_flare_credits": 0,
        "gpt_image_25_sunburst_credits": 0,
        "v6_720p_5s_no_audio_credits": 40,
        "minimax_h3_768p_5s_credits": 150,
        "seedance_25_1080p_5s_credits": 850,
        "projected_8_video_v6_credits": 320,
    }
    facts = manifest.get("measured_facts", {})
    for key, value in expected.items():
        if facts.get(key) != value:
            errors.append(f"measured fact mismatch: {key} expected {value}, got {facts.get(key)}")
    return manifest, errors


def validate_sources(gtm: Path) -> list[str]:
    errors: list[str] = []
    paths = {
        "scan": (gtm / "../../runs/2026-09-20/ad_library_airpods_mcp.json").resolve(),
        "report": (gtm / "../../runs/2026-09-20/airpods_scan_report.json").resolve(),
        "diff": (gtm / "../../runs/2026-09-20/airpods_scan_diff.json").resolve(),
        "snapshot": (gtm / "../../snapshots/2026-09-20.json").resolve(),
    }
    try:
        scan = load_json(paths["scan"])
        report = load_json(paths["report"])
        diff = load_json(paths["diff"])
        snapshot = load_json(paths["snapshot"])
        if scan.get("estimated_total_count") != 6792 or len(scan.get("ads", [])) != 50:
            errors.append("bounded scan source no longer reconciles")
        if report.get("unique_ad_count") != 50 or report.get("tagged_ad_count") != 21:
            errors.append("scan report source no longer reconciles")
        if diff.get("new_count") != 29 or diff.get("retained_count") != 21:
            errors.append("scan diff source no longer reconciles")
        if len(snapshot) != 103:
            errors.append("snapshot source no longer reconciles")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"source reconciliation failed: {exc}")
    return errors


def validate_links(gtm: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(gtm.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(f"{path.name}: missing link target {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gtm-root", default=Path(__file__).parent / "gtm")
    args = parser.parse_args()
    gtm = Path(args.gtm_root).resolve()

    errors = [f"missing required GTM file: {name}" for name in sorted(REQUIRED_FILES) if not (gtm / name).is_file()]
    if not errors:
        _, manifest_errors = validate_manifest(gtm)
        errors.extend(manifest_errors)
        errors.extend(validate_public_safety(gtm))
        errors.extend(validate_sources(gtm))
        errors.extend(validate_links(gtm))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "status": "PASS",
                "documents": len(REQUIRED_FILES),
                "public_safety": "PASS",
                "source_reconciliation": "PASS",
                "links": "PASS",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
