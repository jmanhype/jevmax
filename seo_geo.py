#!/usr/bin/env python3
"""SEO/GEO workflows for exported Search Console and AI-citation data.

These workflows are deterministic and offline. They do not log into Search
Console, scrape Bing, or query AI engines. They analyze exports you supply.

Commands:
  python3 seo_geo.py search-console benchmarks/search_console_sample.csv \
      --own-domain example.com
  python3 seo_geo.py citations benchmarks/citation_sample.csv \
      --own-domain example.com
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


QUERY_ALIASES = {"query", "queries", "search query", "search terms report", "top queries"}
PAGE_ALIASES = {"page", "landing page", "url"}


def canonical_header(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


def read_table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    start = 0
    for i, row in enumerate(rows[:10]):
        normalized = {canonical_header(x) for x in row if x}
        if normalized & QUERY_ALIASES:
            start = i
            break
    if not rows:
        return []
    header = rows[start]
    return [dict(zip(header, row)) for row in rows[start + 1 :] if any(x.strip() for x in row)]


def pick(row: dict[str, str], names: set[str]) -> str:
    for key, value in row.items():
        if canonical_header(key) in names:
            return value
    return ""


def number(value: str) -> float:
    value = (value or "").strip().replace("%", "").replace(",", "")
    return float(value or 0)


def pct(value: str) -> float:
    return number(value) / (100.0 if "%" in (value or "") else 1.0)


def expected_ctr_for_position(position: float) -> float:
    """Rough organic CTR curve used only to prioritize, not to promise uplift."""
    position = max(1.0, position)
    return max(0.001, 0.16 * math.exp(-0.22 * position))


def is_own_page(page: str, own_domain: str) -> bool:
    if not own_domain:
        return False
    host = urlparse(page).netloc
    return own_domain in host if host else True


def action_for(row: dict) -> tuple[str, str]:
    pos = float(row["position"])
    ctr = float(row["ctr"])
    impressions = int(float(row["impressions"]))
    gap = float(row["expected_ctr"]) - ctr
    if pos <= 5 and ctr < 0.02:
        return ("title_meta", "Top-5 position but weak CTR: rewrite title/meta description for intent")
    if pos <= 15 and gap > 0:
        return ("quick_win", "Strengthen intent match, internal links, and above-fold proof")
    if pos <= 30 and impressions >= 500:
        return ("refresh", "Refresh/expand the page, add comparison schema, and build supporting links")
    return ("monitor", "No deterministic action yet; keep monitoring")


def search_console(path: Path, own_domain: str, min_impressions: int) -> dict:
    rows = []
    for raw in read_table(path):
        query = pick(raw, QUERY_ALIASES)
        page = pick(raw, PAGE_ALIASES)
        if not query:
            continue
        position = number(pick(raw, {"position", "avg. position", "average position"}))
        clicks = number(pick(raw, {"clicks"}))
        impressions = number(pick(raw, {"impressions"}))
        ctr_raw = pick(raw, {"ctr", "click rate"})
        ctr = pct(ctr_raw) if "%" in ctr_raw else number(ctr_raw)
        expected = expected_ctr_for_position(position)
        potential = max(0, impressions * (expected - ctr))
        row = {
            "query": query,
            "page": page,
            "clicks": int(clicks),
            "impressions": int(impressions),
            "ctr": round(ctr, 6),
            "expected_ctr": round(expected, 6),
            "position": round(position, 2),
            "click_potential": round(potential, 1),
            "own_page": is_own_page(page, own_domain),
        }
        action, recommendation = action_for(row)
        row["action"] = action
        row["recommendation"] = recommendation
        rows.append(row)

    prioritized = sorted(
        [r for r in rows if r["impressions"] >= min_impressions],
        key=lambda r: (r["click_potential"], r["impressions"]),
        reverse=True,
    )
    page_groups: dict[str, dict] = defaultdict(lambda: {"impressions": 0, "clicks": 0, "queries": 0, "actions": Counter()})
    for row in rows:
        page = row["page"] or "(no page dimension)"
        g = page_groups[page]
        g["impressions"] += row["impressions"]
        g["clicks"] += row["clicks"]
        g["queries"] += 1
        g["actions"][row["action"]] += 1
    pages = [
        {"page": page, **vals, "actions": dict(vals["actions"])}
        for page, vals in sorted(page_groups.items(), key=lambda kv: kv[1]["impressions"], reverse=True)
    ]
    by_action = Counter(r["action"] for r in rows)
    return {
        "source": str(path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "own_domain": own_domain,
        "min_impressions": min_impressions,
        "rows": rows,
        "prioritized": prioritized,
        "pages": pages,
        "action_mix": dict(by_action),
        "totals": {
            "queries": len(rows),
            "impressions": sum(r["impressions"] for r in rows),
            "clicks": sum(r["clicks"] for r in rows),
            "estimated_click_potential": round(sum(r["click_potential"] for r in rows), 1),
        },
        "method_note": "Expected CTR is a rough prioritization curve, not a forecast. Actions require human review.",
    }


def citations(path: Path, own_domain: str) -> dict:
    rows = read_table(path)
    groups: dict[tuple[str, str], dict] = defaultdict(lambda: {"checks": 0, "brand_mentions": 0, "own_citations": 0, "ranks": [], "urls": Counter()})
    for raw in rows:
        engine = pick(raw, {"engine", "assistant", "provider"}).strip() or "unknown"
        query = pick(raw, {"query", "prompt"}).strip()
        url = pick(raw, {"cited_url", "url", "citation_url"}).strip()
        rank = number(pick(raw, {"rank", "position"}))
        brand = pick(raw, {"mentions_brand", "brand_mentioned"}).strip().lower()
        g = groups[(engine, query)]
        g["checks"] += 1
        if brand in {"yes", "true", "1"}:
            g["brand_mentions"] += 1
        if url and own_domain and own_domain in (urlparse(url).netloc + urlparse(url).path):
            g["own_citations"] += 1
        if url:
            g["ranks"].append(rank)
            g["urls"][url] += 1

    answers = []
    for (engine, query), g in groups.items():
        answers.append({
            "engine": engine,
            "query": query,
            "checks": g["checks"],
            "brand_mention_rate": round(g["brand_mentions"] / g["checks"], 3),
            "own_citation_rate": round(g["own_citations"] / g["checks"], 3),
            "average_cited_rank": round(sum(g["ranks"]) / len(g["ranks"]), 2) if g["ranks"] else None,
            "top_cited_urls": dict(g["urls"].most_common(5)),
        })
    engine_groups: dict[str, dict] = defaultdict(lambda: {"checks": 0, "brand_mentions": 0, "own_citations": 0})
    for row in answers:
        g = engine_groups[row["engine"]]
        g["checks"] += row["checks"]
        g["brand_mentions"] += row["brand_mention_rate"] * row["checks"]
        g["own_citations"] += row["own_citation_rate"] * row["checks"]
    by_engine = {
        engine: {
            "checks": g["checks"],
            "brand_mention_rate": round(g["brand_mentions"] / g["checks"], 3),
            "own_citation_rate": round(g["own_citations"] / g["checks"], 3),
        }
        for engine, g in engine_groups.items()
    }
    gaps = [x for x in answers if x["own_citation_rate"] < 0.34]
    return {
        "source": str(path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "own_domain": own_domain,
        "answers": sorted(answers, key=lambda x: (x["own_citation_rate"], x["query"])),
        "by_engine": by_engine,
        "gaps": gaps,
        "method_note": "Offline analysis of a citation export; no AI engine was queried.",
    }


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_sc = sub.add_parser("search-console")
    p_sc.add_argument("input")
    p_sc.add_argument("--own-domain", default="")
    p_sc.add_argument("--min-impressions", type=int, default=100)
    p_sc.add_argument("--out", default="seo_geo_report.json")
    p_cit = sub.add_parser("citations")
    p_cit.add_argument("input")
    p_cit.add_argument("--own-domain", required=True)
    p_cit.add_argument("--out", default="citation_report.json")
    args = ap.parse_args()

    if args.cmd == "search-console":
        result = search_console(Path(args.input), args.own_domain, args.min_impressions)
        out = Path(args.out)
        write_json(out, result)
        csv_out = out.with_name(out.stem + "_prioritized.csv")
        if result["prioritized"]:
            with csv_out.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(result["prioritized"][0]))
                w.writeheader()
                w.writerows(result["prioritized"])
        print(json.dumps({"out": str(out), "prioritized_csv": str(csv_out), "totals": result["totals"], "action_mix": result["action_mix"]}, indent=2))
    else:
        result = citations(Path(args.input), args.own_domain)
        out = Path(args.out)
        write_json(out, result)
        print(json.dumps({"out": str(out), "by_engine": result["by_engine"], "gap_count": len(result["gaps"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
