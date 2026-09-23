# Shot record — production unit (v1.1, 2026-09-23)

One row/record per shot. Adopts the best of what the closed platforms ship as
products, composed from open parts (see `decisions.md` 2026-09-23 adoption
note): **Dramagic**'s script→structured-shot-table with matched assets,
**Slate**'s director's brief + takes, **Eyecandy** as the grammar layer
(`eyecandy-catalog.md`), **Shot Composer** as the previz layer (free
pre-render blocking check; capture doubles as a generation reference frame),
generation via Kling MCP / PixVerse CLI, selection via Jev.

## Episode header (director's brief — one per episode, Slate-style)

```
EP: EP001 · title · target duration (e.g. 110s vertical 9:16)
beat-in: state the episode enters on        beat-out: exit state (button)
grade register: series-wide look lock (e.g. 16mm Ektachrome, Vintage, halation on practicals)
cast: Element ids + lock files (e.g. Valya 322149783311120 / identity_lock.yaml)
grammar budget: max distinct dominant techniques per episode (default 5)
```

## Shot record (one per shot — the storyboard table row, Dramagic-style)

```
shot: EP001-S01 · duration 5s · ratio 9:16
beat: what this shot changes (info/power/state) — from script.md scene
eyecandy: ONE dominant technique (name + slug)   [required, from catalog]
  camera:  concrete framing/movement the name implies, said twice
  motion:  subject/world motion spec
  world:   set/prop/environment deltas
  grade:   shot-level deviation from series register (default: none)
withheld: techniques deliberately NOT used (anti-overpacking)  [required non-empty]
previz: REQUIRED for geometrically complex shots (OTS, split-plane/split-diopter,
  rack beats, motion timing) — build blocking in Shot Composer (MCP
  `shot-composer` in new sessions, or the UI at localhost:5173), verify, and
  `capture_shot` → PNG; record path here + use as generation reference frame.
  SKIPPED for unambiguous inserts (object close-ups) — write "skip: simple insert".
assets: Element refs / bible pages / prop refs (matched, Dramagic-style);
  previz frame path when present
audio: sound design beats (Kling native audio prompt lines)
takes: N (imageCount/videoCount, default 2) · gate: pick-by (vision describe -> Jev select)
prompt: the final generation prompt (recorded verbatim after render)
```

## Rules

1. No shot without a named dominant technique; no shot with two dominants.
2. `withheld` must be non-empty — the discipline is naming what you refuse.
3. Complex shots carry a previz frame BEFORE any render budget is spent;
   simple inserts record the skip reason. Previz is free; takes are not.
4. Takes: generate ≥2, select via vision-description + Jev (or human REVIEW
   band) before a shot enters the edit sheet. Never spend render credits once
   on an ungated single take of a critical beat.
5. Records are markdown in the episode's `storyboard.md`; after render, the
   verbatim prompt is appended (generation-record convention).
6. Gate discipline unchanged: episode map must have ADVANCE'd before its shots
   get budgets; script must be canon-clean vs both bibles.
7. Platform routing per shot: PixVerse v6 for inserts/atmosphere drafts
  (free gpt-image-2.5 seeds, 40-50 cr/take, --seed/--idempotency-key);
  Kling 3.0 for dialogue/audio-critical finals (Elements, prompted sound).
  Record platform + actual credit delta on every render (quoted costs drift).
