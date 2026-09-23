# Found Footage Character Bible — Mario vs Sweet Tooth (June 16, 2026)

## Validated Workflow

This session produced a complete 2-character, 16-page found footage character bible using:
- **Reference image:** `ep1_found_footage_mario_vs_sweettooth.png` (generated via Codex CLI gpt-image-1)
- **Period stock:** "A freeze-frame from a 1995 Hi8 camcorder recording"
- **Model:** gpt-image-2 with `-i` reference flag
- **Output:** `/Users/speed/bibles/mario_vs_sweettooth_found_footage/`

## Key Pattern: Scene Image as Universal Reference

The user provided a SCENE image (Mario + Sweet Tooth racing on a dirt track) and wanted it used as the `-i` reference for ALL bible pages of BOTH characters. This is different from the standard "generate page 01, use it for pages 2-8" pattern.

```bash
REF_IMAGE="/path/to/scene_image.png"

# ALL pages use the scene image, not page 01
for page in 1 2 3 4 5 6 7 8; do
    PROMPT=$(cat /tmp/mario_page${page}.txt)
    codex exec --skip-git-repo-check -m gpt-image-2 -i "$REF_IMAGE" -- "$PROMPT"
done
```

**Why this works:** The scene image contains BOTH characters, their vehicles, the environment, and the aesthetic. It's richer context than a single character's page 01.

## Characters

### Mario
- Italian-American man, 5'6", compact muscular build
- Faded red baseball cap with white "M" patch
- Red long-sleeve cotton shirt, blue denim work overalls
- White cotton gloves caked in mud
- Thick black handlebar mustache (costume-grade)
- Vehicle: Battered red-and-white go-kart, hand-painted "1", "Mario's Plumbing"

### Sweet Tooth
- Large muscular man, 6'2", heavy build
- White hockey mask with red flame decals (spray-painted)
- Black t-shirt (sleeves cut off), black cargo pants, black combat boots
- Black fingerless gloves, shaved head with flaming skull tattoo
- Vehicle: 1980s ice cream truck, rusted white, "SWEET TOOTH" spray-painted, welded scrap armor, broken jingle speaker

## Aesthetic Rules (Found Footage)
- PERIOD STOCK: "Recorded on a Sony Handycam Hi8 in 1995"
- VHS timestamp overlay in bottom-left corner (HH:MM:SS-X format)
- Flat natural lighting (no cinematic drama)
- Low resolution, grainy, authentic amateur quality
- Real mud, real costumes, cheap props
- Overcast sky, no sun, no shadows
- Color palette: muted browns, grays, overcast whites, character accent colors

## Prompt Structure Example (Page 1)
```
A freeze-frame from a 1995 Hi8 camcorder recording of an underground go-kart
racer standing next to his battered red-and-white go-kart on a muddy dirt track.
The racer is an Italian-American man, 5 foot 6, compact muscular build, wearing
a faded red baseball cap with a white "M" patch, red long-sleeve cotton shirt
stained with mud, blue denim work overalls with a worn leather belt, and white
cotton gloves caked in dried mud. He has a thick black handlebar mustache
(costume-grade, slightly crooked). Full body visible head to toe, standing in a
confident stance with one hand on his hip and the other resting on the kart
steering wheel. His go-kart is a real racing chassis — red and white paint
chipped and mud-splattered, exposed engine, hand-painted number "1" on the side,
"Mario's Plumbing" faded text on the rear panel. Overcast sky, flat natural
lighting. VHS timestamp overlay "16:42:08-1" in bottom-left corner. Low
resolution, authentic found footage quality. Amateur documentary style.
```

## File Structure
```
bibles/mario_vs_sweettooth_found_footage/
├── mario/
│   ├── identity_lock.yaml
│   ├── all_8_prompts.md
│   ├── prompts/
│   └── images/
│       ├── page_01_primary_hero_reference.png
│       ├── page_02_orthographic_turnaround.png
│       ├── page_03_morphology_proportions_silhouette.png
│       ├── page_04_expression_emotion_sheet.png
│       ├── page_05_cranial_appendage_details.png
│       ├── page_06_surface_treatment_construction.png
│       ├── page_07_extremities_props_accessories.png
│       └── page_08_materials_color_rigging_motion.png
└── sweet_tooth/
    ├── identity_lock.yaml
    ├── all_8_prompts.md
    ├── prompts/
    └── images/
        └── (same 8 pages)
```

## From Bible to Scene Generation

After creating the bible, use Prompt Forge v2 img2img for scene generation:

```bash
curl -X POST http://localhost:7861/generate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "New scene description...",
    "reference_image": "/path/to/ep1_found_footage_mario_vs_sweettooth.png",
    "denoise": 0.85,
    "lora": "ektachrome_style_v1.safetensors",
    "lora_strength": 0.3
  }'
```

## Lessons Learned

1. **Scene images > bible pages as references.** The user explicitly wanted the found footage scene image used for ALL pages. It carries more context than any individual bible page.

2. **Found footage aesthetic does NOT benefit from high LoRA strength.** Ektachrome LoRA at 0.8 fights the VHS aesthetic. Keep it at 0.3 or skip entirely.

3. **img2img double-degradation.** When the reference already has grain/degradation, img2img adds another layer. Use low LoRA + high denoise to let the model regenerate the aesthetic from scratch.

4. **Usage limits hit at ~15 images per day.** Plan batches accordingly. Mario (8 pages) + Sweet Tooth (8 pages) = 16 images, which is right at the limit.

5. **All prompts are saved at:** `/Users/speed/launch_pdfs/ALL_PROMPTS_MARIO_SWEETTOOTH.md`
