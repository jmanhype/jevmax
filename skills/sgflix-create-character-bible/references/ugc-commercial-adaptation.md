# Commercial UGC Adaptation for Character Bibles

When adapting the 8-page character bible process for brand/product UGC videos (instead of narrative or anime content):

## Key Differences from Narrative Work

- **Product Reference is Mandatory**: Always use Codex CLI with `-i <product-photo>` when generating pages that show the product (especially Pages 1, 5, and 7). Text prompts alone produce inconsistent bottle/packaging rendering.
- **Dual Reference Pattern**: For product interaction pages, pass both the original product photo and Page 1 (character) as `-i` references.
- **Page Priority**: Focus first on Pages 1 (hero), 5 (hands/details), and 7 (props/interaction) for product accuracy. Other pages can be generated later with text prompts + Page 1 as character anchor.
- **No Environment Bible Needed**: Unlike SGFLIX cinematic work, UGC benefits from natural variation in shooting locations. Do not over-constrain environments.

## Workflow Used Successfully (SugarLips Example)

1. Create base bible structure
2. Generate Page 1 with product photo as reference via Codex CLI
3. Generate Pages 5 and 7 using both product photo + Page 1 as dual references
4. Generate remaining pages (2, 3, 4, 6, 8) with text prompts referencing Page 1
5. Use resulting bible + product photo to generate per-scene first frames
6. Chain videos using first frames (Codex video generation or local Grok endpoint)

## Tunneling Note

When using `video_generate` tool with local first-frame images, expose them via Cloudflare Tunnel (`cloudflared tunnel --url http://localhost:XXXX`) to satisfy the HTTPS URL requirement.

This adaptation was developed during the SugarLips Vaginal Probiotic UGC project.