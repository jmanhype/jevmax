# Gate results — 2026-09-23 (live runs, TYPESAFE_API_KEY transient)

All four gates from GATE_REPORT.md ran live. Key used once via env, never stored.

## 1. episodes — vertical-9x16/episode-map.csv (advance 2)
| ep | total | hook | cliff | cheap | gate |
|----|-------|------|-------|-------|------|
| 1 | 10.08 | 3.11 | 3.29 | 3.68 | ADVANCE |
| 4 | 9.92 | 2.57 | 3.46 | 3.89 | ADVANCE |
| 2 | 9.07 | 2.29 | 3.24 | 3.54 | HOLD |
| 3 | 8.56 | 2.43 | 3.19 | 2.94 | HOLD |
Output: `vertical-9x16/ranked_episodes.csv`. ~2.2k in / 188 out tokens.

## 2. rank — film-16x9/opening-hooks.csv (advance 1)
| hook | total | hook | era | engine | gate |
|------|-------|------|-----|--------|------|
| C: Two Empires | 6.85 | 1.76 | 2.31 | 2.78 | ADVANCE |
| A: The Call | 5.99 | 2.11 | 2.40 | 1.48 | HOLD |
| B: The Inspection | 5.90 | 1.64 | 2.02 | 2.24 | HOLD |
Output: `film-16x9/ranked_hooks.csv`. ~1.7k in / 142 out tokens.
Note: gate overturned the writer's pick (A). A had the strongest hook image (2.11) but the weakest engine (1.48). The beat sheet was written for A — rewriting it for C needs a human go-ahead.

## 3. canon — identity_lock.yaml vs vertical-9x16/episode-01-cold-open.md
8/8 auto-PASS (0.99–1.00). Olive ribbon not mentioned in script (free check — fine, it's soft-visible canon).
Output: `vertical-9x16/canon_report_ep01.json`.

## 4. canon — identity_lock.yaml vs film-16x9/beat-sheet.md
7 PASS, 1 REVIEW: **red pencil — consistent at 0.77** (under the 0.80 auto-accept line). It appears once in the canon header, never in beat action. Judgment is "consistent", not "contradicts" — thin usage, not a defect. Human call: accept as-is or work it into a beat.
Sky-blue piping not mentioned in script (free check — fine).
Output: `film-16x9/canon_report_beatsheet.json`.

## Context note
Commit 02d8617 (other session) already made the format call: **vertical short-drama 12×110s**, with its own gated 12-episode map (eps 1–9 ADVANCE) and story bible. That sprint's lore engine (frequency 14, American mayday, SEVEN-THREE, father tape) differs from this sprint's (dead jack, "do not answer", tomorrow's log, heartbeat lamp). Choosing between the two engines is a human creative call — the gates can't make it.
