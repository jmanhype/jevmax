#!/usr/bin/env python3
"""qc_shot_lock.py — camera-lock + set-drift QC for a generated shot.

Catches the defect class Jay spotted in EP003 S03 take1: the set morphing
mid-shot.

Method (classical, numpy/PIL only): cut a grid of small patches from the
head frame and NCC-match each against the SAME location in the tail frame
(zero shift). NCC is invariant to linear brightness changes, so only real
structural change lowers it. In a locked shot with a holding set, background
patches correlate ~0.9; the subject's patches don't. Metric:

    lock_fraction = fraction of patches with zero-shift NCC > 0.75

Two branches:
  * candidate_bg = patches with low head-tail RGB diff (verifiable background).
    If < 5% of the frame, the shot doesn't hold head-to-tail at all
    (camera moved, subject swept the frame, or full repaint) => FLAG, or
    INCONCLUSIVE with --allow-motion.
  * bg_hold = of candidate patches, fraction with NCC > 0.75. If < 50%,
    the background changed under the camera => FLAG (set drift).

Calibrated 2026-09-23:
  EP003 S03 take1 (camera swung, 3-wall morph): cand  low  => FLAG
  EP003 S03 take2 ("locked" but set re-dressed): cand ok, hold low => FLAG
  EP003 S01 take1 (subject sweeps frame): cand low => FLAG/INCONCLUSIVE
  EP003 S02 take2 (true lock): cand high, hold high => PASS

Why not the depth model: Depth-Anything-V2-Small was tried for this job and
rejected 2026-09-23 — its relative depth is scene-context dependent, so the
same physical wall scores different depth when the foreground composition
changes (locked take2 scored the same "drift" as drifting take1). Template
search also failed: the jackfield's periodic texture gives false NCC peaks
at shifted positions. Zero-shift patch NCC has neither problem.

Usage:
    python qc_shot_lock.py shot.mp4 [--threshold 0.25] [--allow-motion]

Exit 0 = PASS, 1 = FLAG/INCONCLUSIVE.
Calibrated 2026-09-23 on EP003 S03 take1 (drift) vs take2 (locked).
"""
import argparse
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image


def extract_frame(video: str, t: str, out: str) -> None:
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", video,
         "-frames:v", "1", out], check=True)


def probe_duration(video: str) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", video], check=True, capture_output=True, text=True)
    return float(r.stdout.strip())


def gray_w320(path: str) -> np.ndarray:
    im = Image.open(path).convert("L")
    w = 320
    h = int(im.height * w / im.width)
    return np.asarray(im.resize((w, h), Image.BILINEAR)).astype(np.float32)


def zero_shift_stats(g1: np.ndarray, g2: np.ndarray,
                     patch: int = 21, stride: int = 8):
    """Per-patch: zero-shift NCC and mean abs diff between g1 and g2."""
    H, W = g1.shape
    r = patch // 2
    nccs, diffs = [], []
    for y in range(r, H - r, stride):
        for x in range(r, W - r, stride):
            t = g1[y - r:y + r + 1, x - r:x + r + 1].ravel().astype(np.float32)
            p = g2[y - r:y + r + 1, x - r:x + r + 1].ravel().astype(np.float32)
            diffs.append(float(np.abs(t - p).mean()))
            t = t - t.mean()
            p = p - p.mean()
            denom = np.sqrt((t * t).sum() * (p * p).sum())
            nccs.append(float((t * p).sum() / (denom + 1e-9)) if denom > 1e-9 else 0.0)
    return np.array(nccs), np.array(diffs)


def main() -> int:
    ap = argparse.ArgumentParser(description="Camera-lock + set-drift QC")
    ap.add_argument("video")
    ap.add_argument("--threshold", type=float, default=0.25,
                    help="(legacy) lock_fraction above this => PASS")
    ap.add_argument("--cand-diff", type=float, default=20.0,
                    help="mean abs diff below this => candidate background patch")
    ap.add_argument("--cand-frac", type=float, default=0.05,
                    help="candidate background below this => shot does not hold")
    ap.add_argument("--hold-frac", type=float, default=0.5,
                    help="of candidate patches, NCC>threshold below this => set drift")
    ap.add_argument("--ncc", type=float, default=0.75,
                    help="per-patch NCC counted as holding")
    ap.add_argument("--allow-motion", action="store_true",
                    help="low lock_fraction => INCONCLUSIVE instead of FLAG")
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    outdir = args.outdir or tempfile.mkdtemp(prefix="shotlock_")
    os.makedirs(outdir, exist_ok=True)
    dur = probe_duration(args.video)
    hp = os.path.join(outdir, "head.png")
    tp = os.path.join(outdir, "tail.png")
    extract_frame(args.video, "0.5", hp)
    extract_frame(args.video, f"{max(0.6, dur - 0.5):.2f}", tp)
    g1, g2 = gray_w320(hp), gray_w320(tp)

    nccs, diffs = zero_shift_stats(g1, g2)
    cand = diffs < args.cand_diff
    cand_frac = float(cand.mean())
    hold_frac = float((nccs[cand] > args.ncc).mean()) if cand.sum() else 0.0
    lock_fraction = float((nccs > args.ncc).mean())

    print(f"video: {args.video}  ({dur:.1f}s)")
    print(f"patches: {len(nccs)}  candidate_bg: {cand_frac*100:.1f}%  "
          f"bg_hold: {hold_frac*100:.1f}%  overall_lock: {lock_fraction*100:.1f}%")

    if cand_frac < args.cand_frac:
        detail = ("too little verifiable background head-to-tail "
                  "(camera moved, heavy occlusion, or full repaint)")
        verdict, rc = ("FLAG — " + detail, 1) if not args.allow_motion else \
                      ("INCONCLUSIVE — " + detail, 1)
    elif hold_frac < args.hold_frac:
        verdict, rc = "FLAG — set drift: background changed under the camera", 1
    else:
        verdict, rc = "PASS — camera locked, set holds", 0
    print(f"verdict: {verdict}")
    print(f"artifacts: {outdir}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
