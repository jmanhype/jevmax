#!/usr/bin/env python3
"""Generate preflighted pvx queue command files for comedy boards and videos."""

from __future__ import annotations

import argparse
import json
import shlex
from pathlib import Path


def shell_quote(value: str) -> str:
    return shlex.quote(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--stage", choices=("boards", "videos"), required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--pvx", default="/Users/batmanosama/.codex/plugins/cache/openai-curated-remote/pixverse/1.3.0/scripts/pvx")
    args = parser.parse_args()
    pvx = shell_quote(args.pvx)

    if args.stage == "boards":
        manifest = json.loads((args.run / "boards" / "manifest.json").read_text(encoding="utf-8"))
        rows = manifest["boards"]
        queue = args.run / "boards" / "queue.json"
        output = args.run / "boards" / "queue-commands.sh"
        lines = ["#!/bin/sh", "set -eu"]
        for index, row in enumerate(rows):
            operation = "queue write" if index == 0 else "queue append"
            force = " --force" if index == 0 else ""
            lines.append(
                f'{pvx} {operation}{force} {shell_quote(str(queue))} '
                f'--project {shell_quote(args.project)} --id {shell_quote("board_" + row["candidate_id"])} '
                f'--label {shell_quote("Comedy board " + row["candidate_id"])} --preflight --format markdown -- '
                f'pixverse create image --model gpt-image-2.5-sunburst --quality 1440p --detail-level high '
                f'--aspect-ratio 9:16 --prompt {shell_quote(row["prompt_path"])}'
            )
        lines.append(f'{pvx} quote queue {shell_quote(str(queue))} --format markdown')
    else:
        plan = json.loads((args.run / "render" / "plan.json").read_text(encoding="utf-8"))
        rows = plan["videos"]
        queue = args.run / "render" / "queue.json"
        output = args.run / "render" / "queue-commands.sh"
        lines = ["#!/bin/sh", "set -eu"]
        for index, row in enumerate(rows):
            operation = "queue write" if index == 0 else "queue append"
            force = " --force" if index == 0 else ""
            lines.append(
                f'{pvx} {operation}{force} {shell_quote(str(queue))} '
                f'--project {shell_quote(args.project)} --id {shell_quote("video_" + row["candidate_id"])} '
                f'--label {shell_quote("Comedy V6 " + row["candidate_id"])} --preflight --format markdown -- '
                f'pixverse create video --model v6 --quality 720p --duration 5 --aspect-ratio 9:16 '
                f'--seed 0 --no-audio --image {shell_quote(row["board_local_path"])} '
                f'--prompt {shell_quote(row["prompt_path"])}'
            )
        lines.append(f'{pvx} quote queue {shell_quote(str(queue))} --format markdown')

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    output.chmod(0o755)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
