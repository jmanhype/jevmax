# Brand Identity System evidence

Verification date: 2026-09-21

## Result

The package was assembled from existing repository artifacts with **0 new
generation credits**. It reuses the approved Ava identity seed and an existing
V6 validation render; no live API, image generation, video generation, media
change, commit, or push was performed while creating this package.

## Approved identity and seed integrity

| Item | Evidence |
|---|---|
| Character ID | `ava-01` |
| Contract | [creative/persona-ava.json](../../../creative/persona-ava.json) |
| Downstream variant | [creative/persona-ava-lost-future-lf001.json](../../../creative/persona-ava-lost-future-lf001.json) |
| Approved seed | [creative/renders/ava-01_seed.png](../../../creative/renders/ava-01_seed.png) |
| Seed format | PNG, 768 x 1376, RGB |
| Seed bytes | 1,720,465 |
| SHA-256 | `3acc728cbe8bd2e252f6f5459c3f2c5ec08984de75286bad0a2f71303815d0f9` |
| Historical seed route | Nano Banana 2, 25 credits, recorded in [docs/BUILD_LOG.md](../../../docs/BUILD_LOG.md) |

The seed hash was recomputed locally on 2026-09-21 and matched the approved
value above. Both the base persona and LF001 variant identify Ava as fictional,
not based on a real person, and discloseable as AI-generated. The LF001 variant
explicitly requires reuse of the approved seed and forbids another identity
anchor.

## Mandatory identity constraints

| Constraint | Base persona | LF001 variant |
|---|---:|---:|
| `render_fictional_model_only` | true | true |
| `no_real_person_likeness` | true | true |
| `disclose_as_ai` | true | true |
| `product_must_be_legible` | true | true |
| Character block locked | true | true |
| Based on real person | false | false |

The style layer additionally avoids requesting the exact style of a living
artist and translates visual references into era, medium, lighting, composition,
production method, and artifacts in
[creative/lost-future-system-prompt.md](../../../creative/lost-future-system-prompt.md).

## Visual grammar evidence

The controlled grammar is recorded in
[creative/eyecandy-source-grammar.md](../../../creative/eyecandy-source-grammar.md):

- Dominant technique: Central Framing.
- Supporting register: Vintage/discovered analog tape.
- Deliberately withheld from the first execution: Camera Roll and Floating UI,
  to avoid overpacking a five-second test.
- Technique gate winner: LF001 local sponsor bumper, score 6.34.
- LF001 maps the selected technique into concrete `camera`, `motion`,
  `environment`, and `grade` fields rather than leaving a broad retro label.

## Measured current image cost and QA

Source: [runs/2026-09-20/cli-price-test/REPORT.md](../../../runs/2026-09-20/cli-price-test/REPORT.md)

| Model | Task ID | Subject | Quality setting | Actual file | Credits | QA outcome |
|---|---|---:|---|---|---:|---|
| GPT Image 2.5 Flare | `425666878904818` | Product-only | 1080p/high | [Flare PNG](../../../projects/jevmax-gpt25-price-test/assets/images/425666878904818/pixverse_image_425666878904818_1789967534644.png) | 0 | Clean product-only image, but earbuds drifted onto sand instead of the towel |
| GPT Image 2.5 Sunburst | `425666880188252` | Product-only | 1080p/high | [Sunburst PNG](../../../projects/jevmax-gpt25-price-test/assets/images/425666880188252/pixverse_image_425666880188252_1789967559082.png) | 0 | Earbuds on textured towel, beach context, analog artifacts, no readable text |

Observed account delta for both successful tests: **0 credits**. The two output
files are local 720 x 1280 PNGs. Their SHA-256 records are:

- Flare: `5ae6d3352f0876902f8733c681136d62aa7abb3ef4a94633b2a8691e4074f235`
- Sunburst: `732f4a63b6d3d8e6112c188214e6e6a3bcaf148b4b8663374df49cc70c0b9a20`

The first Flare/Sunburst attempts that supplied the Ava swimwear seed as a
reference were moderation-rejected at 0 credits. The successful free route was
therefore product-only. These boards support style and product QA; they do not
replace or alter the approved Ava identity seed.

## Existing V6 identity-hold evidence

The package reuses the already-generated V6 file:
[V6 MP4](../../../projects/jevmax-lf001-v6-h3/assets/videos/425667939727864/pixverse_video_425667939727864_1789968093731.mp4).

| Measure | Value |
|---|---:|
| Task ID | `425667939727864` |
| Model | `v6` |
| Measured credits | 40 |
| Resolution | 720 x 1280 |
| Duration | 5.041667 seconds |
| Audio stream | absent |
| QA issues | 0 |

The machine report is
[pixverse V6 QA JSON](../../../projects/jevmax-lf001-v6-h3/quality/pixverse_video_425667939727864_1789968093731-qa.json).
Its latest-run scope checked two assets, passed two, and reported zero issues.
The V6-specific report confirms one video stream, no audio stream, the expected
9:16 aspect ratio, and four extracted sample frames.

Manual review recorded in the source report confirms that Ava remained seated,
identity and wardrobe held, the earbud cable stayed legible, no text card or
extra person appeared, and the retro production texture remained controlled.

## QA ledger

| Gate | Result | Evidence |
|---|---|---|
| Fictional identity | PASS | Both persona JSON contracts |
| No real-person likeness | PASS | Persona constraints and style-system safety rule |
| AI disclosure | PASS | `disclose_as_ai: true` in both persona contracts |
| Frozen character block | PASS | Verbatim-frozen wording in both persona contracts |
| Seed integrity | PASS | Local SHA-256 matches approved record |
| Identity hold | PASS | Existing V6 manual review and zero machine issues |
| Product legibility | PASS | Seed review and V6 cable-legibility review |
| No readable text | PASS | Current image boards and V6 review |
| Visual-grammar fit | PASS | LF001 score 6.34 and field mappings |
| Cost control | PASS | 0 package-generation credits; current GPT tests measured 0 |
| Client legal clearance | NOT INCLUDED | Explicit product exclusion |

## Limitations

1. Free GPT Image 2.5 cost is a measured promotion observation, not a permanent
   price guarantee.
2. The successful free image tests are product-only because person-reference
   attempts were moderation-rejected.
3. Identity hold is evidenced by one existing V6 render plus earlier Ava video
   review, not a randomized identity study.
4. No trademark clearance, talent clearance, legal opinion, or live media
   deployment is included.
5. The historical 25-credit seed route is retained as provenance; this product
   package did not generate a replacement seed.

