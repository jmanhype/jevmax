#!/usr/bin/env python3
"""Generate a self-contained static Jevmax status dashboard."""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def workflow_status() -> list[dict]:
    return [
        {"id": 1, "name": "Ad Library scanning", "status": "Bounded production sampling", "detail": "49-ID AirPods baseline; official MCP limit is 50 per query"},
        {"id": 2, "name": "Survival patterns", "status": "Collecting", "detail": "First 60-day read expected around Nov 19, 2026"},
        {"id": 3, "name": "Brief scoring", "status": "Demo verified", "detail": "Concrete angle outranks vague AI hype"},
        {"id": 4, "name": "Buyer search-term sorting", "status": "Ready for real CSV", "detail": "25/25 regression pass; AirPods ICP saved"},
        {"id": 5, "name": "Creative fatigue", "status": "Demo verified", "detail": "5/5 regression pass; ACT/REVIEW bands implemented"},
        {"id": 6, "name": "Ad/page promise match", "status": "Demo verified", "detail": "Caught engineered 30-day vs 14-day offer mismatch"},
        {"id": 7, "name": "Lead scoring", "status": "Demo verified", "detail": "Strong ICP 86–92; student request 11"},
        {"id": 8, "name": "Account audit", "status": "Read-only verified", "detail": "2022 campaigns completed; no live delivery"},
        {"id": 9, "name": "SEO/GEO opportunity audit", "status": "Sample verified", "detail": "Search Console + citation exports analyzed offline"},
    ]


def baseline_mix():
    raw = load_json(ROOT / "ad_library_mcp_raw.json", [])
    ids = {str(x["id"]) for x in raw}
    rows = []
    with (ROOT / "ad_library_mcp_tagged.csv").open(newline="", encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f) if r["id"] in ids]
    hooks = Counter(r.get("hook", "") or "(untagged)" for r in rows)
    offers = Counter(r.get("offer", "") or "(untagged)" for r in rows)
    return {"count": len(ids), "hook_mix": hooks, "offer_mix": offers}


def bar_chart(title: str, values: dict) -> str:
    total = sum(values.values()) or 1
    bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{esc(k)}</span>'
        f'<div class="bar-track"><div class="bar-fill" style="width:{v / total * 100:.2f}%"></div></div>'
        f'<span class="bar-value">{v}</span></div>'
        for k, v in sorted(values.items(), key=lambda kv: -kv[1])
    )
    return f'<section><h2>{esc(title)}</h2>{bars}</section>'


def metric_cards(cards: list[tuple[str, str, str]]) -> str:
    return '<div class="metrics">' + "".join(
        f'<article class="metric"><div class="metric-label">{esc(label)}</div>'
        f'<div class="metric-value">{esc(value)}</div><div class="metric-sub">{esc(sub)}</div></article>'
        for label, value, sub in cards
    ) + "</div>"


def workflow_table(rows: list[dict]) -> str:
    body = "".join(
        f'<tr><td>#{r["id"]}</td><td>{esc(r["name"])}</td>'
        f'<td><span class="status">{esc(r["status"])}</span></td><td>{esc(r["detail"])}</td></tr>'
        for r in rows
    )
    return (
        '<section><h2>Workflows</h2><table><thead><tr><th>#</th><th>Workflow</th>'
        f'<th>Status</th><th>Evidence / limitation</th></tr></thead><tbody>{body}</tbody></table></section>'
    )


def benchmark_section(data: dict) -> str:
    rows = "".join(
        f'<tr><td>{esc(x["name"])}</td><td>{x["pass"]}/{x["n"]}</td>'
        f'<td>{pct(x["accuracy"])}</td></tr>'
        for x in data.get("suites", [])
    )
    return (
        '<section><h2>Offline regression benchmark</h2>'
        f'<p class="muted">Mode: {esc(data.get("mode", "unknown"))}. This is regression evidence, not a blind holdout.</p>'
        '<table><thead><tr><th>Suite</th><th>Cases</th><th>Pass</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></section>'
    )


def seo_section(seo: dict, citations: dict) -> str:
    if not seo or not citations:
        return '<section><h2>SEO/GEO</h2><p class="muted">Sample reports not found.</p></section>'
    engine_rows = "".join(
        f'<tr><td>{esc(engine)}</td><td>{x.get("checks", 0)}</td>'
        f'<td>{pct(x.get("own_citation_rate", 0))}</td><td>{pct(x.get("brand_mention_rate", 0))}</td></tr>'
        for engine, x in citations.get("by_engine", {}).items()
    )
    top = seo.get("prioritized", [])[:5]
    top_rows = "".join(
        f'<tr><td>{esc(x["query"])}</td><td>{x["impressions"]}</td><td>{x["position"]}</td>'
        f'<td>{x["click_potential"]}</td><td>{esc(x["recommendation"])}</td></tr>'
        for x in top
    )
    return (
        '<section><h2>SEO/GEO sample reports</h2>'
        '<div class="two-col"><div><h3>Top Search Console opportunities</h3>'
        '<table><thead><tr><th>Query</th><th>Impr.</th><th>Pos.</th><th>Priority score</th><th>Action</th></tr></thead>'
        f'<tbody>{top_rows}</tbody></table></div><div><h3>AI citation coverage</h3>'
        '<table><thead><tr><th>Engine</th><th>Checks</th><th>Own citation</th><th>Brand mention</th></tr></thead>'
        f'<tbody>{engine_rows}</tbody></table></div></div>'
        '<p class="muted">Expected CTR is a prioritization aid, not a forecast. No AI engine is queried by the script.</p></section>'
    )


def snapshot_section() -> str:
    directory = ROOT / "snapshots"
    snapshots = sorted(directory.glob("*.json")) if directory.exists() else []
    rows = []
    for path in snapshots:
        ids = load_json(path, [])
        rows.append((path.stem, len(ids)))
    body = "".join(f'<tr><td>{esc(d)}</td><td>{n}</td></tr>' for d, n in rows)
    return (
        '<section><h2>Longitudinal snapshots</h2><table><thead><tr><th>Date</th><th>Unique IDs</th></tr></thead>'
        f'<tbody>{body}</tbody></table><p class="muted">First 60-day survival calculation requires a later snapshot.</p></section>'
    )


def generate(out: Path) -> dict:
    benchmark = load_json(ROOT / "benchmark_results.json", {})
    seo = load_json(ROOT / "seo_geo_report.json", {})
    citations = load_json(ROOT / "citation_report.json", {})
    account = load_json(ROOT / "account_snapshot.json", {})
    mix = baseline_mix()
    cards = [
        ("Workflows", "9", "7 core + audit + SEO/GEO"),
        ("Regression", f'{benchmark.get("total_passed", 0)}/{benchmark.get("total_cases", 0)}', "Offline recorded fixtures"),
        ("AirPods baseline", str(mix["count"]), "Official-MCP bounded sample"),
        ("Live delivery", "0", "Both 2022 campaigns completed"),
        ("Missing input", "1", "Real Google Ads search-terms CSV"),
    ]
    campaigns = account.get("campaigns", [])
    campaign_rows = "".join(
        f'<tr><td>{esc(c["name"])}</td><td>{esc(c.get("status", ""))}</td>'
        f'<td>{esc(c.get("delivery", {}).get("status", "unknown"))}</td></tr>'
        for c in campaigns
    )
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Jevmax decision dashboard</title>
<style>
:root{{--bg:#080c14;--panel:#101827;--line:#243247;--text:#e8eef8;--muted:#8fa1ba;--accent:#43d9a3;--warn:#f2c14e;--bad:#ff7a7a}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 system-ui,-apple-system,sans-serif}}
header{{padding:32px max(24px,calc((100% - 1180px)/2));background:linear-gradient(120deg,#0b1220,#102b26 70%,#0b1220);border-bottom:1px solid var(--line)}}
h1{{margin:0;font-size:32px;letter-spacing:-.03em}} header p{{color:var(--muted);max-width:850px}}
main{{max-width:1180px;margin:auto;padding:24px;display:grid;gap:18px}} section{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px}}
h2,h3{{margin:0 0 12px}} .metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}
.metric{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}} .metric-label{{color:var(--muted);font-size:12px;text-transform:uppercase}}
.metric-value{{font-size:28px;font-weight:750;color:var(--accent)}} .metric-sub{{color:var(--muted);font-size:12px}}
table{{width:100%;border-collapse:collapse}} th,td{{padding:10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}} th{{color:var(--muted);font-size:12px;text-transform:uppercase}}
.status{{color:var(--accent)}} .muted{{color:var(--muted)}} .bar-row{{display:grid;grid-template-columns:150px 1fr 40px;gap:10px;align-items:center;margin:8px 0}}
.bar-label{{color:var(--muted);overflow:hidden;text-overflow:ellipsis}} .bar-track{{height:9px;background:#1b2637;border-radius:99px;overflow:hidden}} .bar-fill{{height:100%;background:var(--accent)}}
.bar-value{{text-align:right;color:var(--muted)}} .two-col{{display:grid;grid-template-columns:1.3fr .7fr;gap:16px}} footer{{padding:24px;color:var(--muted);text-align:center}}
@media(max-width:800px){{.two-col{{grid-template-columns:1fr}}.bar-row{{grid-template-columns:100px 1fr 34px}}}}
</style></head><body>
<header><div><h1>Jevmax decision layer</h1><p>Status dashboard for the seven post workflows, account audit, SEO/GEO judgment workflows, and bounded competitive sampling. Claims are separated by evidence state.</p></div></header>
<main>{metric_cards(cards)}{workflow_table(workflow_status())}{benchmark_section(benchmark)}
<section><h2>AirPods competitive baseline</h2><p>49 unique ads from the official Ads MCP route. Three lacked taggable titles.</p><div class="two-col">{bar_chart('Hook mix', mix['hook_mix'])}{bar_chart('Offer mix', mix['offer_mix'])}</div></section>
{seo_section(seo, citations)}<section><h2>Ad account read-only status</h2><table><thead><tr><th>Campaign</th><th>Configured</th><th>Actual delivery</th></tr></thead><tbody>{campaign_rows}</tbody></table><p class="muted">No live campaign changes are permitted by the dashboard or benchmark.</p></section>{snapshot_section()}
<section><h2>Claim discipline</h2><ul><li>Verified locally: workflow fixtures and read-only account status.</li><li>Waiting: 60-day survival and real Google Ads search terms.</li><li>Not claimed: 30x, 90%, “whole Ad Library,” or production ROAS lift.</li></ul></section></main>
<footer>Generated {esc(date.today().isoformat())} · Static offline artifact</footer></body></html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return {"out": str(out), "bytes": out.stat().st_size, "workflows": 9, "baseline_ads": mix["count"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="dashboard.html")
    args = ap.parse_args()
    result = generate(Path(args.out))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
