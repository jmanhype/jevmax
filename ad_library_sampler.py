#!/usr/bin/env python3
"""Bounded multi-query Meta Ad Library sampling and snapshot diffing.

The official `ads_library_search` MCP tool returns at most 50 results and has
no cursor. This module therefore makes the sampling boundary explicit:
multi-query sampling is useful competitive intelligence, but it is not a
whole-library census.

This script does not call Meta. The agent/automation fetches each query through
MCP, saves JSON arrays, then uses this script to validate, combine, deduplicate,
diff, and report those local files.

Commands:
  python3 ad_library_sampler.py plan --plan ad_library_sample_plan.json
  python3 ad_library_sampler.py combine INPUT.json... \
      --plan ad_library_sample_plan.json --out samples/combined.json
  python3 ad_library_sampler.py diff samples/baseline.json samples/current.json
  python3 ad_library_sampler.py report samples/combined.json \
      --tags ad_library_mcp_tagged.csv
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_AD_FIELDS = {"id", "page_name", "ad_delivery_start_time"}


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def validate_plan(plan: dict) -> None:
    required = {"name", "countries", "ad_active_status", "ad_type", "limit_per_query", "max_queries_per_run", "queries"}
    missing = sorted(required - set(plan))
    if missing:
        raise ValueError(f"sample plan missing fields: {', '.join(missing)}")
    if not 1 <= int(plan["limit_per_query"]) <= 50:
        raise ValueError("official ads_library_search limit_per_query must be between 1 and 50")
    if int(plan["max_queries_per_run"]) < 1:
        raise ValueError("max_queries_per_run must be positive")
    if not plan["queries"]:
        raise ValueError("queries cannot be empty")
    if not plan["countries"]:
        raise ValueError("countries cannot be empty")


def plan_manifest(plan_path: Path) -> dict:
    plan = load_json(plan_path)
    validate_plan(plan)
    selected = plan["queries"][: int(plan["max_queries_per_run"])]
    return {
        "plan_file": str(plan_path),
        "plan_name": plan["name"],
        "countries": plan["countries"],
        "ad_active_status": plan["ad_active_status"],
        "ad_type": plan["ad_type"],
        "limit_per_query": int(plan["limit_per_query"]),
        "selected_queries": selected,
        "selected_query_count": len(selected),
        "requested_max_ads": len(selected) * int(plan["limit_per_query"]),
        "policy": plan.get(
            "policy",
            "Bounded official-MCP sampling only; not bulk extraction and not a whole-library census.",
        ),
        "fetch_instructions": [
            "For each selected_queries entry, call official Meta Ads MCP ads_library_search once.",
            "Use the plan countries/ad_active_status/ad_type/limit_per_query exactly.",
            "Save each result as a JSON array before combining.",
            "Do not retry indefinitely or attempt to circumvent the 50-result tool limit.",
        ],
    }


def normalize_ad(ad: dict, source: str, query: str | None = None) -> dict:
    # Support both original MCP payloads and files converted by mcp_to_raw.py.
    if "page_name" not in ad and "advertiser" in ad:
        ad = {**ad, "page_name": ad.get("advertiser")}
    if "ad_delivery_start_time" not in ad and "started" in ad:
        parsed = datetime.strptime(ad["started"], "%b %d, %Y").replace(tzinfo=timezone.utc)
        ad = {**ad, "ad_delivery_start_time": int(parsed.timestamp())}
    missing = REQUIRED_AD_FIELDS - set(ad)
    if missing:
        raise ValueError(f"ad {ad.get('id', '<missing id>')} from {source} missing fields: {sorted(missing)}")
    return {
        "id": str(ad["id"]),
        "page_id": str(ad.get("page_id", "")),
        "page_name": ad.get("page_name", ""),
        "title": ad.get("ad_creative_link_title") or ad.get("copy") or "",
        "ad_creation_time": ad.get("ad_creation_time"),
        "ad_delivery_start_time": ad.get("ad_delivery_start_time"),
        "currency": ad.get("currency", ""),
        "snapshot_url": ad.get("ad_snapshot_url", ""),
        "source_file": source,
        "query": query,
    }


def iter_ads(path: Path):
    data = load_json(path)
    if isinstance(data, list):
        for item in data:
            yield normalize_ad(item, str(path))
    elif isinstance(data, dict) and isinstance(data.get("ads"), list):
        query = data.get("query")
        for item in data["ads"]:
            yield normalize_ad(item, str(path), query)
    else:
        raise ValueError(f"{path} must be a JSON array or an object containing an ads array")


def combine(inputs: list[Path], plan_path: Path | None, out: Path) -> dict:
    if plan_path:
        manifest = plan_manifest(plan_path)
    else:
        manifest = {
            "plan_file": None,
            "plan_name": "Unplanned local combination",
            "policy": "No sampling plan supplied; coverage is unknown.",
        }
    combined: dict[str, dict] = {}
    source_counts: Counter = Counter()
    duplicate_count = 0
    for path in inputs:
        before = len(combined)
        for ad in iter_ads(path):
            source_counts[str(path)] += 1
            if ad["id"] in combined:
                duplicate_count += 1
                combined[ad["id"]]["also_seen_in"].append({"source": ad["source_file"], "query": ad["query"]})
            else:
                ad["also_seen_in"] = []
                combined[ad["id"]] = ad
        if len(combined) == before and not source_counts[str(path)]:
            raise ValueError(f"{path} contained zero valid ads")

    ads = sorted(combined.values(), key=lambda a: (a["ad_delivery_start_time"] or 0, a["id"]), reverse=True)
    result = {
        **manifest,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "input_files": [str(p) for p in inputs],
        "unique_ad_count": len(ads),
        "input_ad_count": sum(source_counts.values()),
        "duplicate_ad_count": duplicate_count,
        "source_row_counts": dict(source_counts),
        "ads": ads,
        "coverage_warnings": [
            "Unique count can be smaller than requested_max_ads because queries overlap.",
            "A clean combination of bounded queries is still not a whole-library census.",
            "Newest-first/no-cursor behavior means long-running ads can be underrepresented.",
        ],
    }
    write_json(out, result)
    return result


def ids_from_sample(path: Path) -> set[str]:
    data = load_json(path)
    if isinstance(data, list):
        return {str(x["id"]) for x in data}
    if isinstance(data, dict) and isinstance(data.get("ads"), list):
        return {str(x["id"]) for x in data["ads"]}
    raise ValueError(f"{path} is neither an ad array nor a combined sample object")


def diff(baseline: Path, current: Path, out: Path | None) -> dict:
    old_ids, new_ids = ids_from_sample(baseline), ids_from_sample(current)
    result = {
        "baseline": str(baseline),
        "current": str(current),
        "baseline_count": len(old_ids),
        "current_count": len(new_ids),
        "retained_count": len(old_ids & new_ids),
        "new_count": len(new_ids - old_ids),
        "missing_count": len(old_ids - new_ids),
        "observed_retention_rate": round(len(old_ids & new_ids) / len(old_ids), 4) if old_ids else None,
        "new_ids": sorted(new_ids - old_ids),
        "missing_ids": sorted(old_ids - new_ids),
        "interpretation": (
            "Observed retention only means IDs appeared in both bounded samples. "
            "It is not 60-day survival unless the snapshots are at least 60 days apart "
            "and sampling coverage is stable."
        ),
    }
    if out:
        write_json(out, result)
    return result


def load_tags(path: Path | None) -> dict[str, tuple[str, str]]:
    if not path:
        return {}
    tags = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            tags[str(row["id"])] = (row.get("hook") or "(untagged)", row.get("offer") or "(untagged)")
    return tags


def domainish(value: str) -> str:
    value = value.strip().lower()
    if not value:
        return "(no title)"
    parsed = urlparse(value if "://" in value else "https://" + value)
    return parsed.netloc or parsed.path.split("/")[0]


def report(path: Path, tags_path: Path | None) -> dict:
    raw = load_json(path)
    ads = raw if isinstance(raw, list) else raw.get("ads", [])
    tags = load_tags(tags_path)
    advertisers = Counter(a["page_name"] for a in ads)
    domains = Counter(domainish(a.get("title", "")) for a in ads)
    starts = Counter(datetime.fromtimestamp(a["ad_delivery_start_time"], tz=timezone.utc).date().isoformat() for a in ads)
    hooks, offers = Counter(), Counter()
    tagged_count = 0
    for ad in ads:
        if ad["id"] in tags:
            tagged_count += 1
            hooks[tags[ad["id"]][0]] += 1
            offers[tags[ad["id"]][1]] += 1
    return {
        "sample": str(path),
        "unique_ad_count": len(ads),
        "tagged_ad_count": tagged_count,
        "top_advertisers": advertisers.most_common(15),
        "top_link_titles": domains.most_common(15),
        "delivery_start_dates": dict(sorted(starts.items(), reverse=True)),
        "hook_mix": dict(hooks),
        "offer_mix": dict(offers),
        "coverage_warnings": raw.get("coverage_warnings", []) if isinstance(raw, dict) else [],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan")
    p_plan.add_argument("--plan", default="ad_library_sample_plan.json")
    p_plan.add_argument("--out")

    p_combine = sub.add_parser("combine")
    p_combine.add_argument("inputs", nargs="+")
    p_combine.add_argument("--plan")
    p_combine.add_argument("--out", required=True)

    p_diff = sub.add_parser("diff")
    p_diff.add_argument("baseline")
    p_diff.add_argument("current")
    p_diff.add_argument("--out")

    p_report = sub.add_parser("report")
    p_report.add_argument("input")
    p_report.add_argument("--tags")
    p_report.add_argument("--out")

    args = ap.parse_args()
    if args.cmd == "plan":
        result = plan_manifest(Path(args.plan))
        if args.out:
            write_json(Path(args.out), result)
    elif args.cmd == "combine":
        result = combine([Path(x) for x in args.inputs], Path(args.plan) if args.plan else None, Path(args.out))
    elif args.cmd == "diff":
        result = diff(Path(args.baseline), Path(args.current), Path(args.out) if args.out else None)
    else:
        result = report(Path(args.input), Path(args.tags) if args.tags else None)
        if args.out:
            write_json(Path(args.out), result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
