# Jevmax Build Log

This is the implementation history behind [`workflow.md`](../workflow.md): from
"what is this MCP thing" to a pushed, cloned, self-running system. It records
the order in which capabilities were proven and links each step to the durable
artifact in this repository.

The operating invariant was the same at every layer: **prove one real, measured
unit before scaling it.**

## Phase 1 — Verify the foundation (Meta)

1. Catalogued all 95 `mcp__meta-ads__` tools and called the lightest one,
   `ads_get_ad_accounts`, first.
2. Established the OAuth protocol: login windows belonged to the operator, not
   the agent. The operator completed consent; the agent retried afterward.
3. Probed gated scopes instead of assuming access:
   - Pixel: available
   - Pages: available
   - Instagram: empty
   - Account `49852068`: confirmed

## Phase 2 — Wire the judgment engine (TypeSafe)

4. Put `TYPESAFE_API_KEY` in `.env`; it was never committed to repository code.
5. Built [`typesafe.py`](../typesafe.py), a standard-library-only client with:
   - `ask(state, questions)` and batch support
   - 429/529 retries
   - printed input/output token costs on every call

No workflow shipped with asserted economics. Token cost had to be measured.

## Phase 3 — Pipeline A (intelligence)

### Live-market input

6. Tested the Meta Ad Library route through `ads_library_search`, including
   both keyword and page scans.
7. Learned and recorded the hard limit: results were newest-first, roughly two
   days deep, and had no useful pagination into history.
8. Built [`ad_library_scan.py`](../ad_library_scan.py) to pull ads and ask Jev
   to tag each ad by hook, proof, and offer while computing days running.
9. Built [`mcp_to_raw.py`](../mcp_to_raw.py) to normalize MCP dumps.
10. Produced the first 74-ad tagged output in
    [`ad_library_mcp_tagged.csv`](../ad_library_mcp_tagged.csv).

### Longitudinal survival

11. Built [`survival.py`](../survival.py) so the shallow Ad Library view could
    still support longitudinal analysis:
    - snapshot the set of live ad IDs every scan day
    - later report what percentage of a 60-day-old baseline remains alive
    - selftest the survival logic
12. Seeded the first baseline on 2026-09-20 in
    [`snapshots/2026-09-20.json`](../snapshots/2026-09-20.json).
13. Automated scans, snapshots, reports, and notification with a Monday 08:00
    cron. Tagging was deliberately not forced during unattended scans.

### Account audit

14. Built [`audit.py`](../audit.py) with deterministic checks plus Jev ranking.
15. The first real audit found a 2022 $5/day zombie boost that was still
    spending. Both dead campaigns were paused with `ads_update_entity`.
16. Preserved the first audited output in
    [`audit_report.md`](../audit_report.md).

## Phase 4 — Pipeline B (creative)

17. Defined the `jevmax-creative-v2` schema in
    [`creative/persona-ava.json`](../creative/persona-ava.json):
    - the character block is **verbatim-frozen**
    - scene, wardrobe, pose, and camera remain variable
    - plain lists are compositional and appear together
    - `*_options` fields are alternatives and expand cartesian-style
    - the distinction was caught before a render batch manufactured nonsense
18. Built [`flatten.py`](../flatten.py) to expand specs into painter paragraphs
    and a manifest.
19. Built [`score_briefs.py`](../score_briefs.py) as a gate to rank concepts
    before spending render credits.
20. Built [`pixverse.py`](../pixverse.py) to generate one kit per variant:
    seed prompt, video direction, and a TTS hook-line slot.

## Phase 5 — Make rendering real (PixVerse)

21. Installed the PixVerse CLI globally with `npm install -g pixverse`.
22. Verified Node 22 and the agent-operable CLI contract:
    - prompts accept file paths
    - JSON output is supported
    - exit codes are deterministic
23. Completed PixVerse OAuth through device flow; the operator completed the
    browser login. The account was Pro with 12,150 credits.
24. Discovered that the later API key used a separate wallet: authentication
    succeeded at zero credits. The CLI remained the render channel, while the
    key stayed in `.env` for the product path.
25. Rendered the seed still from
    [`creative/pixverse/V001.seed.txt`](../creative/pixverse/V001.seed.txt)
    with Nano Banana 2 for 25 credits, producing
    [`creative/renders/ava-01_seed.png`](../creative/renders/ava-01_seed.png).
26. QA'd the seed against the frozen character specification.
27. Rendered [`creative/pixverse/V001.mp4`](../creative/pixverse/V001.mp4)
    specifically to price a 5-second video: 50 credits. Frame-by-frame review
    confirmed identity held.
28. Built [`render_videos.py`](../render_videos.py) as a manifest-driven batch
    runner:
    - every variant uses the same approved seed
    - failures are tolerated without stopping the batch
    - every result is logged to
      [`creative/pixverse/render_log.csv`](../creative/pixverse/render_log.csv)
29. Ran the eight expansions. One content-filter failure was retried once.
    Result: nine rendered videos on disk — V001 plus V002-E01 through E08 —
    for 475 credits total.

## Phase 6 — Close the input gaps (computer use)

30. Located the real "Lost Future Style Catalog" conversation in Chrome.
31. Extracted its output grammar — style families, titles, taglines, prompt and
    negative-prompt pairs — into
    [`creative/lost_future_example.md`](../creative/lost_future_example.md),
    including its mapping to the creative schema. That unblocked Layer 1.
32. Verified that the expected Google Ads search-terms CSV did not exist:
    there was no connected account and no export. The gap was reported honestly
    instead of being filled with fabricated data.
33. Reviewed the cron prompt and deliberately kept it unchanged.

## Phase 7 — Make it durable and shareable

34. Wrote the complete system description in
    [`workflow.md`](../workflow.md).
35. Secret-scanned the repository.
36. Initialized Git, committed, and pushed to the private repository
    `github.com/jmanhype/jevmax`.
37. Cloned it back to `/Users/batmanosama/jevmax`, proving that the pushed tree
    contained the runnable system.

## Pattern

Every layer proved itself with one real, measured unit before scaling:

- one OAuth-backed account check
- one tagged ad
- one survival snapshot
- one audit finding
- one frozen-character seed
- one priced video
- then the batch

The resulting system is not an execution autopilot. It is an intelligence and
production-control layer: market survival data enters, judgment-grade decisions
are produced, creative variants are constrained and priced, and every scaling
step follows a proven unit.

## Post-build live rerun — 2026-09-20

The first end-to-end rerun after cloning is recorded in
[`runs/2026-09-20/RUN_REPORT.md`](../runs/2026-09-20/RUN_REPORT.md). It
reconnected to the official Meta Ads MCP endpoint, ran a live read-only top-50
AirPods scan, merged 103 unique IDs into the daily snapshot, refreshed the
account audit, regenerated the creative prompts and kits, verified the existing
render inventory, and spent zero PixVerse credits.
