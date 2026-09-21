# Creative Test Sprint — Measured Dogfood Evidence

## Existing V6 batch

Eight existing vertical variants are on disk:

- `V002-E01`
- `V002-E02`
- `V002-E03`
- `V002-E04`
- `V002-E05`
- `V002-E06`
- `V002-E07`
- `V002-E08`

Each is 9:16 and five seconds. The historical expansion route used V6 720p with
audio at 50 credits per video. The first seed image cost 25 credits and the
first priced video cost 50 credits, bringing the original nine-video plus seed
batch to **475 credits**.

## Current measured V6 route

The strengthened LF001 rerender used:

- model: `v6`
- resolution: 720p
- duration: 5 seconds
- audio: disabled
- credits: **40**
- task ID: `425667939727864`
- local QA: pass

Current projected eight-video sprint:

```text
8 x 40 credits = 320 credits
```

## Current V6 QA

The rerender:

- exists locally
- is 720×1280
- is 9:16
- runs 5.0417 seconds
- has no audio stream, as intended
- kept Ava seated on the towel
- preserved identity and wardrobe
- kept the earbud cable legible
- introduced no text card
- introduced no extra people

## Concept gate

The Lost Future/Eyecandy dogfood gate scored four concepts using:

```text
1,771 input tokens
200 output tokens
```

Top concept:

- title: `SPONSORED MINUTE`
- style: 1986–1992 Local Sponsor Bumper
- Eyecandy technique: Central Framing
- gate score: 6.34
- tagline: “One minute of quiet, courtesy of tomorrow.”

## Cost comparison

| Route | Quality | Duration | Measured credits |
|---|---:|---:|---:|
| Historical V6 audio route | 720p | 5s | 50 |
| Current V6 no-audio route | 720p | 5s | 40 |
| MiniMax H3 | 768p | 5s | 150 |
| Seedance 2.5 | 1080p | 5s | 850 |

Premium routes are excluded from the default sprint.

## Limitations

- The existing eight variants were produced under the older 50-credit audio-enabled route.
- Retro sponsor-bumper styling in the current V6 output is subtle rather than exaggerated.
- No live paid test has measured hook rate, CTR, conversion, or ROAS.
- A garbled text card appeared in the separate Seedance 1080p test; it is not used as V6 sprint evidence.
- The product is a controlled creative test, not a guarantee of advertising performance.
