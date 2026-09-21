# Comedy Test Sprint

Internal upgrade to Creative Test Sprint.

## Pipeline

```text
120 premises
six personas x 20
→ deterministic product/safety filters
→ Jev tournament 1: 24 survivors
→ persona-specific mutation
→ Jev tournament 2: 8 finalists
→ 8 free GPT Image 2.5 Sunburst boards
→ at most 2 V6 720p no-audio videos
→ technical QA + human review
```

## Commands

```bash
RUN=studio/comedy/runs/<sprint-id>
BRIEF=studio/comedy/briefs/airpods-wired-2026-09-21.json

python3 studio/comedy/comedy_sprint.py generate --brief "$BRIEF" --output "$RUN"
python3 studio/comedy/comedy_sprint.py filter --output "$RUN"
python3 studio/comedy/comedy_sprint.py tournament --output "$RUN" --round 1
python3 studio/comedy/comedy_sprint.py mutate --output "$RUN"
python3 studio/comedy/comedy_sprint.py tournament --output "$RUN" --round 2
python3 studio/comedy/comedy_sprint.py boards --output "$RUN"
python3 studio/comedy/comedy_sprint.py report --output "$RUN"
python3 studio/comedy/validate_run.py "$RUN"
```

Offline structure test:

```bash
python3 studio/comedy/comedy_sprint.py selftest
```

## Production policy

- Boards: GPT Image 2.5 Sunburst, 1440p, high detail, 9:16, current free promotion.
- Videos: V6, 720p, five seconds, no audio, at most two.
- No MiniMax, Seedance, or other premium video route.
- No live ad change.
- No humor-performance or ROAS claim.

## Current live-run status

The AirPods run has:

- 120 generated premises
- six personas x 20
- deterministic filter evidence

The real TypeSafe tournament is not recorded because DNS resolution for
`api.typesafe.ai` has failed repeatedly; the live run status records the exact
attempt count and preserves the filtered input. No local/mock scores are used
as live Jev evidence.
