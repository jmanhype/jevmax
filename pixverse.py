#!/usr/bin/env python3
"""Creative pipeline, layer 7 — PixVerse video kits.

Takes the same jevmax-creative-v2 specs as flatten.py and emits one kit per
variant. Rendering runs through the PixVerse CLI (`npm install -g pixverse`,
OAuth device flow: `pixverse auth login`); the web agent (app.pixverse.ai/agent)
is the fallback. PixVerse is image-to-video at heart, so the loop is: render
the STILL SEED with an image model, approve it, then animate it with the VIDEO
DIRECTION as image-to-video. Character consistency flows through the seed image
(and later, multi-reference: V6 accepts up to 10 images).

Each variant produces three files:
    {vid}.kit.md        human-readable kit (also embeds the CLI commands)
    {vid}.seed.txt      still-seed prompt (feeds `create image --prompt`)
    {vid}.direction.txt video direction (feeds `create video --prompt`)

Optional spec fields (same list conventions as flatten.py; *_options expand):

    motion.camera      e.g. "handheld micro-drift, gentle push-in"
    motion.subject     e.g. "talks animatedly into the mic, wind in her hair"
    motion.world       e.g. "gentle waves rolling behind her"
    video.duration_s   default 5 (V6 supports 1-15)
    video.aspect       default 9:16
    video.hook_line    optional spoken line (renders via `create voice` TTS)

Defaults keep the UGC feel: handheld drift, no cinematic camera language.

Usage: python3 pixverse.py spec1.json [spec2.json ...] [--outdir creative/pixverse]
"""
import argparse
import csv
import json
import os

from flatten import collect, expand, flatten

DEFAULT_MOTION = {
    "motion.camera": "handheld smartphone drift, subtle and unpolished",
    "motion.subject": "talks naturally into the mic module, small gestures, wind moving her hair",
    "motion.world": "the background moves gently and continuously (waves, distant people)",
}


def direction_text(v, duration):
    return (
        f"Animate this frame as a candid vertical selfie video. "
        f"Subject: {v.get('motion.subject', DEFAULT_MOTION['motion.subject'])}. "
        f"Camera: {v.get('motion.camera', DEFAULT_MOTION['motion.camera'])}. "
        f"World: {v.get('motion.world', DEFAULT_MOTION['motion.world'])}. "
        f"Keep everything else locked: {v.get('grade.look', 'natural smartphone color science')}; "
        f"{v.get('camera.depth_of_field', 'subject sharp, background softly blurred')}. "
        f"No scene cuts, no style shifts — one continuous {duration}s take."
    )


def kit(v, vid, outdir):
    aspect = v.get("video.aspect", "9:16")
    duration = v.get("video.duration_s", "5")
    ref = v.get("identity_reference.reference_image",
                "creative/renders/<character>-seed.png  (upload once approved)")
    ref_path = ref.split("  (")[0].strip()
    hook_raw = v.get("video.hook_line")

    seed_txt = os.path.join(outdir, f"{vid}.seed.txt")
    dir_txt = os.path.join(outdir, f"{vid}.direction.txt")

    voice_cmd = ""
    if hook_raw:
        voice_cmd = (
            f"\n# 3) optional spoken hook (TTS -> lip-sync the seed video with it)\n"
            f'pixverse create voice --text "{hook_raw}" \\\n'
            f"  --output {outdir}/{vid}.hook.mp3 --json\n"
        )

    return f"""# PixVerse kit — {vid}

## 1. STILL SEED (image model first — this is the character anchor)
{flatten(v)}

## 2. VIDEO DIRECTION (image-to-video; seed stays locked)
{direction_text(v, duration)}

## 3. SETTINGS
- Aspect ratio: {aspect} (vertical)
- Duration: {duration}s
- Character reference: {ref}
- Preview mode on; keep seed fixed while iterating motion

## 4. HOOK LINE (speech / lip-sync)
{hook_raw or "(none set — add video.hook_line to the spec)"}

## 5. RUN IT (PixVerse CLI — `pixverse` on PATH; run from the jevmax/ repo root)

# 1) render the seed still (Nano Banana 2; people-strong alternatives: gpt-image-2.5-flare, seedream-5.0-pro)
pixverse create image --prompt {seed_txt} --model gemini-3.1-flash --quality 1080p --aspect-ratio {aspect} --json

# 2) approve the seed, save it to {ref_path}, then animate it (V6: 1-15s, up to 10 reference images)
pixverse create video --prompt {dir_txt} --image {ref_path} --model v6 --quality 720p --duration {duration} --aspect-ratio {aspect} --json
{voice_cmd}
# JSON out + deterministic exit codes -> pipe into scripts; `--count 4 --seed N` for batch variants.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("specs", nargs="+")
    ap.add_argument("--outdir", default="creative/pixverse")
    ap.add_argument("--max-variants", type=int, default=50)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    rows = []
    for path in args.specs:
        with open(path, encoding="utf-8") as f:
            spec = json.load(f)
        fixed, options = collect(spec)
        variants, keys = expand(fixed, options, args.max_variants)
        approved_ref = spec.get("identity_reference", {}).get("reference_image")
        vmeta = spec.get("variant", {})
        base_id = vmeta.get("variant_id") or os.path.splitext(os.path.basename(path))[0]
        print(f"{os.path.basename(path)}: {len(variants)} PixVerse kit(s)")
        for i, (v, combo) in enumerate(variants):
            if approved_ref:
                v["identity_reference.reference_image"] = approved_ref
            vid = base_id if len(variants) == 1 else f"{base_id}-E{i + 1:02d}"
            fname = os.path.join(args.outdir, f"{vid}.kit.md")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(kit(v, vid, args.outdir))
            with open(os.path.join(args.outdir, f"{vid}.seed.txt"), "w", encoding="utf-8") as f:
                f.write(flatten(v))
            with open(os.path.join(args.outdir, f"{vid}.direction.txt"), "w", encoding="utf-8") as f:
                f.write(direction_text(v, v.get("video.duration_s", "5")))
            rows.append({"variant_id": vid, "kit_file": fname,
                         "aspect": v.get("video.aspect", "9:16"),
                         "duration_s": v.get("video.duration_s", "5")})

    mpath = os.path.join(args.outdir, "manifest.csv")
    with open(mpath, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["variant_id", "kit_file", "aspect", "duration_s"])
        w.writeheader()
        w.writerows(rows)
    print(f"Written: {len(rows)} kit(s) + seed/direction txts + manifest.csv -> {args.outdir}/")


if __name__ == "__main__":
    main()
