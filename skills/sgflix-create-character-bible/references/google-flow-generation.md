# Google Flow (Gemini Flow) — Character Bible Generation

Alternative generation path via `labs.google/fx/tools/flow` using ego-browser. Use when Codex is unavailable or for quick iteration.

## Setup
- URL: `https://labs.google/fx/tools/flow`
- Requires: Google account logged in via ego-browser (imports Chrome data)
- Model: 🍌 Nano Banana Pro
- Output: 4 images per prompt, ~25% failure rate (1 of 4 typically fails)

## Aspect Ratios
- **16:9 landscape** — default, used for pages 2, 4, 6, 7, 8
- **3:4 portrait** — used for pages 1, 3, 5

Switch ratio via the model selector dropdown BEFORE typing each prompt:
```js
// Open model menu
const modelMatch = snap.match(/button \[ref=(\d+)[^\]]*\]\s*\n\s*text "🍌 Nano Banana Pro"/)
await click('@' + modelMatch[1], { label: 'open model menu' })
await wait(2)

// Select ratio
const ratioMatch = snap2.match(/tab \[ref=(\d+)[^\]]*\]\s*\n\s*text "crop_portrait"\s*\n\s*text "3:4"/)
// OR for landscape: /tab \[ref=(\d+)[^\]]*\]\s*\n\s*text "crop_16_9"\s*\n\s*text "16:9"/
await click('@' + ratioMatch[1])
await pressKey('Escape')
```

## Generation Flow
```js
// 1. Navigate to project
await gotoAndWait('https://labs.google/fx/tools/flow/project/<PROJECT_ID>', { timeout: 15 })
await wait(3)

// 2. Fix viewport (required for backgrounded tabs)
await cdp('Emulation.setDeviceMetricsOverride', { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false })

// 3. Click prompt textfield and type
const tfMatch = snap.match(/textfield \[ref=(\d+)/)
await click('@' + tfMatch[1])
await typeText('Your prompt here...')

// 4. Click Create
const btnMatch = snap.match(/button \[ref=(\d+)[^\]]*\]\s*\n\s*text "arrow_forward"\s*\n\s*text "Create"/)
await click('@' + btnMatch[1])
await wait(25)  // ~25 seconds for generation
```

## Downloading Images — CRITICAL SPA PITFALL

Google Flow is a React SPA. **Navigating between `/edit/<id>` URLs does NOT update the rendered image.** The canvas keeps the previous image, producing identical downloads with matching MD5 hashes.

**Fix: Extract from project listing page thumbnails.**

```js
const { writeFile } = await import('fs/promises')

// Navigate to project listing (NOT individual edit URLs)
await gotoAndWait('https://labs.google/fx/tools/flow/project/<PROJECT_ID>', { timeout: 15 })
await wait(3)

// Extract by index from the img array on the listing page
const dataUrl = await js(String.raw`(() => {
  const imgs = document.querySelectorAll('img[src*="getMediaUrlRedirect"]');
  const filtered = [...imgs].filter(i => i.naturalWidth > 0);
  const img = filtered[TARGET_INDEX];  // 0 = newest, increments for older
  if (!img) return 'no image';
  const c = document.createElement('canvas');
  c.width = img.naturalWidth; c.height = img.naturalHeight;
  c.getContext('2d').drawImage(img, 0, 0);
  return c.toDataURL('image/jpeg', 0.95);
})()`)

if (dataUrl.startsWith('data:')) {
  const buf = Buffer.from(dataUrl.replace(/^data:image\/jpeg;base64,/, ''), 'base64')
  await writeFile('/path/to/save.jpg', buf)
}
```

### Image ordering on listing page
- Images appear newest-first
- Group by size to identify which batch they belong to (e.g., all 3:4 images are one batch)
- Use `naturalWidth`/`naturalHeight` to distinguish 16:9 (1376×768) from 3:4 (896×1200)

### Verification
Always verify uniqueness after download:
```bash
md5 /path/to/page_*.jpg
```
If any two files share the same hash, the SPA caching bug hit — re-download from the listing page.

## ESM Module Note
ego-browser runs as ESM. Use `await import('fs/promises')` not `require('fs')`. Mixing require and top-level await throws a module format error.

## img2img from Reference Image (THE ONLY RELIABLE PATH FOR CHARACTER BIBLES)

**Discovered June 19, 2026:** Text-to-image in Flow consistently gets iconic character accessories wrong (hats, mustaches, outfit layers). The @Character reference feature strips accessories entirely. The ONLY reliable approach is img2img from the reference image's edit page.

### Why text-to-image fails for character bibles
- Nano Banana Pro ignores specific accessory descriptions (hat construction, mustache style)
- Saying "mushroom-style cap with short brim, NOT a baseball cap" still produces baseball caps
- @Character references strip ALL accessories — every generated image had NO hat
- @ mention dropdown requires keyboard nav (ArrowDown + Enter); JS click/dispatch events/CDP clicks all fail on the contenteditable dropdown

### Workflow: Upload reference → img2img each page

```js
// STEP 1: Upload reference image to Flow project
// Navigate to project, click "Add Media"
const addMediaMatch = snap.match(/button \[ref=(\d+)[^\]]*\]\s*\n\s*text "add"\s*\n\s*text "Add Media"/)
await click('@' + addMediaMatch[1])
await wait(2)

// Upload via file input (accept="image/*")
await uploadFile('input[type="file"]', '/path/to/reference_image.png')
await wait(5)

// STEP 2: Navigate to reference image's edit page
// Get edit URLs from project listing
const editUrls = snap.match(/edit\/([a-f0-9-]+)/g)
// Navigate to the first (the uploaded reference)
await gotoAndWait('https://labs.google/fx/tools/flow/project/<PROJECT_ID>/' + editUrls[0], { timeout: 15 })
await wait(4)

// STEP 3: Type the page prompt as "what to change"
const tfMatch = snap.match(/textfield \[ref=(\d+)/)
await click('@' + tfMatch[1])
await typeText('Transform this into a freeze-frame from a 1995 Hi8 camcorder recording of this same character standing next to his go-kart...')
await wait(2)

// STEP 4: Generate
const createMatch = snap.match(/button \[ref=(\d+)[^\]]*\]\s*\n\s*text "arrow_forward"\s*\n\s*text "Create"/)
await click('@' + createMatch[1])
await wait(25)
```

### Key difference from text-to-image prompts
- Frame the prompt as "what to CHANGE" not "what to create"
- Reference character's accessories are preserved automatically by img2img
- You only need to describe the SCENE, POSE, ENVIRONMENT, and AESTHETIC — not the character's hat, outfit, or mustache

### Downloading img2img results
Same SPA pitfall applies. Download from project listing page via canvas toDataURL (see Downloading Images section above).

## Detail-Correction Pipeline: ImageMagick Bridge (June 19, 2026)

**Problem:** img2img preserves overall character shape but misses specific small details (letters, emblems, symbols on clothing). E.g., white "M" on Mario's cap is absent despite being in the prompt.

**Solution:** Paint the missing detail with ImageMagick, re-upload as new media, img2img from the corrected reference.

### Step-by-step

1. **Generate base via img2img** — get correct hat shape, composition, outfit
2. **Find target coordinates** using Z.ai vision:
   ```
   "This image is 1200x896 pixels. Give me the exact X,Y coordinates of the CENTER FRONT of the hat."
   ```
3. **Paint the detail** with ImageMagick:
   ```bash
   magick base_image.jpg \
     -font Helvetica-Bold -pointsize 36 \
     -fill white -stroke black -strokewidth 1 \
     -gravity NorthWest -annotate +748+210 "M" \
     corrected_with_M.jpg
   ```
4. **Upload corrected image** to Flow as new media:
   ```js
   await uploadFile('input[type="file"]', '/path/to/corrected_with_M.jpg')
   ```
5. **img2img from the corrected reference** — the painted "M" survives into the generation

### Why this works
Flow's img2img engine respects visual pixel details from the reference. A letter painted with ImageMagick at the correct coordinates becomes part of the reference image, and the model propagates it into the output. Text prompts alone cannot reliably place specific letters on specific objects.

### Tips
- Use `-stroke black -strokewidth 1` for contrast against colored backgrounds
- Adjust `-pointsize` based on target area size (use Z.ai vision to estimate pixel dimensions)
- Test on a single generation first — if the detail disappears, increase the painted size/contrast
- The painted detail doesn't need to look perfect — img2img will blend it naturally into the generation

## Prompt Adjustments for Flow (Text-to-Image Only)
Nano Banana Pro interprets prompts differently than gpt-image-2. Use these ONLY when text-to-image is unavoidable:
- Remove quotes around text that should appear in the image (e.g., use `VHS timestamp 14:22:03-1` not `"14:22:03-1"`)
- Be explicit about hat construction: "rounded mushroom-style cap with short small brim, NOT a baseball cap"
- Aspect ratio keywords in the prompt help: mention "portrait" for 3:4, "wide/landscape" for 16:9
- **Known limitation:** Even with explicit descriptions, the model often ignores accessory details. Prefer img2img.
