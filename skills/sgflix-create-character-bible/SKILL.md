---
name: sgflix-create-character-bible
description: Generate complete 8-page character bibles from scratch using gpt-image-2 with CHARACTER_IDENTITY_LOCK structure.
version: 2.0
---

# SGFLIX Create Character Bible

Generate complete 8-page character bibles from scratch using gpt-image-2 with CHARACTER_IDENTITY_LOCK structure.

## Description

Creates production-ready character bibles (8 pages) from character name and description using Codex gpt-image-2. Each bible includes CHARACTER_IDENTITY_LOCK for identity preservation and serves as the foundation for video generation.

## Capabilities

- Generate CHARACTER_IDENTITY_LOCK from character name/description
- Create 8-page character bible structure
- Use gpt-image-2 to generate each page
- Save organized bible with prompts and images
- Production-ready quality (8-9/10 fidelity)
- Support any anime character from any series

## Complete Pipeline

```
Character Name → CHARACTER_IDENTITY_LOCK → 8-Page Bible → gpt-image-2 → Reference Image → Factory Specs → Video → QC
```

## Usage

### Via Natural Language

**Most common - create bible from character name:**

```
"Create a character bible for Naruto Uzumaki from Naruto"
"Generate a character bible for Gon Freecss from Hunter x Hunter"
"Make a character bible for Luffy from One Piece"
```

**What happens:**
1. Analyzes character name and series
2. Generates CHARACTER_IDENTITY_LOCK
3. Creates 8-page prompt structure
4. Uses gpt-image-2 for each page
5. Organizes bible with images and prompts
6. Returns ready-to-use character bible

### Via Character Description

**With more details:**

```
"Create a character bible for a character named Sasuke Uchiha who is an avenger with spiky black hair, blue outfit, and fire techniques"
```

**What happens:**
- Extracts character details from description
- Builds CHARACTER_IDENTITY_LOCK
- Creates complete 8-page bible
- Generates images using gpt-image-2

### Via API

```bash
curl -X POST http://localhost:8648/api/hermes/media/sgflix-create-character-bible \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "character_name": "Naruto Uzumaki",
    "series": "Naruto Shippuden",
    "description": "Orange jumpsuit, spiky blond hair, whisker marks, ninja, Rasengan technique",
    "generate_pages": true
  }'
```

## 8-Page Bible Structure

Each character bible contains 8 pages with specific prompts:

### Page 1: PRIMARY_HERO_REFERENCE (3:4)
**Purpose:** Main character reference with full identity lock
**Content:** Full-body character design, signature pose, primary visual elements

### Page 2: ORTHOGRAPHIC_TURNAROUND
**Purpose:** Front, side, back views for 3D understanding
**Content:** 360° character rotation, consistent design

### Page 3: MORPHOLOGY_PROPORTIONS_SILHOUETTE
**Purpose:** Body type, proportions, silhouette
**Content:** Morphology details, proportions, character class silhouette

### Page 4: EXPRESSION_EMOTION_SHEET
**Purpose:** Facial expressions and emotions
**Content:** Range of expressions (happy, sad, angry, determined, etc.)

### Page 5: CRANIAL_APPENDAGE_DETAILS
**Purpose:** Head, hands, feet details
**Content:** Close-up views of key extremities and features

### Page 6: SURFACE_TREATMENT_CONSTRUCTION
**Purpose:** Clothing, materials, textures
**Content:** Surface details, fabric textures, material properties

### Page 7: EXTREMITIES_PROPS_ACCESSORIES
**Purpose:** Weapons, props, accessories
**Content:** Character's signature items and props

### Page 8: MATERIALS_COLOR_RIGGING_MOTION
**Purpose:** Color palette, rigging, motion range
**Content:** Full color specification, rigging guides, motion constraints

## CHARACTER_IDENTITY_LOCK Structure

Each bible includes identity locks for:

```yaml
CHARACTER_IDENTITY_LOCK:
  name: Character Name
  character_class: humanoid
  age_cohort: age-appropriate description
  species: Human/demon/spirit/etc.
  role: hero/villain/side character/etc.
  
  morphology_lock: body type, posture, build
  cranial_lock: hair, facial features, expressions
  surface_lock: clothing, accessories, materials
  appendage_lock: limb count, extremities
  accessory_prop_lock: signature items/props
  chromatic_lock: primary/secondary colors
  material_lock: material types
  style_lock: art style (anime, manga, etc.)
  
  signature_visual_hooks: key visual identifiers
  DO_NOT_CHANGE: core identity elements
  BOUNDED_VARIATION: allowed variations
```

## Bible Generation Process

### Step 1: Analyze Character
**Input:** Character name + series/description
**Process:**
- Extract character identity
- Build CHARACTER_IDENTITY_LOCK
- Define morphology, cranial, surface locks
- Identify signature visual hooks

### Step 2: Generate Page Prompts
**Process:**
- Create 8 page prompts using templates
- Each prompt includes:
  - CHARACTER_IDENTITY_LOCK
  - Page-specific instructions
  - DO_NOT_CHANGE constraints
  - BOUNDED_VARIATION allowances
  - Presentation constraints

### Step 3: Generate Images
**Tool:** Codex gpt-image-2 via CLI
**Process:**
- Generate page 01 first (primary hero reference)
- Use page 01 as `-i` reference for ALL remaining pages (2-8)
- Each page takes ~5 minutes
- Save to `images/page_XX_name.png`
- Save prompt to `prompts/page_XX_name.md`

**Command:**
```bash
# Page 01 (no reference)
codex exec --skip-git-repo-check -m gpt-image-2 -- "$(cat /tmp/page1.txt)"

# Pages 2-8 (with page 01 as reference for identity consistency)
codex exec --skip-git-repo-check -m gpt-image-2 \
  -i /path/to/images/page_01_primary_hero_reference.png \
  -- "$(cat /tmp/page2.txt)"
```

### Step 4: Organize Bible
**Structure:**
```
bibles/{project_name}/{character_name}/
├── identity_lock.yaml
├── all_8_prompts.md
├── prompts/
│   ├── page_01_primary_hero_reference.md
│   └── ... (pages 2-8)
└── images/
    ├── page_01_primary_hero_reference.png
    └── ... (pages 2-8)
```

### Step 5: QC Validate
**Process:**
- Verify all 8 pages generated (check file sizes, all should be 1.5-2.5MB)
- Run `md5` on all pages — ALL must have unique hashes (detects duplicate cascade)
- Check identity lock consistency across pages
- Validate character fidelity
- Score overall quality (target: 8-9/10)

## Example Usage

### Example 1: Naruto Uzumaki

**In Web UI:**
```
"Create a character bible for Naruto Uzumaki from Naruto Shippuden"
```

**What happens:**
1. Analyzes: Naruto Uzumaki, ninja, orange jumpsuit, spiky blond hair, whisker marks
2. Generates CHARACTER_IDENTITY_LOCK
3. Creates 8 page prompts
4. Generates 8 images using gpt-image-2
5. Organizes bible structure
6. Returns: Ready-to-use character bible

### Example 2: Custom Character

```
"Create a character bible for a character named Zara who is a lightning mage with silver hair flowing up, yellow and black armor, and electric aura"
```

## Quality Targets

**Character Fidelity:**
- Morphology: 9/10 (body type, posture, silhouette)
- Cranial: 8/10 (hair, facial features, expression)
- Surface: 9/10 (clothing, accessories, colors)
- Overall: 8-9/10 (production-ready)

**Consistency:**
- All 8 pages maintain same identity
- CHARACTER_IDENTITY_LOCK preserved across pages
- Signature visual hooks consistent
- DO_NOT_CHANGE elements respected

## Integration with Video Generation

**After creating character bible:**

```
"Generate a video of Naruto using his Rasengan attack"
```

**What happens:**
1. Reads newly created character bible
2. Uses page_01 as reference image
3. Creates factory specs (CHAI, scene JSON, handoffs, QC)
4. Generates video with 8.5/10 fidelity
5. Returns video + QC report

## Batch Bible Creation

**Create multiple character bibles:**

```
"Create character bibles for Naruto, Sasuke, Sakura, and Kakashi from Naruto"
```

**What happens:**
- Processes 4 characters in parallel
- Each: CHARACTER_IDENTITY_LOCK → 8 pages → images
- Returns: 4 complete character bibles
- Ready for batch video generation

## Notes

- **gpt-image-2 required:** Codex App Server must be running on port 9100. ALWAYS use `-m gpt-image-2`, never gpt-image-1 for bible generation.
- **Quality targets:** 8-9/10 character fidelity
- **Identity preservation:** CHARACTER_IDENTITY_LOCK ensures consistency
- **Production-ready:** Bibles ready for video generation pipeline
- **Any character:** Works for any anime/manga character

## From Bible to Scene Generation (Prompt Forge img2img)

After creating a character bible, the next step is generating scenes. Use the Prompt Forge img2img pipeline:

1. Generate a strong scene image first using Codex gpt-image-2 (with both characters, environment, action)
2. Use THAT scene image as the reference for Prompt Forge img2img (not a bible page)
3. Winning formula: `denoise: 0.85, lora_strength: 0.3, lora: ektachrome_style_v1.safetensors`
4. This produces 9/10 quality with character consistency

**Why scene images work better than bible pages as references:**
- Bible pages are posed/stiff (T-pose, orthographic) — they don't carry scene context
- A scene image has the character in action, with vehicles, environment, props
- Prompt Forge img2img preserves the scene context while generating new angles/moments

**DOUBLE-DEGRADATION PITFALL (June 16, 2026 discovery):**
When the reference image already has found footage/VHS artifacts (grain, desaturation, timestamp overlays), img2img causes "double-degradation":
1. Reference image has VHS artifacts (intentional aesthetic)
2. img2img encodes those degraded pixels through VAE → compresses artifacts
3. Model tries to preserve reference → keeps the degradation
4. Prompt asks for MORE found footage look → adds another layer of grain/noise
5. Ektachrome LoRA adds film grain on top of VHS grain → muddy mess

**Result:** 3/10 quality, washed-out, unclear garbage.

**The fix:** For found footage aesthetics, use txt2img (denoise: 1.0, no reference image) with the 13-rule system prompt + Ektachrome LoRA at 0.6 strength. This produces 9/10 quality because it starts CLEAN and generates the found footage look in one shot — no fighting against reference artifacts.

**When img2img DOES work:**
- Clean reference images (bible pages, high-quality character art)
- Non-degraded aesthetics (photoreal, anime, illustration)
- denoise 0.6-0.7 (tight to reference) OR denoise 0.95 (mostly free)
- Never denoise 0.85 with degraded references — worst possible zone where reference and generation fight each other

See `ideogram-4-json-prompting` → `references/found-footage-img2img-workflow.md` for the full workflow.

## Pitfalls

### Usage Limits
Codex has daily usage limits that reset at 1:52 AM. Batch generation of 15-16 images can hit the limit. Plan batches to complete within the limit window, or split across multiple days.

### Reference Image Flag
When using reference images for consistency, the flag is `-i` not `--image`:
```bash
codex exec --skip-git-repo-check -m gpt-image-2 -i /path/to/reference.png -- "prompt"
```
This is CRITICAL for maintaining character identity across all 8 pages.

### Output Location
Codex saves images to `~/.codex/generated_images/<session-id>/` — they must be manually copied to your bible directory. The tool cannot save directly to arbitrary paths.

### Shell Escaping
Prompts with parentheses or special characters will fail with shell escaping errors. Write prompts to temp files first:
```bash
cat > /tmp/page1.txt << 'EOF'
Your prompt here with (parentheses)
EOF
PROMPT=$(cat /tmp/page1.txt)
codex exec --skip-git-repo-check -m gpt-image-2 -i ref.png -- "$PROMPT"
```

## Output

**Generated files:**
- `identity_lock.yaml` - Character identity specification
- `all_8_prompts.md` - Master prompt file
- `prompts/*.md` - 8 individual page prompts
- `images/*.png` - 8 generated character images
- Ready for use in video generation pipeline

## Kling 3.0 Integration

After generating a bible, the best pages for Kling Element upload are:
1. Page 01 (Primary Hero) - main identity anchor
2. Page 02 (Turnaround) - multiple angles
3. Page 04 (Expressions) - face variety
4. Page 05 (Details) - close-up features

Upload these 4 pages to Kling as a single Element to create the @EntityName anchor.

## Multi-Entity Projects

When a project has multiple characters:
1. Generate bibles in priority order (lead characters first)
2. Use the lead character's page_01 as reference (-i flag) when generating supporting characters to maintain world consistency
3. Create entity registry after all bibles are complete
4. Each entity gets its own Kling Element upload

Priority levels:
- **full 8-page**: Lead characters, characters with significant screen time
- **simplified 4-page**: Supporting characters (pages 01, 02, 04, 07 only)
- **reference only**: Background characters (page 01 only)

## PERIOD STOCK (Mandatory for ALL pages)

Every image generated by this skill MUST be framed as a photograph or footage captured on a SPECIFIC device from a SPECIFIC era. Do NOT describe it as 'concept art' or 'design sheet with texture.' Instead, frame the entire prompt as: 'A photograph taken on [device] at [time/place].'

The key insight: saying 'a photograph taken on an iPhone 15 Pro at 2:47 AM' produces photorealistic results. Saying 'apply iPhone texture to concept art' produces garbage.

### How to apply:
- Frame the prompt as a REAL PHOTO or REAL FOOTAGE captured on the period-appropriate device
- The device/stock determines ALL texture characteristics automatically
- Do NOT add texture keywords separately — the device name IS the texture

### Period Stock Reference Table:

| Era/Context | Device/Stock | How to frame the prompt |
|-------------|-------------|------------------------|
| 2020s found footage | iPhone 15 Pro night mode | 'A photograph taken on an iPhone 15 Pro at 2 AM in the rain' |
| 2010s CCTV | Hikvision IP camera | 'Security camera footage from a Hikvision DS-2CD2143 at 12:03 AM' |
| 2020s bodycam | Axon Body 3 | 'Bodycam footage from an Axon Body 3 during a night patrol' |
| 2004 reality TV | Panasonic DVX100 | 'Shot on a Panasonic DVX100 in 24p mode, available light only' |
| 1998 public-access | Canon XL1 MiniDV | 'Recorded on a Canon XL1 in a community center' |
| 1995 amateur documentary | Sony Handycam Hi8 | 'A freeze-frame from a 1995 Hi8 camcorder recording' |
| 1970s Grindhouse | 35mm Eastmancolor worn print | 'A frame from a worn 35mm Eastmancolor print, projected in a drive-in' |
| 1970s Giallo | 35mm Eastmancolor | 'A still from a 1974 Italian thriller shot on Eastmancolor stock' |
| 1960s NASA | 16mm Kodak Ektachrome | 'A frame from a 1966 NASA 16mm Ektachrome educational reel' |
| 1980s VHS | VHS 3rd-gen dub | 'A freeze-frame from a 3rd-generation VHS dub recorded off late-night TV' |
| 1990s anime OVA | Cel + 35mm optical | 'A frame from a 1993 OVA cel-animated production printed on 35mm' |

### Aging Scale:
- Fresh: How it looked when first captured
- Light: Slight wear from normal use
- Moderate: Years of storage, visible degradation
- Heavy: Damaged, partially destroyed
- Found: Barely surviving, recovered from disaster

## Pitfalls (Production-Tested)

**HAT/ACCESSORY SPECIFICITY — the #1 prompt failure for iconic characters.**
Saying "red baseball cap with white M" generates a regular baseball cap with a long curved brim. For Mario, the correct hat is a **rounded mushroom-style cap with a very short small brim** — completely different construction. Always describe hat CONSTRUCTION, not just color+letter:
```
WRONG: "faded red baseball cap with white M embroidered on front"
RIGHT: "faded red rounded mushroom-style cap with short small brim/visor (NOT a baseball cap), white bold M on front"
```
This applies to ANY iconic headwear — always specify dome vs brim, structured vs unstructured, fitted vs adjustable. The model defaults to the most common interpretation (baseball cap) unless you explicitly exclude it.

**1. ALWAYS use a reference image with `-i` flag for consistency.**
Generate page 01 first, then pass it as `-i` for all subsequent pages:
```bash
codex exec --skip-git-repo-check -m gpt-image-2 \
  -i /path/to/character/images/page_01_primary_hero_reference.png \
  -- "prompt for page 02..."
```
Without `-i`, pages 2-8 will drift from the page 01 identity. The user will catch this immediately.

**2. DUPLICATE CASCADE — the #1 batch script failure mode.**
When generation fails (usage limit, timeout, safety filter), `find ~/.codex/generated_images | ls -t | head -1` returns the LAST SUCCESSFUL image. The script copies that same image to the new path, creating identical duplicates. In production: Sweet Tooth pages 2-8 were all the same MD5 hash.

**Fix — track before/after image count:**
```bash
generate_page() {
    local prompt_file="$1"
    local output_path="$2"
    before_count=$(find ~/.codex/generated_images -name "*.png" 2>/dev/null | wc -l)
    PROMPT=$(cat "$prompt_file")
    codex exec --skip-git-repo-check -m gpt-image-2 -i "$REF_IMAGE" -- "$PROMPT" 2>&1 | tail -5
    sleep 2
    after_count=$(find ~/.codex/generated_images -name "*.png" 2>/dev/null | wc -l)
    if [ "$after_count" -gt "$before_count" ]; then
        latest=$(find ~/.codex/generated_images -name "*.png" -print0 | xargs -0 ls -t | head -1)
        cp "$latest" "$output_path"
        echo "Saved: $output_path"
    else
        echo "FAILED: No new image — skipping (no duplicate)"
    fi
}
```
**Always verify with `md5` after batch completes — all 8 pages should have unique hashes.**

**3. Usage limits kill batches silently.**
Codex free tier has daily limits. If you hit the limit mid-batch, ALL remaining generations fail but the script keeps running. Add a check:
```bash
output=$(codex exec ... 2>&1)
if echo "$output" | grep -q "usage limit"; then
    echo "USAGE LIMIT HIT — aborting batch"
    exit 1
fi
```

**4. Write prompts to /tmp/*.txt files — never inline.**
Prompts with parentheses, quotes, apostrophes break shell parsing:
```bash
cat > /tmp/page2.txt << 'EOF'
A freeze-frame from a 1995 Hi8 camcorder recording...
EOF
PROMPT=$(cat /tmp/page2.txt)
codex exec ... -- "$PROMPT"
```

**5. Generation takes ~5 minutes per image — not 2-3 minutes.**
Set timeout to 600s+. Do not report "timeout" or "failure" without checking `~/.codex/generated_images/` for actual output.

**6. vision_analyze HALLUCINATES image content.**
The built-in vision_analyze tool describes completely wrong content for generated images. Use Z.ai vision MCP wrapper for QC, or just open images for the user to judge.

**7. MANDATORY: Load this skill BEFORE attempting any bible generation.**
If the user asks to "create a character bible", load this skill immediately. Do not write bibles from scratch without following the 8-page structure and CHARACTER_IDENTITY_LOCK format defined here. The user has corrected this multiple times.

**8. QC REFERENCE COMPARISON — always cross-check against the reference image.**
After generating all 8 pages, audit each page against the original reference image (e.g. `ep1_found_footage_mario_vs_sweettooth.png`) for iconic accessories. Use Z.ai vision MCP wrapper to compare specific elements:
- Hat type and construction (dome vs brim, snapback vs fitted)
- Mustache style (handlebar vs other)
- Outfit layers (shirt + overalls, not just a t-shirt)
- Gloves, boots, props
The user WILL catch wrong accessories. Don't assume the model got it right — verify every iconic element.

**9. GOOGLE FLOW (Gemini Flow) — use img2img from reference, NEVER text-to-image for character bibles.**
When Codex is unavailable or for quick iteration, use Google Flow at `labs.google/fx/tools/flow` via ego-browser.

**CRITICAL (June 19, 2026): Text-to-image in Flow consistently gets iconic character accessories WRONG.**
- All 8 pages of a Mario bible generated with text prompts produced baseball caps instead of Mario's dome cap, despite explicit prompt language ("mushroom-style cap with short small brim, NOT a baseball cap")
- The model defaults to the most generic interpretation regardless of prompt specificity
- @Character references in Flow STRIP accessories entirely — every image had NO hat

**The ONLY reliable path: img2img from the reference image's edit page.**
1. Upload reference image to Flow project via "Add Media" → file upload (`uploadFile('input[type="file"]', path)`)
2. Navigate to the reference image's edit page (`/project/<id>/edit/<image-id>`)
3. Type the page prompt as "what to change" — the img2img engine preserves the reference character's accessories
4. Generate and download from the project listing page

**Verified:** img2img from `ep1_found_footage_mario_vs_sweettooth.png` produced correct Mario dome cap on all outputs. Text-only produced baseball caps on all outputs.

**DETAIL-GAP FIX (June 19, 2026): ImageMagick paint → re-upload → img2img.**
When img2img preserves the overall shape but misses a specific detail (e.g. white "M" on the cap), use this bridge:
1. Generate base via img2img → correct hat shape, missing M
2. Paint the detail with ImageMagick:
   ```bash
   magick input.jpg -font Helvetica-Bold -pointsize 36 -fill white -stroke black -strokewidth 1 \
     -gravity NorthWest -annotate +748+210 "M" output_with_m.jpg
   ```
3. Upload the painted image as new media (Add Media → uploadFile)
4. Img2img from the painted reference → M survives into the generation
This works because Flow's img2img propagates visual details from the reference that text prompts cannot produce. Use Z.ai vision to find pixel coordinates of the target area before painting.

See `references/google-flow-generation.md` for the full img2img workflow, upload technique, and SPA download pattern.

## Batch Generation Pitfalls

When generating 8-page bibles in batch, watch for these failure modes:

### Silent Generation Failures → Identical Images
When Codex generation fails silently (network timeout, rate limit, error), the batch script may copy the same "latest" image multiple times, resulting in all pages having identical MD5 hashes.

**Verification**: Always check MD5 hashes after batch generation:
```bash
md5 /Users/speed/bibles/.../images/page_*.png | awk '{print $4, $1}'
```
If pages 2-8 all have the same hash as page 1, the batch failed.

**Fix**: Track image count before/after each generation instead of just grabbing "latest":
```bash
before_count=$(find ~/.codex/generated_images -name "*.png" 2>/dev/null | wc -l)
# ... generate ...
after_count=$(find ~/.codex/generated_images -name "*.png" 2>/dev/null | wc -l)
if [ "$after_count" -gt "$before_count" ]; then
  # success, copy newest
fi
```

### Codex Usage Limits
gpt-image-2 has daily usage limits. After ~15 images, you'll hit:
```
ERROR: You've hit your usage limit. Upgrade to Pro or try again at [timestamp].
```

**Mitigation**: 
- Generate Mario bible first, then Sweet Tooth
- Spread generation across multiple sessions if needed
- Check usage at https://chatgpt.com/codex/settings/usage

### Shell Escaping with Long Prompts
Long prompts with quotes, parentheses, and special characters break bash quoting. Workaround: write prompts to temp files.

```bash
# Write prompt to file
cat > /tmp/mario_page1.txt << 'EOF'
Generate image: A freeze-frame from a 1995 Hi8 camcorder recording...
EOF

# Use in codex command
PROMPT=$(cat /tmp/mario_page1.txt)
codex exec --skip-git-repo-check -m gpt-image-2 -- "$PROMPT"
```

### Reference Image with `-i` Flag
For character consistency across all 8 pages, use the Codex `-i` flag to pass a reference image:

```bash
codex exec --skip-git-repo-check -m gpt-image-2 \
  -i /path/to/reference_image.png \
  -- "Generate image: [prompt]..."
```

This ensures all pages maintain the same character identity (costume, vehicle, aesthetic) from the reference.

## See Also

- `sgflix-poster-first-validate` - Poster validation gate (use this before creating character bibles)
- `sgflix-character-video` - Video generation using character bibles
- `sgflix-qc-validate` - QC validation system
- `sgflix-batch-produce` - Batch processing
- `codex-image-with-references` - Detailed Codex CLI patterns, shell escaping, batch scripts
- `references/character-lock-database.md` - Scale generation to 3000+ images using STYLE PREFIX + CHARACTER LOCK formula (no LoRA needed)
