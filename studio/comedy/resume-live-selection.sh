#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
cd "$ROOT"

RUN="studio/comedy/runs/airpods-wired-2026-09-21"
BRIEF="studio/comedy/briefs/airpods-wired-2026-09-21.json"

printf '%s\n' "==> Jevmax Comedy Test Sprint: live selection resume"
printf '%s\n' "Run: $RUN"
printf '%s\n' "This script invokes TypeSafe/Jev and creates board prompts."
printf '%s\n' "It does not submit PixVerse image or video generation."
printf '%s\n' ""

if [ ! -f "$RUN/premises.filtered.csv" ]; then
  python3 studio/comedy/comedy_sprint.py generate \
    --brief "$BRIEF" \
    --output "$RUN"
  python3 studio/comedy/comedy_sprint.py filter --output "$RUN"
fi

if [ ! -f "$RUN/round1.survivors.csv" ]; then
  python3 studio/comedy/comedy_sprint.py tournament --output "$RUN" --round 1
fi

if [ ! -f "$RUN/round1.mutated.csv" ]; then
  python3 studio/comedy/comedy_sprint.py mutate --output "$RUN"
fi

if [ ! -f "$RUN/round2.finalists.csv" ]; then
  python3 studio/comedy/comedy_sprint.py tournament --output "$RUN" --round 2
fi

if [ ! -f "$RUN/boards/manifest.json" ]; then
  python3 studio/comedy/comedy_sprint.py boards --output "$RUN"
fi

python3 studio/comedy/comedy_sprint.py report --output "$RUN"
python3 studio/comedy/build_pixverse_commands.py \
  --run "$RUN" \
  --stage boards \
  --project jevmax-comedy-airpods-boards

python3 studio/comedy/validate_run.py "$RUN"

printf '\n%s\n' "==> Selection complete"
printf '%s\n' "Review: $RUN/REPORT.md"
printf '%s\n' "Board commands: $RUN/boards/queue-commands.sh"
printf '%s\n' "No image or video generation has been submitted."
