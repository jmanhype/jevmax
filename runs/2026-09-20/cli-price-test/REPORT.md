# CLI-only PixVerse price test — 2026-09-20

Scope: verify the current GPT Image 2.5 promotion on the CLI, then rerender
the LF001 concept once with V6 and once with MiniMax H3. The web UI was not
used.

## Account

- Plan: Pro
Starting balance for the successful image test: **10,825 credits**
Final balance after both videos: **10,635 credits**
Total video spend: **190 credits**

## GPT Image 2.5 price verification

### First attempt with the Ava reference

Two tasks attempted:

- `gpt-image-2.5-flare`
- `gpt-image-2.5-sunburst`

Both were rejected by PixVerse moderation (`audit_reject`) because the approved
Ava swimwear seed was supplied as a reference. Both failed tasks recorded
**0 credits**, and the account balance did not change.

Task IDs:

- Flare: `425666619053242`
- Sunburst: `425666712797627`

### Safe product-only retry

One bounded retry used the same 1986–1992 local sponsor-bumper style without a
person or reference image.

| Model | Task ID | Status | Credits | Output |
|---|---|---:|---:|---|
| `gpt-image-2.5-flare` | `425666878904818` | success | **0** | [Flare PNG](../../../projects/jevmax-gpt25-price-test/assets/images/425666878904818/pixverse_image_425666878904818_1789967534644.png) |
| `gpt-image-2.5-sunburst` | `425666880188252` | success | **0** | [Sunburst PNG](../../../projects/jevmax-gpt25-price-test/assets/images/425666880188252/pixverse_image_425666880188252_1789967559082.png) |

Measured result:

- Flare: **0 credits**
- Sunburst: **0 credits**
- Account delta: **0**

This confirms the current paid-member promotion: **GPT Image 2.5 Flare and
Sunburst are free through the CLI at the tested 1080p/high settings.**

### Visual comparison

**Flare** produced a clean product-only image, but placed the earbuds directly
on sand rather than on the requested towel.

**Sunburst** was closer to the brief: earbuds on a white textured towel,
beach background, visible horizontal analog artifacts, and no text.

No readable text appeared in either image.

## LF001 video rerenders

Both videos used:

- approved Ava seed as the identity/product reference
- same 5-second prompt
- 9:16 vertical output
- seed `0`
- strengthened final-frame no-text constraint

Prompt:
[regen.txt](../../../projects/jevmax-lf001-v6-h3/prompts/regen.txt)

### V6

| Measure | Value |
|---|---:|
| Model | `v6` |
| Quality | 720p |
| Resolution | 720×1280 |
| Duration | 5.0417s |
| Audio | disabled |
| Task ID | `425667939727864` |
| Credits | **40** |

Output:
[V6 MP4](../../../projects/jevmax-lf001-v6-h3/assets/videos/425667939727864/pixverse_video_425667939727864_1789968093731.mp4)

Visual review:

- Ava remained seated on the towel
- identity and wardrobe held
- earbud cable stayed legible
- no text card appeared
- no extra people appeared
- retro production texture was subtle rather than exaggerated

### MiniMax H3

| Measure | Value |
|---|---:|
| Model | `minimax-h3` |
| Quality | 768p |
| Resolution | 768×1344 |
| Duration | 5.167s |
| Audio stream | present |
| Task ID | `425668071427759` |
| Credits | **150** |

Output:
[H3 MP4](../../../projects/jevmax-lf001-v6-h3/assets/videos/425668071427759/pixverse_video_425668071427759_1789968240957.mp4)

Visual review:

- Ava identity and product remained recognizable
- no text card appeared
- major composition drift: Ava appeared standing in shallow water rather than
  seated on the towel
- H3 generated an AAC audio stream; audio content was not human-reviewed

## Price comparison

| Route | Quality | Duration | Measured credits |
|---|---:|---:|---:|
| GPT Image 2.5 Flare | 1080p/high | still | **0** |
| GPT Image 2.5 Sunburst | 1080p/high | still | **0** |
| V6 | 720p | 5s | **40** |
| MiniMax H3 | 768p | 5s | **150** |
| Seedance 2.5 | 1080p | 5s | **850** |

## Conclusion

For current tests, the measured CLI cost ladder is:

1. **GPT Image 2.5 Sunburst** for free image boards.
2. **V6 720p** for cheap motion tests at 40 credits.
3. MiniMax H3 only when its stronger generation quality justifies 150 credits.
4. Avoid Seedance 2.5 for routine exploration; one 5-second test cost 850.

V6 was the best cheap motion result in this run: it preserved the seed
composition, identity, towel, product, and no-text constraint for 40 credits.
