#!/usr/bin/env python3
"""qc_continuity.py — temporal-consistency QC for a generated shot.

Catches the defect class Jay spotted in EP003 S03 take1: the set morphing
mid-shot (plus subtler re-dressing that the eye misses, as in S03 take2).

Method — three signals, all CPU-friendly, no depth model:
  1. CLIP cosine similarity across N evenly-sampled frames (VBench-style
     "background consistency"). Catches backgrounds that subtly drift or
     reshape over time even when the foreground subject looks fine.
     Metrics: min consecutive-frame similarity, head-vs-tail similarity.
  2. Farneback dense optical flow (OpenCV) between consecutive samples.
     Median flow magnitude ~= global motion energy: a locked camera reads
     near-zero even with a moving subject; a camera swing or full repaint
     reads high.
  3. Consecutive-frame MSE on downscaled grayscale (cheap change detector).

Why not the depth model: Depth-Anything-V2-Small was tried for this job and
retired 2026-09-23. Relative monocular depth is normalized per frame (the
network only learns ordering *within* one image), so the same physical wall
scores different depth when the foreground composition changes — a truly
locked shot scored the same "drift" as a drifting one. Cross-frame depth
comparison is invalid by construction; the model is now reserved for
single-frame creative work (keyframe gating, depth-driven post, 3D Ken Burns
fillers). See editing-doctrine.md.

Usage:
    python qc_continuity.py shot.mp4 [--samples 8] [--allow-motion]

Exit 0 = PASS, 1 = FLAG.
Calibrated 2026-09-23 on EP003 takes (numbers below). A FLAG means
"human review", not automatic rejection.

Calibration results (8 samples, CLIP ViT-B/32 pooler_output, Farneback@320px):
  DRIFT   S03 take1 (camera swing, set morphs): min_consec 0.903, head_tail
          0.779, flow 19.6px  -> FLAG (head_tail + flow)
  REDRESS S03 take2 (locked cam, jackfield re-dressed to meter panel):
          min_consec 0.866, head_tail 0.831, flow 13.5px -> FLAG (both CLIP)
  LOCKED  S02 take2 (clean locked control): min_consec 0.931, head_tail
          0.927, flow 0.6px -> PASS
  SWEEP   S01 take1 (legit subject action): min_consec 0.875, head_tail
          0.861, flow 26.9px -> FLAG; with --allow-motion flow is
          informational and CLIP still flags for review (accepted shot).

Thresholds separate LOCKED from everything else with margin:
min_consec 0.90, head_tail 0.85, flow 2.0px.

Note: transformers>=5's get_image_features() returns
BaseModelOutputWithPooling; the projected embedding is .pooler_output
(512-d), NOT [0] (that is the raw patch sequence, (1,50,768)).
"""
import argparse
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

DEFAULT_CLIP_DIR = os.path.expanduser(
    "~/.cache/huggingface/hub/models--openai--clip-vit-base-patch32"
    "/snapshots/manual")

# Calibrated 2026-09-23 on EP003 (LOCKED/DRIFT/REDRESS/SWEEP; see module
# docstring). Thresholds separate the clean locked control from the rest.
FLAG_MIN_CONSEC_CLIP = 0.90   # min cosine sim over consecutive samples
FLAG_HEAD_TAIL_CLIP = 0.85    # head-frame vs tail-frame cosine sim
FLAG_MAX_MEDIAN_FLOW = 2.0    # px at 320px width, worst segment


def extract_frames(video: str, n: int, outdir: str):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", video], check=True, capture_output=True, text=True)
    dur = float(r.stdout.strip())
    paths = []
    for i in range(n):
        t = dur * (i + 0.5) / n
        p = os.path.join(outdir, f"f{i:02d}.png")
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", video,
             "-frames:v", "1", p], check=True)
        paths.append(p)
    return paths


def load_clip(clip_dir: str):
    import torch
    from transformers import CLIPModel, CLIPProcessor
    model = CLIPModel.from_pretrained(clip_dir, local_files_only=True)
    proc = CLIPProcessor.from_pretrained(clip_dir, local_files_only=True)
    model.eval()
    return model, proc, torch


def clip_sims(paths, clip_dir):
    """Cosine similarity matrix of CLIP image embeddings."""
    model, proc, torch = load_clip(clip_dir)
    embs = []
    with torch.no_grad():
        for p in paths:
            im = Image.open(p).convert("RGB")
            inp = proc(images=im, return_tensors="pt")
            out = model.get_image_features(**inp)
            # transformers>=5: BaseModelOutputWithPooling; [0] is the raw
            # patch sequence (batch,50,768), [1]/pooler_output is the
            # projected 512-d image embedding.
            feat = out.pooler_output
            feat = feat / feat.norm(p=2, dim=-1, keepdim=True)
            embs.append(feat[0].numpy())
    E = np.stack(embs)
    S = E @ E.T
    consec = [S[i, i + 1] for i in range(len(paths) - 1)]
    return float(np.min(consec)), float(S[0, -1]), [float(c) for c in consec]


def gray_w320(path: str) -> np.ndarray:
    im = Image.open(path).convert("L")
    w = 320
    h = int(im.height * w / im.width)
    return np.asarray(im.resize((w, h), Image.BILINEAR)).astype(np.float32)


def flow_and_mse(paths):
    """Farneback median flow magnitude + MSE per consecutive pair."""
    import cv2
    grays = [gray_w320(p) for p in paths]
    med_flows, mses = [], []
    for g1, g2 in zip(grays, grays[1:]):
        flow = cv2.calcOpticalFlowFarneback(
            g1, g2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag = np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2)
        med_flows.append(float(np.median(mag)))
        mses.append(float(np.mean((g1 - g2) ** 2)))
    return med_flows, mses


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--samples", type=int, default=8)
    ap.add_argument("--allow-motion", action="store_true",
                    help="action shot: flow branch is informational only")
    ap.add_argument("--clip-dir", default=DEFAULT_CLIP_DIR)
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as td:
        paths = extract_frames(args.video, args.samples, td)
        min_consec, head_tail, consec = clip_sims(paths, args.clip_dir)
        med_flows, mses = flow_and_mse(paths)

    max_med_flow = max(med_flows)
    max_mse = max(mses)

    print(f"clip min_consecutive_sim : {min_consec:.4f}")
    print(f"clip head_tail_sim       : {head_tail:.4f}")
    print(f"flow max_median_mag(px)  : {max_med_flow:.3f} "
          f"(per-segment: {' '.join(f'{m:.2f}' for m in med_flows)})")
    print(f"mse  max_consecutive      : {max_mse:.1f}")

    reasons = []
    if min_consec < FLAG_MIN_CONSEC_CLIP:
        reasons.append(
            f"clip min_consecutive_sim {min_consec:.3f} < {FLAG_MIN_CONSEC_CLIP}")
    if head_tail < FLAG_HEAD_TAIL_CLIP:
        reasons.append(
            f"clip head_tail_sim {head_tail:.3f} < {FLAG_HEAD_TAIL_CLIP}")
    if not args.allow_motion and max_med_flow > FLAG_MAX_MEDIAN_FLOW:
        reasons.append(
            f"flow max_median {max_med_flow:.2f}px > {FLAG_MAX_MEDIAN_FLOW}px")

    if reasons:
        print("VERDICT: FLAG — " + "; ".join(reasons))
        return 1
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
