# Category Signal Audit — Measured Dogfood Evidence

## Live bounded scan

Query:

```text
search_terms=AirPods
countries=US
ad_active_status=ACTIVE
ad_type=ALL
limit=50
```

Measured result:

- Estimated total active ads: **6,792**
- Returned ads: **50**
- Current-only IDs versus prior 74-ID bounded sample: **29**
- Overlap with prior bounded sample: **21**
- Prior-baseline IDs absent from this top-50 result: **53**

This absence is not evidence that an ad stopped running; the interface is
newest-first and bounded.

## Signal

From the current scan report:

- unique ads: **50**
- tagged ads: **21**
- top advertiser: VOLTA Charger, 5 ads
- hook mix:
  - direct offer: 14
  - curiosity claim: 5
  - untagged: 2
- offer mix:
  - other product: 19
  - untagged: 2

## Snapshot

The same-day snapshot contains **103 unique live IDs**.

- Snapshot: `/Users/batmanosama/jevmax/snapshots/2026-09-20.json`
- SHA-256: `afec580b80129d2b5e375e710d9903f3cc29b4e915f5df5844daeb2194775e09`
- First valid 60-day survival read: **2026-11-19**

## Account audit

Live read-only account state found:

- account active and queryable
- both 2022 campaigns paused
- pixel active but never fired
- Instagram account not linked
- lead-gen ToS not accepted

The final Jev-ranked audit contains three findings.

## Measured cost

- New render credits for package assembly: **0**
- Account audit judgment: **1,005 input / 114 output tokens**
- Meta Ad Library and account calls: read-only
- Live ad changes: **0**

## QA

- Saved raw scan exists
- Saved scan report exists
- Saved diff exists
- Saved audit report exists
- Account snapshot exists
- Snapshot JSON parses and contains 103 IDs
- Bounded-sample limitation is explicit
- Same-day survival limitation is explicit

## Limitations

- The Ad Library tool exposes a bounded, newest-first sample.
- Current-only ads were not tagged because that would require additional token spend.
- Survival is not yet measurable until the baseline is at least 60 days old.
- No ROAS, conversion lift, or production performance claim is made.
