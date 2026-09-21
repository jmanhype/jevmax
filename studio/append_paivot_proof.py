#!/usr/bin/env python3
"""Append a prepared proof block to a Paivot/nd story."""

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("story_id")
    parser.add_argument("proof_path", type=Path)
    args = parser.parse_args()
    text = args.proof_path.read_text(encoding="utf-8")
    subprocess.run(
        ["pvg", "nd", "update", args.story_id, "--append-notes", text],
        check=True,
    )


if __name__ == "__main__":
    main()
