# Growth Loop measured dogfood evidence

Verification date: **2026-09-21**

Dogfood case: **AirPods / United States / Meta Ad Library bounded sample**

## Evidence summary

| Claim | Measured result | Source |
|---|---|---|
| Longitudinal baseline | 103 unique ad IDs in one JSON snapshot | `snapshots/2026-09-20.json` |
| Snapshot integrity | SHA-256 `afec580b80129d2b5e375e710d9903f3cc29b4e915f5df5844daeb2194775e09` | `runs/2026-09-20/RUN_REPORT.md` and independent OpenSSL check |
| Current bounded scan | 50 returned ads from an estimated 6,792 | `runs/2026-09-20/airpods_scan_report.json` |
| Comparable-sample difference | 74 baseline IDs, 50 current IDs, 21 retained, 29 current-only, 53 absent | `runs/2026-09-20/airpods_scan_diff.json` |
| Observed bounded overlap | 28.38%; explicitly not survival | `runs/2026-09-20/airpods_scan_diff.json` |
| First valid survival read | 2026-11-19, only if a comparable snapshot is taken on or after that date | `runs/2026-09-20/RUN_REPORT.md` |
| Active weekly automation | ACTIVE, Mondays at 08:00, top-50 read-only scan | `AUTOMATION_EVIDENCE.md` |
| Account audit | 3 findings; read-only refresh, no campaign change | `runs/2026-09-20/audit_report.md` |
| Offline QA | 36 / 36 passed, 100%, PASS | `benchmark_report.md` and 2026-09-21 rerun |

## Snapshot and survival evidence

The dogfood baseline is a JSON array of 103 unique live ad IDs. `jq` reported
the array length as 103, and `openssl dgst -sha256` independently reproduced the
recorded hash:

```text
SHA2-256(snapshots/2026-09-20.json)= afec580b80129d2b5e375e710d9903f3cc29b4e915f5df5844daeb2194775e09
```

The baseline and current observation are same-day. Therefore no 60-day survival
rate exists yet. The first valid 60-day read for this baseline is
**2026-11-19**. A later read must also use a comparable scan plan and state its
bounded coverage before any survival number is reported.

The 28.38% retention figure means only that 21 IDs appeared in both bounded
samples. It is not 60-day survival, not ad death evidence for the 53 absent
IDs, and not a performance result.

## Weekly automation evidence

The active local automation definition is:

`/Users/batmanosama/.codex/automations/weekly-airpods-ad-scan/automation.toml`

Inspected facts:

- ID: `weekly-airpods-ad-scan`
- Status: `ACTIVE`
- Cadence: `FREQ=WEEKLY;BYDAY=MO;BYHOUR=8;BYMINUTE=0`
- Query: AirPods, US, ACTIVE, ALL, limit 50
- Safety: report inline; do not create, edit, archive, pause, or delete ads
- Failure rule: report the exact blocker rather than guessing or fabricating

Automation limitation: the prompt compares against a 49-row baseline at
`/Users/batmanosama/.zcode/workspace/default/jevmax/ad_library_mcp_tagged.csv`
and does not explicitly instruct the automation to persist a dated unique-ID
snapshot. The repo's stronger Growth Loop contract therefore requires an
operator update to the automation prompt before claiming fully automated
longitudinal snapshot collection. The 103-ID snapshot and the weekly scan state
are verified separately by this evidence.

No automation file was modified while building this package.

## Monthly cadence evidence

The reusable monthly cadence is defined in `TEMPLATE.md`: review four or more
dated weekly observations, refresh the read-only account audit, test 60-day
eligibility, review actual creative and measurement signals, and route an
approved refresh to Creative Test Sprint.

The dogfood evidence verifies the inputs and first cycle state, not a completed
monthly review. No monthly survival or performance result is claimed.

## Measured cost

| Item | Measured value |
|---|---:|
| Package assembly generation tasks | 0 |
| Package assembly PixVerse credits | 0 |
| Package assembly Meta API calls | 0 |
| Source 2026-09-20 PixVerse credits | 0 |
| Source 2026-09-20 TypeSafe input tokens | 2,363 |
| Source 2026-09-20 TypeSafe output tokens | 265 |
| Source 2026-09-20 TypeSafe total tokens | 2,628 |
| Source run live ad changes | 0 |

The source run's 2,628 judgment tokens covered account-audit ranking and a
three-concept brief gate. Its Ad Library and account work was read-only. The
offline benchmark makes no TypeSafe API calls.

Default Growth Loop operation adds no creative generation cost. Any bounded
tagging pass or refresh generation needs a separate approved token or credit
budget. Free GPT Image 2.5 and the 40-credit V6 720p no-audio route remain
subject to the studio policy; all other paid or premium generation requires
explicit operator approval.

## QA verification

Commands and checks used on 2026-09-21:

| Check | Result |
|---|---|
| `jq 'length' snapshots/2026-09-20.json` | 103 |
| `openssl dgst -sha256 snapshots/2026-09-20.json` | Matches recorded hash |
| `python3 benchmark.py --min-pass-rate 0.99` | PASS, 36 / 36, 100% |
| JSON parse of `MANIFEST.json` | Pass |
| Manifest path resolution from the product directory | Pass |
| Automation config inspection | Read-only pass |

The offline regression is recorded-fixture regression, not a blind holdout. It
verifies intended workflow semantics and the survival boundary logic; it does
not establish market performance.

## Bounded-sample limitations

1. The official scan returned 50 ads while estimating 6,792 total results.
2. Only 21 of the 50 returned ads were tagged. The other 29 current-only rows
   were left untagged rather than scaling judgment calls without approval.
3. Hook and offer summaries therefore describe tagged rows only: direct offer
   14, curiosity claim 5, untagged 2; other product 19, untagged 2.
4. The newest-first, no-cursor interface limits visible history. Absence from
   one top-50 result is not evidence that an ad stopped running.
5. The active automation still references the older 49-row `.zcode` baseline
   and needs the snapshot-persistence update described above.
6. No whole-library coverage, ROAS, production lift, blind holdout, or
   profitability claim is supported by this evidence.

## Read-only account findings

The 2026-09-20 audit found:

1. Pixel `117869962136376` was active but had never fired.
2. No Instagram account was linked.
3. The Jay Guthrie Airpods Page had not accepted lead-generation terms.

Both 2022 campaigns were paused. The audit made no campaign or ad change. These
are launch-readiness findings, not measurements of creative performance.
