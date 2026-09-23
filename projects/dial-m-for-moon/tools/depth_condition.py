#!/usr/bin/env python3
"""depth_condition.py — Depth Anything V2 Small depth-map conditioning step.

Takes a keyframe/reference image and emits a grayscale depth map PNG suitable
as structural conditioning (ControlNet-style depth input) for image-to-video
generation, or as a continuity check against Shot Composer previz.

Usage:
    python depth_condition.py input.png output_depth.png
    python depth_condition.py input.png output_depth.png --model depth-anything/Depth-Anything-V2-Small-hf

The model (~25M params) runs CPU-only here; GPU auto-used if available.
First run downloads weights from Hugging Face (cached afterwards).
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image


def estimate_depth(image_path: str, model_id: str):
    from transformers import AutoImageProcessor, DepthAnythingForDepthEstimation
    import torch

    processor = AutoImageProcessor.from_pretrained(model_id, local_files_only=True)
    model = DepthAnythingForDepthEstimation.from_pretrained(model_id, local_files_only=True)
    model.eval()

    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    # interpolate to input size
    pred = torch.nn.functional.interpolate(
        outputs.predicted_depth.unsqueeze(1),
        size=image.size[::-1],
        mode="bicubic",
        align_corners=False,
    ).squeeze().cpu().numpy()
    depth = Image.fromarray(pred)
    return image, depth


def to_grayscale_png(depth: Image.Image, out_path: str) -> None:
    arr = np.asarray(depth).astype(np.float32)
    lo, hi = arr.min(), arr.max()
    if hi > lo:
        arr = (arr - lo) / (hi - lo)
    out = Image.fromarray((arr * 255).astype(np.uint8))
    out.save(out_path)


def main() -> int:
    ap = argparse.ArgumentParser(description="Depth Anything V2 Small conditioning step")
    ap.add_argument("input", help="input keyframe / reference image")
    ap.add_argument("output", help="output grayscale depth PNG")
    ap.add_argument("--model", default=os.path.expanduser(
        "~/.cache/huggingface/hub/models--depth-anything--Depth-Anything-V2-Small-hf/snapshots/manual"),
        help="HF model id or local model dir (default: local Depth-Anything-V2-Small)")
    args = ap.parse_args()

    image, depth = estimate_depth(args.input, args.model)
    to_grayscale_png(depth, args.output)
    print(f"input {image.size} -> depth map written: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
