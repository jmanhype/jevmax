#!/usr/bin/env python3
"""Creative pipeline, layer 6 — flatten v2 creative specs into render prompts.

Input: jevmax-creative-v2 JSON specs (see creative/persona-ava.json).

List conventions (the wildcard mechanism):
  - a plain list of strings is COMPOSITIONAL: all items render together,
    joined with commas (e.g. environment.background)
  - a field named *_options holds ALTERNATIVES: flatten.py expands every
    combination into its own variant prompt, capped with --max-variants.
    Same idea as prompt wildcards (__location__ etc.), one level up.

Output: one painter-ready paragraph per variant, composed in render order
(character -> action -> product -> setting -> light -> camera -> style),
plus manifest.csv mapping every render back to variant_id / brief_id /
the exact option choices made.

Studio metadata (meta, variant, identity_reference, constraints, schema)
never enters the painter prompt: booleans and avoid-lists guide the
translator, not the painter (negations render weakly).

Usage: python3 flatten.py spec1.json [spec2.json ...] [--outdir creative/prompts]
"""
import argparse
import csv
import itertools
import json
import os

SKIP_SECTIONS = {"meta", "variant", "identity_reference", "constraints", "schema"}


def collect(spec):
    """Walk the spec -> ({path: value}, {path: [alternatives]})."""
    fixed, options = {}, {}

    def walk(node, path):
        if path.split(".")[-1] in SKIP_SECTIONS and path.count(".") == 0:
            return
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(node, list):
            strs = [x.strip() for x in node if isinstance(x, str) and x.strip()]
            if not strs:
                return
            if path.split(".")[-1].endswith("_options"):
                options[path] = strs
            else:
                fixed[path] = ", ".join(strs)
        elif isinstance(node, str) and node.strip():
            fixed[path] = node.strip()

    walk(spec, "")
    return fixed, options


def expand(fixed, options, max_variants):
    keys = sorted(options)
    combos = list(itertools.product(*(options[k] for k in keys))) if keys else [()]
    if len(combos) > max_variants:
        print(f"  (!) {len(combos)} combinations, capped at {max_variants}")
        combos = combos[:max_variants]
    out = []
    for combo in combos:
        v = dict(fixed)
        for k, val in zip(keys, combo):
            v[k] = val
        out.append((v, combo))
    return out, keys


def flatten(v):
    s = []

    def add(*parts):
        txt = ", ".join(dict.fromkeys(p for p in parts if p))
        if txt:
            s.append(txt)

    add(v.get("character.description"), v.get("character.default_expression"))
    add(v.get("pose.body"), v.get("pose.body_position"), v.get("pose.arms"),
        v.get("pose.hands"), v.get("pose.head"), v.get("pose.micro_action"))
    add(v.get("product.item"), v.get("product.interaction"), v.get("product.legibility"))
    add(v.get("outfit.top"), v.get("outfit.bottom"), v.get("outfit.accessories"))
    add(v.get("scene.spot"), v.get("scene.specific_spot"), v.get("scene.location"),
        v.get("scene.time_of_day"), v.get("scene.atmosphere"))
    add(v.get("environment.background"), v.get("environment.foreground"))
    add(v.get("environment.lighting.source"), v.get("environment.lighting.temperature"),
        v.get("environment.lighting.effect"), v.get("environment.lighting"))
    add(v.get("camera.pov"), v.get("camera_perspective.pov"), v.get("camera.angle"),
        v.get("camera.framing"), v.get("camera.lens_character"),
        v.get("camera.depth_of_field"), v.get("camera.distance"))
    add(v.get("grade.look"), v.get("post_processing.color_grading"),
        v.get("grade.contrast"), v.get("grade.retouching"),
        v.get("post_processing.retouching"), v.get("grade.final_look"))
    return " | ".join(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("specs", nargs="+")
    ap.add_argument("--outdir", default="creative/prompts")
    ap.add_argument("--max-variants", type=int, default=50)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    rows = []
    for path in args.specs:
        with open(path, encoding="utf-8") as f:
            spec = json.load(f)
        fixed, options = collect(spec)
        variants, keys = expand(fixed, options, args.max_variants)
        vmeta = spec.get("variant", {})
        base_id = vmeta.get("variant_id") or os.path.splitext(os.path.basename(path))[0]
        char = spec.get("character", {})
        char_id = char.get("character_id", "unspecified") if isinstance(char, dict) else "unspecified"
        brief = vmeta.get("brief_id") or ""

        print(f"{os.path.basename(path)}: {len(variants)} variant(s)"
              + (f" (expanding {', '.join(k.split('.')[-1] for k in keys)})" if keys else ""))
        for i, (v, combo) in enumerate(variants):
            vid = base_id if len(variants) == 1 else f"{base_id}-E{i + 1:02d}"
            fname = os.path.join(args.outdir, f"{vid}.txt")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(flatten(v) + "\n")
            choices = " | ".join(f"{k.split('.')[-1]}={c}" for k, c in zip(keys, combo)) if keys else ""
            rows.append({"variant_id": vid, "character_id": char_id, "brief_id": brief,
                         "expansions": choices, "prompt_file": fname})

    mpath = os.path.join(args.outdir, "manifest.csv")
    with open(mpath, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["variant_id", "character_id", "brief_id",
                                          "expansions", "prompt_file"])
        w.writeheader()
        w.writerows(rows)
    print(f"Written: {len(rows)} prompt(s) + manifest.csv -> {args.outdir}/")


if __name__ == "__main__":
    main()
