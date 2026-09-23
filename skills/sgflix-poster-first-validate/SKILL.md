---
name: sgflix-poster-first-validate
description: Validate a concept by generating one cinematic movie poster (era-accurate film stock, 27:40) and scoring it with the 5-criteria Cannon Films test (Glance, Thumbnail, Buy, Era, Uniqueness). 5/5 GREENLIT proceeds to character bible production, 4/5 CONDITIONAL regenerates, 3/5 or below KILLED before wasting generation credits. Use when a new concept or premise is proposed, or on "poster test", "Cannon test", "validate" requests.
version: 1.0
---

# SGFLIX Poster-First Validate

Validate concepts by generating a single explosive poster image before committing to full character bible production. Based on Cannon Films rule: "Sell the poster first. Make the movie after."

## Description

Generates cinematic movie poster from concept/premise and applies Cannon Films validation test. If concept sells in one image, greenlit for character bible. If not, killed before wasting production time.

## Pipeline

```
Concept → Poster Generation → Cannon Test → GREENLIT → Character Bible
                                          → KILLED → New concept
```

## Usage

**Natural Language:**
```
"Poster test: A 1970s blaxploitation revenge film about a Harlem numbers runner"
"Cannon test: 1990s OVA cyberpunk assassin in Neo-Tokyo"
"Validate: Grindhouse film about woman hunting corrupt cops"
```

**API:**
```bash
curl -X POST http://localhost:8648/api/hermes/media/sgflix-poster-first-validate \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "concept": "1970s blaxploitation revenge film",
    "era": "1970s",
    "genre": "blaxploitation",
    "title": "THE NUMBERS MAN",
    "tagline": "He counted their money. Now he counts their days."
  }'
```

## Poster Generation Rules

**Aspect Ratio Lock:**
- Standard: `27:40` (movie poster)
- Alternative: `2:1` (wide teaser)

**Required Elements:**
1. Title — Large, readable, era-appropriate typography
2. Tagline — One-line hook
3. Key Visual — Single explosive image selling the concept
4. Negative Space — Bottom 15% for billing block
5. Color Palette — Era-specific

**Film Stock Rules:**
- 1970s: Heavy grain, warm tones, halation
- 1980s: Airbrush illustration, neon accents
- 1990s: High contrast photographic
- 2000s: Desaturated digital, teal grade

**PERIOD STOCK (Mandatory Field):**

Do NOT say 'add grain' or 'make it look old.' Instead, name the EXACT camera/film/format that would have actually been used for this type of production in this era. The texture comes from specifying the real technology, not from generic filter language.

| Era/Context | Actual Stock | What It Looks Like |
|-------------|-------------|-------------------|
| 1950s Soviet documentary | 35mm ORWO/Svema B&W | Heavy contrast, chemical grain, slight fog |
| 1960s NASA educational | 16mm Kodak Ektachrome | Clean but textured, slight cyan shift, high contrast |
| 1960s Italian cinema | 35mm Technicolor/Eastmancolor | Rich saturated, slight color bleed at edges |
| 1970s Grindhouse/Drive-in | 35mm Eastmancolor (worn print) | Heavy grain, warm bleed, halation, scratches, splice marks |
| 1970s Giallo | 35mm Eastmancolor | Saturated colors bleeding, deep blacks, halation on practicals |
| 1970s Bollywood | 35mm Eastmancolor (Indian lab) | Vivid but slightly muddy, warm shift, heavy grain |
| 1978 British TV | 16mm Kodak 7247 | Soft, slightly overexposed highlights, warm grain |
| 1980s VHS rental | VHS (3rd generation dub) | Tracking noise, color smear, soft edges, tape roll |
| 1980s broadcast TV | 1-inch Type C videotape | Clean but flat, slight lag on fast motion |
| 1983 Soviet industrial | 16mm Svema DS-5M | Dusty, underexposed, chemical staining, cyan shift |
| 1986 local TV commercial | 3/4-inch U-matic | Soft, oversaturated, slight halo on bright objects |
| 1988 direct-to-video | Super VHS / 16mm blowup | Sharper than VHS but still soft, visible gate weave |
| 1990s anime OVA | Cel + 35mm optical print | Cel dust, registration wobble, rich blacks |
| 1992 Hong Kong action | 35mm Fuji Eterna | High contrast, slightly cool, fast-stock grain |
| 1994 kids broadcast | Betacam SP | Clean, bright, slightly flat, broadcast-safe colors |
| 1995 European documentary | Super 16mm Kodak Vision | Organic grain, natural color, slight warmth |
| 1998 public-access cable | Consumer DV (Canon XL1) | Compression blocks, auto-exposure shifts, flat |
| 1999 late-night cable animation | Digital ink + NTSC broadcast | Flat color, interlace artifacts, cable compression |
| 2001 early digital cinema | MiniDV / DVCam | Sharp but harsh, no film grain, clinical |
| 2002 BBC drama | Digi-Beta / early HD | Clean but slightly cold, institutional |
| 2004 reality TV | Panasonic DVX100 | 24p film-like but digital, slight motion judder |
| 2005 low-budget digital anime | Flash/Toon Boom + MPEG compression | Flat, banded gradients, stiff |
| 2010s CCTV | IP camera H.264 | Compression blocks, low framerate, IR blowout |
| 2020s bodycam | Axon Body 3 wide-angle | Fisheye, aggressive auto-exposure, motion blur |

**Aging/Degradation Scale (separate from stock):**

After choosing the period stock, optionally add degradation based on how the media would look TODAY:
- Fresh print: How it looked on release day
- Light aging: Slight color fade, minor dust
- Moderate aging: Scratches, color shift, splice marks, gate weave
- Heavy aging: Water damage, chemical staining, missing frames, warped audio
- Found footage: Barely surviving, extreme damage, partial image loss

**Format in prompt:**
PERIOD STOCK: [exact stock name]
AGING: [fresh / light / moderate / heavy / found]

## POSTER_PROMPT Template

```
Generate a cinematic movie poster:
ASPECT_RATIO: 27:40
ERA: [decade + subgenre]
TITLE: "[TITLE]" — large, readable, era-appropriate
TAGLINE: "[Hook]"
KEY VISUAL: [Subject, composition, lighting, palette]
NEGATIVE SPACE: Bottom 15% for billing block
FILM STOCK: [Era-specific texture]
AVOID: AI text gibberish, generic composition, modern cleanliness on period pieces, cluttered layouts
```

## Cannon Films Validation Test (5 Criteria)

1. **Glance Test** — Understand genre/tone/premise in under 2 seconds?
2. **Thumbnail Test** — Read at phone-screen size?
3. **Buy Test** — Would someone click/watch based on this image alone?
4. **Era Test** — Authentically feel like poster FROM that era?
5. **Uniqueness Test** — Distinct from existing SGFLIX runs?

**Scoring:**
- 5/5 = GREENLIT → Proceed to character bible
- 4/5 = CONDITIONAL → Regenerate with adjustments
- 3/5 or below = KILLED → Concept not strong enough

## Post-Validation

**If GREENLIT:**
1. Extract characters from poster
2. Trigger `sgflix-create-character-bible`
3. Create world bible
4. Generate factory specs

**If KILLED:**
1. Document failure reasons
2. Archive poster
3. Try new premise

## Notes

- gpt-image-2 required (Codex App Server port 9100)
- Kill early, kill cheap — better at poster stage than after 8 bible pages
- Poster IS the pitch — becomes thumbnail, social hook, brand
- Era commitment required for every poster

## See Also

- `sgflix-create-character-bible` — Next step after GREENLIT
- `sgflix-factory-pipeline` — Full production pipeline
- `sgflix-qc-validate` — Quality control system