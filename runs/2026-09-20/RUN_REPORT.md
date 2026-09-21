# Jevmax live run report — 2026-09-20

This run followed the build-log sequence, not only the offline regression suite.
It used live read-only Meta Ads MCP calls, live TypeSafe judgment calls, local
creative generation, and artifact verification. It made **no live ad changes**
and spent **zero PixVerse credits**.

## Connection status

- Official Meta Ads MCP endpoint: `https://mcp.facebook.com/ads`
- Local Codex configuration name: `facebook-ads`
- Connection result: `Meta Ads MCP Server 1.0.0`
- Exposed tools: **95**
- Account verified: `49852068`
- Account status: `ACTIVE`, queryable, payment method present

The server was configured but not injected into the conversation's normal tool
surface. The run therefore connected through the existing local OAuth helper and
the MCP streamable-HTTP protocol using [meta_mcp_call.py](meta_mcp_call.py).
The helper was read at runtime; no credential was embedded or printed.

## Pipeline A — live market intelligence

### Official Ad Library scan

Command parameters:

- search term: `AirPods`
- country: `US`
- status: `ACTIVE`
- type: `ALL`
- limit: `50`

Measured result:

- Estimated total ads: **6,792**
- Returned ads: **50**
- Raw scan: [ad_library_airpods_mcp.json](ad_library_airpods_mcp.json)
- Scan report: [airpods_scan_report.json](airpods_scan_report.json)
- Baseline diff: [airpods_scan_diff.json](airpods_scan_diff.json)

Compared with the saved 74-ID bounded sample:

- baseline IDs: **74**
- current IDs: **50**
- overlap: **21**
- current-only IDs: **29**
- baseline IDs absent from this bounded top-50 result: **53**
- observed bounded-sample overlap: **28.38%**

This is **not survival**. The newest-first, no-cursor interface and different
query coverage make absence from one top-50 result insufficient evidence that an
ad stopped running.

### Current sample signal

Only IDs already present in the tagged baseline were joined to tags; this run did
not spend tokens tagging the 29 new ads.

- Tagged IDs in current result: **21 / 50**
- Hook mix among tagged IDs:
  - direct offer: 14
  - curiosity claim: 5
  - untagged: 2
- Offer mix among tagged IDs:
  - other product: 19
  - untagged: 2
- Top current advertisers:
  - VOLTA Charger: 5
  - Kure for Hypnotherapy: 4
  - J7506v-en.myshopify.com: 3
  - Heddz.co: 3

### Longitudinal snapshot

The live top-50 result was merged into the same-day snapshot. The snapshot now
contains **103 unique live IDs**.

- Snapshot: `/Users/batmanosama/jevmax/snapshots/2026-09-20.json`
- SHA-256: `afec580b80129d2b5e375e710d9903f3cc29b4e915f5df5844daeb2194775e09`
- First valid 60-day survival read: **2026-11-19**

The live MCP response exposed an input-shape mismatch: `ads_library_search` now
returns an object containing an `ads` array, while `survival.py` previously
accepted only the raw array. `survival.py` now accepts both shapes, and its
selftest still passes.

## Pipeline A′ — live account audit

Read-only calls refreshed account, campaign, Page, Instagram, and dataset state.

- Both 2022 campaigns are now **PAUSED**.
- Pixel `117869962136376` is active but has never fired; Meta reports the
  epoch sentinel `1969-12-31` as its last-fired time.
- Page `Jay Guthrie Airpods` has not accepted lead-gen ToS.
- No Instagram account is linked.
- No campaign or ad was created, edited, paused, resumed, or deleted in this run.

Artifacts:

- Live assembled snapshot: [account_snapshot_live.json](account_snapshot_live.json)
- Jev-ranked report: [audit_report.md](audit_report.md)

The final audit contains three findings: dead conversion tracking, missing
Instagram linkage, and unaccepted lead-gen ToS. Campaign findings are gone
because both campaigns are paused.

## TypeSafe judgment engine

Two live judgment runs completed:

| Run | Usage |
|---|---:|
| Account audit ranking | 1,005 input / 114 output tokens |
| Brief gate over 3 concepts | 1,358 input / 151 output tokens |
| **Total** | **2,363 input / 265 output = 2,628 tokens** |

Brief-gate ranking:

1. `9.74` — six-hours-per-week status-meeting pain
2. `8.86` — founder insight / pain mirroring
3. `0.48` — vague AI hype

Artifact: [ranked_briefs.csv](ranked_briefs.csv)

## Pipeline B — creative generation and render gate

The schema expansion regenerated:

- 8 painter-ready prompts
- 8 PixVerse kits
- 8 seed prompt files
- 8 video-direction files
- 2 manifests

Every generated V002 prompt is byte-identical to the approved baseline prompt.
Every generated seed/direction text is byte-identical to its existing kit. This
confirms deterministic generation from the frozen spec.

- Generated prompts: [flatten/](flatten/)
- Generated kits: [pixverse-kits/](pixverse-kits/)
- Prompt bundle SHA-256: `39e250e05984cb1dc46935c60f0742fc61dbb98bd6c185b403a2b9be047615b0`
- Kit bundle SHA-256: `0737394601071ba16df9bf55c2e0b78b211b24e5b08739df0f8d76ef8b2f9168`

`render_videos.py --dry-run` resolved all eight V002 variants:

`V002-E01` through `V002-E08`

No render was launched, so no credits were spent.

## Existing render inventory

- Approved seed image: 1
- Rendered videos: **9**
- Video bundle SHA-256 across all nine files:
  `486321a6c2cda22c84b60e7b7cff9aa5d38ba830d7892235cae9df0a9ca0f1b3`
- Seed SHA-256:
  `3acc728cbe8bd2e252f6f5459c3f2c5ec08984de75286bad0a2f71303815d0f9`

## PixVerse status

- CLI version: `1.4.5`
- Account tier: Pro
- Current total credits: **11,675**
- Credits spent in this run: **0**

The existing render log records eight completed expansion videos at 400 credits.
The first V001 video and seed account for the previously measured full 475-credit
batch total.

## Validation

- `python3 -m py_compile survival.py runs/2026-09-20/meta_mcp_call.py`: PASS
- `python3 survival.py selftest`: PASS
- `python3 jevmax.py selftest`: PASS, 10 stages
- Offline regression: **36/36 passed**, 100%
- `git diff --check`: clean at report creation time

## Honest limits

1. The 50-result Ad Library call is a bounded sample, not a census.
2. Bounded-sample overlap is not survival.
3. The baseline is same-day; no 60-day survival number exists yet.
4. New current-only ads were not tagged, to avoid unmeasured token scaling.
5. No new creative render was launched.
6. This run made no Meta write call and no live ad change.
