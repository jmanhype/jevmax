#!/usr/bin/env python3
"""Install the vendored skills bundle (skills/) into an agent's skill directory.

Copies every skill folder under skills/ into the target directory, skipping
folders that already contain an identical SKILL.md. Idempotent — safe to rerun
after pulling updates to this repo.

Usage:
    python3 install_skills.py                 # -> ~/.zcode/skills
    python3 install_skills.py --agent claude  # -> ~/.claude/skills
    python3 install_skills.py --agent codex   # -> ~/.agents/skills
    python3 install_skills.py --target C:\\any\\skill\\dir
    python3 install_skills.py --list          # just show what's in the bundle
"""
import argparse
import hashlib
import shutil
import sys
from pathlib import Path

AGENT_DIRS = {
    "zcode": Path.home() / ".zcode" / "skills",
    "claude": Path.home() / ".claude" / "skills",
    "codex": Path.home() / ".agents" / "skills",
}

BUNDLE = Path(__file__).resolve().parent / "skills"


def bundled_skills():
    return sorted(p for p in BUNDLE.iterdir() if (p / "SKILL.md").is_file())


def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", choices=sorted(AGENT_DIRS), default="zcode",
                    help="Which agent's skill directory to target (default: zcode)")
    ap.add_argument("--target", help="Explicit target directory (overrides --agent)")
    ap.add_argument("--list", action="store_true", help="List bundle contents and exit")
    args = ap.parse_args()

    skills = bundled_skills()
    if args.list:
        for s in skills:
            print(f"  {s.name}")
        print(f"{len(skills)} skills in {BUNDLE}")
        return 0

    target = Path(args.target) if args.target else AGENT_DIRS[args.agent]
    target.mkdir(parents=True, exist_ok=True)

    installed = updated = skipped = 0
    for src in skills:
        dst = target / src.name
        if (dst / "SKILL.md").is_file() and md5(dst / "SKILL.md") == md5(src / "SKILL.md"):
            skipped += 1
            continue
        if dst.exists():
            shutil.rmtree(dst)
            updated += 1
        else:
            installed += 1
        shutil.copytree(src, dst)

    print(f"{len(skills)} skills in bundle -> {target}")
    print(f"  installed: {installed}  updated: {updated}  unchanged: {skipped}")
    print("Start a new agent session for the skills to be picked up.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
