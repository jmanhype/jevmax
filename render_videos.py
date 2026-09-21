#!/usr/bin/env python3
"""Batch video renderer — runs every kit's VIDEO DIRECTION through the PixVerse CLI.

Reads creative/pixverse/manifest.csv, renders each variant's direction prompt as
image-to-video against the character seed, and appends results (video URL,
credits spent, status) to creative/pixverse/render_log.csv. One Jev-style rule:
the seed NEVER varies — identity consistency flows through it.

Usage:
    python3 render_videos.py --seed creative/renders/ava-01_seed.png
    python3 render_videos.py --seed ... --only V002-E01,V002-E03   # subset
    python3 render_videos.py --seed ... --dry-run                  # list, no spend
"""
import argparse
import csv
import json
import os
import subprocess
import sys

RENDER_LOG = "creative/pixverse/render_log.csv"


def render_one(direction_txt, seed, outdir, vid, timeout_s):
    cmd = [
        "pixverse", "create", "video",
        "--prompt", direction_txt,
        "--image", seed,
        "--model", "v6", "--quality", "720p",
        "--duration", "5", "--aspect-ratio", "9:16",
        "--timeout", str(timeout_s), "--json",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s + 120)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = {"status": "error", "error": (proc.stdout + proc.stderr)[-400:]}
    url = data.get("video_url") or ""
    if url:
        dest = os.path.join(outdir, f"{vid}.mp4")
        dl = subprocess.run(["curl", "-sL", "--max-time", "120", "-o", dest, url],
                            capture_output=True)
        if dl.returncode != 0 or not os.path.exists(dest) or os.path.getsize(dest) < 10_000:
            dest = ""
    else:
        dest = ""
    return {
        "variant_id": vid,
        "status": data.get("status", "error"),
        "credits": data.get("cost_credits", ""),
        "video_id": data.get("video_id", ""),
        "video_url": url,
        "local_file": dest,
        "error": data.get("error", ""),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", required=True, help="character seed image (identity anchor)")
    ap.add_argument("--manifest", default="creative/pixverse/manifest.csv")
    ap.add_argument("--only", default="", help="comma-separated variant_ids to render")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=int, default=600, help="per-video poll timeout (s)")
    args = ap.parse_args()

    if not os.path.exists(args.seed):
        sys.exit(f"seed not found: {args.seed}")

    with open(args.manifest, newline="", encoding="utf-8") as f:
        kits = [r for r in csv.DictReader(f) if r["variant_id"] != "V001"]  # V001 priced separately
    if args.only:
        want = {v.strip() for v in args.only.split(",")}
        kits = [k for k in kits if k["variant_id"] in want]

    todo = []
    for k in kits:
        vid = k["variant_id"]
        direction = f"creative/pixverse/{vid}.direction.txt"
        if not os.path.exists(direction):
            print(f"SKIP {vid}: no {direction}")
            continue
        todo.append((vid, direction))

    if args.dry_run:
        print("Would render:", ", ".join(v for v, _ in todo))
        return

    outdir = os.path.dirname(args.manifest)
    new_log = not os.path.exists(RENDER_LOG)
    total = 0
    with open(RENDER_LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["variant_id", "status", "credits",
                                          "video_id", "video_url", "local_file", "error"])
        if new_log:
            w.writeheader()
        for i, (vid, direction) in enumerate(todo, 1):
            print(f"[{i}/{len(todo)}] rendering {vid} ...", flush=True)
            row = render_one(direction, args.seed, outdir, vid, args.timeout)
            w.writerow(row)
            f.flush()
            spent = row["credits"]
            total += int(spent) if str(spent).isdigit() else 0
            print(f"    {row['status']}  credits={row['credits'] or '?'}  file={row['local_file'] or '-'}"
                  + (f"  ERROR: {row['error'][:120]}" if row["error"] else ""), flush=True)

    print(f"\nDone: {len(todo)} video(s), {total} credits spent this batch. Log: {RENDER_LOG}")


if __name__ == "__main__":
    main()
