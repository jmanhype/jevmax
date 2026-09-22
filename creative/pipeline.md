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
8. SCHEDULE    Buffer MCP (remote, https://mcp.buffer.com/mcp) -> queue Reels
               and carousels to the two connected IG channels. Token lives in
               ~/.zcode config + ~/.claude.json + ~/.cursor/mcp.json — never
               in this repo.
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
- [x] Native Lost Future + Eyecandy one-video test — COMPLETE 2026-09-20.
      The supplied custom-GPT prompt and live Eyecandy grammar were captured,
      four concepts were Jev-gated, and LF001 was rendered once from the
      approved Ava seed. Seedance 2.5 1080p cost **850 credits**, 17× the old
      V6 720p unit price. Technical QA passed; human QA caught a garbled
      sponsor-card text overlay in the final ~1.5 seconds, so LF001 is evidence,
      not an ad-ready creative. Full record:
      `runs/2026-09-20/lost-future-test/REPORT.md`.
- [x] CLI price recheck — 2026-09-20. GPT Image 2.5 Flare and Sunburst both
      completed at **0 credits** under the current paid-member promotion. A
      strengthened LF001 rerender measured **V6 720p = 40 credits** and
      **MiniMax H3 768p = 150 credits**. V6 preserved the seed composition and
      no-text constraint; H3 drifted Ava from seated-on-towel to standing in
      shallow water. Full record: `runs/2026-09-20/cli-price-test/REPORT.md`.
- [ ] Upstream board expansion — 2026-09-21. The related Lost Futures board adds
      six planned business clusters, six planned cinema/story clusters, and
      cross-cutting intake tags. Jevmax routing is recorded in
      [board-expansion-clusters.md](board-expansion-clusters.md). No image or
      video generation has been submitted for those planned clusters.
- [x] CLI re-auth + upgrade 2026-09-22: token had expired (code 10002);
      device-flow re-login OK (Pro), CLI 1.4.1 -> 1.4.5. Current balance:
      **10,595 credits** (60 daily + 4,445 membership + 6,090 bonus,
      3 high-quality renders left). ~1,080 credits spent since the 09-20
      figure — reconcile against render_log.csv before budgeting the next batch.
- [x] Jev judgment gate integrated 2026-09-22 (pijev, permutation-invariant).
      House method is the skill-correct pattern from docs.typesafe.ai: NARROW
      one-judgment questions over a factual state, weights combined in code
      (30/30/15/15/10), a none_of_these option, speculative premises marked.
      No composite "pick the best overall" questions. API key lives in the
      operator's shell env, never in this repo. Decisions logged with their
      probability distributions in the franchise logs.
- [x] Layer 8 machinery: Buffer MCP installed + verified 2026-09-22.
      20 tools incl. create_post, list_posts, ideas, templates, post metrics,
      plus generic GraphQL (execute_query / execute_mutation /
      introspect_schema). Token verified end-to-end via get_account +
      list_channels. Connected channels: glowgolfchronicles + batmanosama
      (both IG business). Free-tier limits: 3 channels / 10 scheduled posts /
      100 ideas. Reels/video upload via create_post is untested — verify with
      a throwaway draft before planning the cadence around it.
