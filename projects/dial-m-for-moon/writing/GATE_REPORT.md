# DIAL M FOR MOON — writing-sprint gate report (2026-09-23)

All four gates attempted. **Every Jev-backed gate is PENDING-KEY** — see failure mode below. No scores were invented; all gate inputs are written and ready to run. Deterministic checks (CSV parse, column resolution) pass.

## Failure mode (verified live)
`TYPESAFE_API_KEY` is not set in this environment (no env var, no `.env` under `~`, `~/workspace`, or `~/workspace/jevmax`). `typesafe.py:load_key()` raises:
`RuntimeError: TYPESAFE_API_KEY not found (env var or .env file)`
`drama_gate.py selftest` passes (no API calls) — the runner is healthy; only the key is missing.

## Gate inputs (ready)
- `writing/vertical-9x16/episode-map.csv` — 4 episode candidates (episode,title,beat,cliffhanger)
- `writing/film-16x9/opening-hooks.csv` — 3 hook variants (title,tagline,concept)
- `writing/vertical-9x16/episode-01-cold-open.md` — EP001 cold-open script (canon subject)
- `writing/film-16x9/beat-sheet.md` — beat sheet for Hook A (canon subject)
- Canon entities: `Valentina Orlova;Valya;headset;red pencil;olive ribbon;sky-blue piping;switchboard;Object 10-D;lunar listening post`

## Commands (run from ~/workspace/jevmax, with TYPESAFE_API_KEY set)

```bash
cd ~/workspace/jevmax
export TYPESAFE_API_KEY="<key>"   # or place TYPESAFE_API_KEY=<key> in .env

# 1. Episodes gate — advance top 2-3 to the shot budget
python3 drama_gate.py episodes projects/dial-m-for-moon/writing/vertical-9x16/episode-map.csv --advance 2 --out projects/dial-m-for-moon/writing/vertical-9x16/ranked_episodes.csv

# 2. Rank gate — 3 film opening hooks
python3 drama_gate.py rank projects/dial-m-for-moon/writing/film-16x9/opening-hooks.csv --advance 1 --out projects/dial-m-for-moon/writing/film-16x9/ranked_hooks.csv

# 3. Canon gate — EP001 cold open vs identity lock
python3 drama_gate.py canon projects/dial-m-for-moon/bibles/valentina-orlova/identity_lock.yaml projects/dial-m-for-moon/writing/vertical-9x16/episode-01-cold-open.md --entities "Valentina Orlova;Valya;headset;red pencil;olive ribbon;sky-blue piping;switchboard;Object 10-D;lunar listening post" --out projects/dial-m-for-moon/writing/vertical-9x16/canon_report_ep01.json

# 4. Canon gate — beat sheet vs identity lock
python3 drama_gate.py canon projects/dial-m-for-moon/bibles/valentina-orlova/identity_lock.yaml projects/dial-m-for-moon/writing/film-16x9/beat-sheet.md --entities "Valentina Orlova;Valya;headset;red pencil;olive ribbon;sky-blue piping;switchboard;Object 10-D;lunar listening post" --out projects/dial-m-for-moon/writing/film-16x9/canon_report_beatsheet.json
```

## Status per gate
| Gate | Status | Note |
|---|---|---|
| episodes (vertical map) | PENDING-KEY | input ready; `--advance 2` per doctrine (top 2–3 to shot budget) |
| rank (film hooks) | PENDING-KEY | input ready; writer's pick is Hook A, gate to confirm/overturn |
| canon (EP001 script) | PENDING-KEY | all 10 entities mentioned in script (deterministic pass will find them) |
| canon (beat sheet) | PENDING-KEY | all 10 entities mentioned in beat sheet |

## Writer's notes for the human (Jay)
- Hook A was picked for the beat sheet because it continues the already-rendered shot_01 beat directly and is cheapest; if the rank gate prefers B or C, the beat sheet gets rewritten — no sunk cost.
- The EP001 script and beat sheet share lore (dead jack, "Do not answer", tomorrow's log, the heartbeat lamp) so both formats stay one canon.
- Confidence policy applied: no gate ran, so nothing advanced — both hooks remain candidates until the key exists.
