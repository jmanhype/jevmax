# Lost Future / Eyecandy / Jevmax / PixVerse — one-video test

Date: 2026-09-20

## Goal

Run the complete creative workflow with the operator-supplied native inputs,
but avoid the prior 475-credit nine-video batch. The authorized test was one
video using the already-approved Ava seed.

## Inputs now made native

- Canonical Lost Futures custom-GPT prompt:
  [creative/lost-future-system-prompt.md](../../../creative/lost-future-system-prompt.md)
- Live Eyecandy grammar source and selected technique mappings:
  [creative/eyecandy-source-grammar.md](../../../creative/eyecandy-source-grammar.md)
- Four generated candidate concepts:
  [creative/lost-future-ava-concepts.csv](../../../creative/lost-future-ava-concepts.csv)
- Gate winner spec:
  [creative/persona-ava-lost-future-lf001.json](../../../creative/persona-ava-lost-future-lf001.json)

## Layer 1 — Lost Future concepts

Four style families were generated under the supplied Lost Futures Architect
prompt:

1. 1994–1998 Regional Retail VHS Accessory Demo Tape
2. 1990–1998 Local Broadcast Forecast Scanline
3. 1993–1998 CD-ROM Kiosk Product Tour
4. 1986–1992 Local Sponsor Bumper

## Layer 2 — Eyecandy grammar

Eyecandy was fetched live from `https://eyecannndy.com/`; 138 technique
categories were exposed by the site.

The considered techniques were:

- Camera Roll — full-scene rotation
- Floating UI — abstract digital interface
- Vintage — discovered-recording aesthetic
- Central Framing — centered subject and visual emphasis

The Jev gate selected **Central Framing** as the dominant technique, with
Vintage supplying the production register. Camera Roll and Floating UI were
withheld to avoid overpacking the five-second test.

## Layer 3 — Jev pre-render gate

Command:

```bash
python3 score_briefs.py creative/lost-future-ava-concepts.csv \
  --brand 'Unbranded white wired earbuds for everyday listeners; fictional creator Ava; playful but clear paid-social tone; product must stay legible; AI-generated media will be disclosed' \
  --out runs/2026-09-20/lost-future-test/ranked_lost_future_concepts.csv
```

Measured usage: **1,771 input / 200 output tokens**.

Ranked result:

| Rank | Concept | Hook | Fit | Survival | Total |
|---:|---|---:|---:|---:|---:|
| 1 | 1986–1992 Local Sponsor Bumper | 2.27 | 0.70 | 0.57 | **6.34** |
| 2 | 1994–1998 Regional Retail VHS Accessory Demo Tape | 2.50 | 0.58 | 0.47 | 5.87 |
| 3 | 1990–1998 Local Broadcast Forecast Scanline | 1.71 | 0.61 | 0.46 | 5.22 |
| 4 | 1993–1998 CD-ROM Kiosk Product Tour | 1.34 | 0.57 | 0.58 | 4.77 |

Selected concept:

> **Sponsored Minute** — “One minute of quiet, courtesy of tomorrow.”

## Layer 4 — Canonical spec

The winning concept was encoded in:

[creative/persona-ava-lost-future-lf001.json](../../../creative/persona-ava-lost-future-lf001.json)

The Ava character block remains verbatim-frozen. The approved seed image is
the only identity reference:

`/Users/batmanosama/jevmax/creative/renders/ava-01_seed.png`

## Layer 5 — Flatten / PixVerse kit

Generated exactly one variant:

- Prompt:
  [flatten/LF001.txt](flatten/LF001.txt)
- Kit:
  [pixverse/LF001.kit.md](pixverse/LF001.kit.md)
- Video direction:
  [pixverse/LF001.direction.txt](pixverse/LF001.direction.txt)

Technical execution used the enhanced Seedance prompt:

[seedance-prompt.txt](seedance-prompt.txt)

## Render

Queue:

`/Users/batmanosama/jevmax/projects/jevmax-lost-future-lf001/queue.json`

Planned and executed tasks: **1**

| Parameter | Value |
|---|---|
| Model | `seedance-2.5` |
| Mode | reference / image-to-video |
| Identity reference | approved Ava seed |
| Resolution | 1080×1920 |
| Aspect | 9:16 |
| Duration target | 5 seconds |
| Wall time | 454.221 seconds |

Task ID: `425658437056168`

Local deliverable:

`/Users/batmanosama/jevmax/projects/jevmax-lost-future-lf001/assets/videos/425658437056168/pixverse_video_425658437056168_1789963836520.mp4`

SHA-256:

`d794ebe294dae433700435cc128070fa9c5066f3d432a8100ceb21da762bd4cf`

## Measured spend

| Measure | Value |
|---|---:|
| Credits before | 11,675 |
| Credits after | 10,825 |
| Observed delta | **850** |
| Task-attributed credits | **850** |
| Seed image spend | 0 |
| Additional renders | 0 |

This is an important cost result: the plugin’s Seedance 2.5 1080p default cost
**850 credits for one 5-second reference video**, versus the previously
measured V6 720p route at 50 credits per video. Preflight did not expose an
exact per-task price before submission.

Future renders should treat model choice as a hard cost gate. Do not use the
premium Seedance route for routine tests unless 850 credits is explicitly
approved.

## Technical QA

Aggregate technical QA passed:

- Local file exists
- MP4 / HEVC video
- 1080×1920
- 9:16 aspect
- 5.056-second duration
- 24 fps
- 121 video frames
- AAC audio stream present

QA report:

`/Users/batmanosama/jevmax/projects/jevmax-lost-future-lf001/quality/latest-run-qa.json`

## Human visual QA

Human review of evenly sampled frames found:

- Ava identity and wardrobe remained stable
- Central framing held
- Earbud product remained legible
- Analog tracking streak appeared as intended
- No extra people were introduced

Material constraint miss:

- From approximately the last 1.5 seconds, PixVerse generated a garbled white
  sponsor card reading roughly “Spuaille Sponder” with smaller pseudo-text.
  The prompt explicitly requested no readable text, captions, logos, or UI.
  This makes the current output unsuitable as an ad-ready asset even though
  generation and technical QA succeeded.

No automatic paid retry was made. A retry requires a fresh explicit cost/model
decision.

## Recommendation

1. **Do not run another premium Seedance test by default.**
2. Preserve this file as evidence of the workflow and pricing.
3. If another paid test is needed, use the previously measured V6 720p route
   at approximately 50 credits and explicitly reinforce the no-text constraint
   near the final-frame instruction.
4. If the last 1.5 seconds are the only bad section, a local trim or localized
   post-process may be cheaper than another generation, but it changes duration
   or image content and needs operator review.

## Conclusion

The end-to-end workflow is operational:

**Lost Future prompt → Eyecandy technique → candidate concepts → Jev gate →
canonical spec → flatten → PixVerse kit → one reference render → technical QA →
human QA → measured invoice**

The first premium-route test succeeded mechanically and exposed two durable
lessons: exact render cost must be treated as a gate, and no-text constraints
remain weakly honored by video generation.
