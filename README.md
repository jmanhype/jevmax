# jevmax — the Jevmaxxing playbook, built

The 7 workflows from the "Jevmaxxing for marketers" post, implemented against
the TypeSafe System One API (model: Jev). Code owns workflow and arithmetic;
Jev owns judgment. No dependencies — Python 3 stdlib only.

## Start here

```bash
python3 jevmax.py status
python3 jevmax.py selftest
python3 jevmax.py dashboard --out dashboard.html
open dashboard.html
```

`selftest` is deliberately offline: it compiles every script, runs the recorded
regression benchmark, checks survival boundaries, exercises the bounded sampler,
analyzes the SEO/GEO fixtures, and regenerates the dashboard. It makes no
TypeSafe or Meta API calls and performs no live ad changes.

Setup: `TYPESAFE_API_KEY` in env or in `../.env` (already configured).

## The workflows

| # | Script | Input | Output |
|---|--------|-------|--------|
| 3 | `score_briefs.py` | briefs.csv + `--brand` | ranked_briefs.csv (hook / brand fit / survival odds, ranked) |
| 4 | `sort_search_terms.py` | Google Ads search-terms export + `--context` | decisions.csv + negatives.csv (p_buyer, KEEP/WATCH/NEGATIVE) |
| 5 | `fatigue.py` | ads.csv (frequency_delta, ctr_delta) | fatigue_decisions.csv (replace/refresh/leave + ACT/REVIEW band; only flagged ads cost tokens) |
| 6 | `page_match.py` | ad copy + page text file | match.json (delivers_promise, match score, biggest gap) |
| 7 | `score_leads.py` | leads.csv + `--icp` | scored_leads.csv (0–100, sorted) |
| 1/2 | `ad_library_scan.py` + `mcp_to_raw.py` + `survival.py` | MCP `ads_library_search` JSON dumps | `ad_library_*_tagged.csv`, `snapshots/`, survival report |
| 8 | `audit.py` | `account_snapshot.json` (agent-assembled from MCP reads) | `audit_report.md` (Jev-ranked priorities) — see `PLAN.md` |
| 9 | `seo_geo.py` | Search Console + citation exports | `seo_geo_report.json`, prioritized CSV, `citation_report.json` |
| 10 | `ad_library_sampler.py` | Sample plan + saved official-MCP JSON results | validated combined sample, snapshot diff, coverage report |

The unified entry point is `jevmax.py`. Example:

```bash
python3 jevmax.py workflow 9 -- search-console exports/search-console.csv \
  --own-domain yourdomain.com --out seo_geo_report.json
```

Every script runs on its included sample file — try any of them as-is.

## Measured cost (demo runs, 2026-09-20)

- Search-term sorting: **~167 tokens/query** → 50k-query report ≈ **~8.4M tokens**
- Brief scoring: ~506 tokens/brief (3 judgments each)
- Fatigue: ~250 tokens/flagged ad, **1 request total** (all flagged ads batched
  into one state per the TypeSafe skill's composition guidance; low-confidence
  calls land in a REVIEW band instead of acting — threshold: `--act-above 0.5`)
- Page match: ~858 tokens/page
- Lead scoring: ~412 tokens/lead
- Ad tagging (MCP route): ~523 tokens/ad (hook + offer, 2 judgments) —
  measured: 4,608 in / 1,667 out for 12 ads in 1 request

Dollar figures: token pricing isn't published in the docs — read spend off the
TypeSafe console (console.typesafe.ai). The 8.4M-token number for a full 50k-row
report is the denominator; the console is the numerator.

## The lessons that cost reruns

1. v1 of the sorter asked 25 identical questions over 25 queries — the model can't
   bind question to data it isn't pointed at, so everything hedged to ~0.55. Every
   question must name its state field (`q3`, `l1`) in backticks. Baked into all
   scripts now.
2. v1 of fatigue.py sent one request per ad. Batching all ads into one state
   (skill guidance: independent questions over the same state run together)
   cut 5 requests to 1 and input tokens from ~2067 to ~1055. Side effect worth
   knowing: confidence values rose sharply (e.g. 0.63 -> 0.90) — the model sees
   the whole portfolio and distributes probability less flatly. Calls stayed
   consistent; the one genuinely ambiguous ad flipped call AND dropped to 0.29
   confidence, which is exactly what the REVIEW band is for.

## Workflows #1/#2 — Meta Ad Library (two verified routes)

**Route A, primary — Meta Ads MCP Server** (`ads_library_search`, already
authenticated). Verified live 2026-09-20: one keyword query ("airpods", US,
ACTIVE) → **6,179 estimated live ads**; one competitor page → 4,500. Each ad
ships page, link title, `ad_delivery_start_time` and snapshot URL — enough
for indexing, `days_running`, and hook/offer tagging.

`mcp_to_raw.py` bridges MCP JSON → `ad_library_scan.py` input.
First MCP-route run: **49 unique ads → 46 tagged** (hook: 30 direct_offer /
16 curiosity_claim; offer: 46 other_product), 3 batched requests. Honest
caveats: MCP listings carry the link **title only** (no body copy, CTA,
domain, or format), so tags lean on titles; and search returns **newest-first
with no cursor**, so the sample window reaches only ~2 days back — survival
read 0% for exactly that reason, not because no ads survive.

**Route B, fallback — browser session** (`ad_library_raw.json`,
`ad_library_tagged.csv`, n=61 construction-software ads): anonymous scrape
captures full body copy, CTA and domain. Use it when you need hook tagging
beyond titles; snapshot-page fetch per ad is the enrichment path on Route A.

Survival (#2) on the MCP route is longitudinal, and `survival.py` is the
machinery: after each scan day, run the MCP searches, save the JSON, then
`python3 survival.py snapshot <json...>` and check
`python3 survival.py report --tags ad_library_mcp_tagged.csv`. Baseline
seeded **2026-09-20** (n=49) — first survival number readable **2026-11-19**.
`python3 survival.py selftest` verifies the math (it caught my own off-by-one
on the 60-day boundary twice, which is why it exists). The official Ad
Library API's deep pagination remains the one-shot alternative to the tail.
Demo-grade either way — survival ≠ performance, budgets keep weak ads alive.

### Bounded multi-query sampling

`ad_library_sample_plan.json` defines eight AirPods-category queries at the
official tool's 50-result maximum. `ad_library_sampler.py` validates the plan,
combines saved MCP JSON arrays, deduplicates IDs, records overlap, and diffs
snapshots. Its reports explicitly say this is **bounded sampling**, not a
whole-library census. The local regression currently combines 99 input rows into
74 unique ads; 25 were duplicates.

Important commands:

```bash
python3 ad_library_sampler.py plan --plan ad_library_sample_plan.json
python3 ad_library_sampler.py combine INPUT.json... --plan ad_library_sample_plan.json --out sample.json
python3 ad_library_sampler.py diff baseline.json current.json
python3 ad_library_sampler.py report sample.json --tags ad_library_mcp_tagged.csv
```

## SEO/GEO workflows

`seo_geo.py` works from exports, so it never needs account credentials:

```bash
python3 seo_geo.py search-console SearchConsole.csv --own-domain yourdomain.com
python3 seo_geo.py citations citations.csv --own-domain yourdomain.com
```

The Search Console route prioritizes queries by impressions, position, current
CTR, and a rough expected-CTR curve, then proposes reviewable title/meta,
quick-win, refresh, or monitor actions. The citation route measures own-domain
citation rate, brand mention rate, average cited rank, and per-engine gaps.

The bundled sample reports are fixtures, not production claims.

## Benchmark and dashboard

```bash
python3 benchmark.py --min-pass-rate 0.99
python3 dashboard.py --out dashboard.html
```

Current offline regression: **36/36 cases passed**. This is regression evidence
against recorded fixtures, not a blind holdout. `dashboard.html` shows workflow
status, benchmark results, AirPods hook/offer mix, SEO/GEO sample findings,
account read-only state, snapshots, and the claims that remain intentionally
unverified.

## Not production-verified yet (needs you)

- **Real data** — every workflow above ran on demo/sample data. Drop in a real
  Google Ads search-terms CSV and the negatives land the same night, as
  advertised.
- **Production Search Console/citation exports** — the SEO/GEO workflows are
  sample-verified only.
- **60 days** — longitudinal survival begins producing trustworthy 60-day reads
  after the baseline has aged.

Do not publicly claim 30x, 90%, “whole Ad Library,” or production ROAS lift
until the benchmark has a defined baseline, blind test set, runtime logs, and
measured dollar cost.
