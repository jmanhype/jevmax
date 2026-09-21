# The content engine — wiring Lost Future + Eyecandy + jevmax creative specs

2026-09-20. Six layers, one job each. Nothing enters the next layer until the
previous one is concrete.

```
1. IDEA        Lost Future GPT (Jay's custom GPT) — premise, world, story hook
2. STORY→SHOT  pick the beats that make ad moments (hook first)
3. GRAMMAR     Eyecandy (eyecannndy.com) — name the technique per shot
               (arc shot, fisheye, object POV...) + reference GIFs
4. SPEC        jevmax-creative-v2 JSON (persona-*.json) — technique translated
               into structured fields; any field may hold a LIST of options
5. GATE        score_briefs.py ranks concepts BEFORE render tokens are spent
6. RENDER      flatten.py -> painter-ready prompts; seed once per character,
               then variants keyed off identity_reference; ship with AI disclosure
7. MOTION      pixverse.py -> PixVerse CLI kits (npm `pixverse`, v1.4.5; auth:
               OAuth device flow, Jay's Pro account, 12,150 credits). Each kit
               ships the STILL SEED prompt (create image), the VIDEO DIRECTION
               (create video --image <seed>, image-to-video) and a hook-line
               TTS command. Web agent (app.pixverse.ai/agent) is the fallback.
```

## How the tools connect

- **PixVerse CLI** (layer 7) takes file paths, not pastes: `--prompt
  creative/pixverse/V001.seed.txt` reads the flatten.py output directly, so
  layers 4 -> 6 -> 7 run as one command chain with `--json` out and
  deterministic exit codes. Reference mode (V6, up to 10 images) is the
  character-consistency upgrade path once a seed exists.
- **Lost Future** (layer 1) outputs *what the story is*. Its wildcard-style
  lists (character traits, locations, actions) map directly onto LIST fields
  in the v2 schema (layer 4) — a wildcard list and a schema list are the same
  idea at different altitudes: options to be systematically expanded, not
  vibes to be re-typed.
- **Eyecandy** (layer 3) outputs *how the shot is seen*. Technique names are
  translated into schema fields (`camera.pov`, `camera.lens_character`,
  `environment.lighting`) per the mapping in technique-ideas.md.
- **flatten.py** (layer 6) is the translation layer: expands list fields into
  the cartesian product (capped), composes each variant into one painter-ready
  paragraph in render order (character -> action -> product -> setting ->
  light -> camera -> style), and writes a manifest so every render maps back
  to its variant id and brief_id.

## Rules that are easy to forget

- The `constraints.avoid` list never enters the painter prompt (negations are
  weakly honored — README lesson 5); it guides the translator.
- The `meta` / `variant` / `identity_reference` blocks never enter the painter
  prompt either — they're studio metadata, not visible content.
- Character block is verbatim-frozen; scene/wardrobe/pose/camera are the
  variable sections. Seed render (V001-equivalent) is generated once, approved,
  and referenced by every later variant.
- Disclosure (`disclose_as_ai`) is enforced at the ad layer
  (`self_ai_disclosure=OPT_IN`), not inside the image.

## Status

- [x] Layer 4 schema: persona-ava.json (+ persona-ava-variants.json wildcard demo)
- [x] Layer 6 machinery: flatten.py (+ manifest) — 9 prompts generated
- [x] Layer 7 machinery: pixverse.py — 9 kits + seed/direction txts in creative/pixverse/,
      each with runnable `pixverse create ...` commands (CLI v1.4.5 installed, authed)
- [x] Technique mapping: technique-ideas.md
- [x] Seed render of Ava — 2026-09-20, Nano Banana 2, 25 credits ->
      creative/renders/ava-01_seed.png (identity anchor for layers 6 AND 7)
- [x] FIRST VIDEO (V001): V6 image-to-video, 720p 5s 9:16, 50 credits ->
      creative/pixverse/V001.mp4. QA pass: identity stable, product legible,
      UGC handheld feel. MEASURED ECONOMICS: 25 cr/seed + 50 cr/video,
      so a 9-variant batch costs 475 credits (~4% of a 12k monthly balance).
- [x] Layer 1 example: captured 2026-09-20 from the real "Lost Future Style
      Catalog" conversation -> lost_future_example.md. Grammar: style family
      (S01-S50) -> concept TITLE/TAGLINE -> shot prompt/negative-prompt pairs
      with five reference anchors. Mapping into v2 schema fields is in that file.
- [x] Batch render V002-E01..E08 (render_videos.py) — COMPLETE 2026-09-20.
      All 9 videos on disk (V001 + 8 wildcard expansions), logged in
      render_log.csv. Total creative spend: 475 credits (25 seed + 9x50),
      ~11,675 remaining. Note: E06 "overhead" rendered as high close-up —
      video models interpret overhead loosely; tighten framing language if
      a true flat-lay is wanted.
