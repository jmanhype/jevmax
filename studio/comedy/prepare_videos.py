#!/usr/bin/env python3
"""Prepare at most two V6 video prompts from successful free finalist boards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--count", type=int, choices=(1, 2), default=2)
    args = parser.parse_args()

    boards = json.loads((args.run / "boards" / "manifest.json").read_text(encoding="utf-8"))
    successful = [row for row in boards.get("boards", []) if row.get("status") == "success" and row.get("local_path")]
    selected = successful[: args.count]
    if not selected:
        raise SystemExit("No successful board image available for V6 video preparation")
    prompts = args.run / "render" / "prompts"
    prompts.mkdir(parents=True, exist_ok=True)
    planned = []
    for board in selected:
        prompt_path = prompts / f"{board['candidate_id']}.video.txt"
        prompt_path.write_text(
            "Animate this exact product-only visual comedy board as one continuous five-second "
            "vertical object scene. Preserve the board composition, unbranded white wired earbuds, "
            "cable shape, props, colors, and comedic staging. Use only small, legible object motion "
            "that makes the visual joke clearer. Keep the product central and sharp. No people, no "
            "scene cut, no text, no captions, no logo, no UI overlay, no extra products, and no "
            "style shift. Audio plan: none; the render command disables audio.\n",
            encoding="utf-8",
        )
        planned.append(
            {
                "candidate_id": board["candidate_id"],
                "board_task_id": board["task_id"],
                "board_local_path": board["local_path"],
                "prompt_path": str(prompt_path),
                "model": "v6",
                "quality": "720p",
                "duration": "5",
                "aspect_ratio": "9:16",
                "audio": "disabled",
            }
        )
    output = {
        "policy": "at most two V6 720p five-second no-audio videos",
        "planned_count": len(planned),
        "videos": planned,
    }
    (args.run / "render" / "plan.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Prepared {len(planned)} V6 video prompt(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
