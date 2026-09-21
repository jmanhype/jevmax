# Lost Future output grammar — real example, captured 2026-09-20

Source: Jay's actual Lost Future GPT conversation "Lost Future Style Catalog"
(chatgpt.com GPT `lost-future`, model 5.5 Thinking). This is the layer-1
format the content engine consumes. Captured via computer use; verbatim below.

## The three-part grammar

**1. STYLE FAMILY** — era + medium + genre, numbered S01–S50. Real samples:

    S01: 1985–1992 Japanese Direct-to-Video Cyberpunk OVA
    S05: 1993–1998 CD-ROM / Pre-Rendered Game Cutscene Future
    S13: 1990s Weather Channel Local Forecast Scanline
    S43: Local Car Dealership Commercials
    S49: Nigerian Nollywood VHS Occult Drama
    S50: Vaporware Magazine-Ad Future

**2. CONCEPTS per family** — ID letter + TITLE + TAGLINE (three per style):

    S43A: TITLE: "BIG DEAL" ;; TAGLINE: "Prices so low they star…"
    S45A: TITLE: "MODEM GIRL" ;; TAGLINE: "She connected to the …"
    S50A: TITLE: "TOMORROWPAD" ;; TAGLINE: "Available soon. Mayb…"

**3. SHOT PROMPTS** — per concept: five reference anchors, then per shot a
Prompt / Negative-prompt pair, shot types lettered (A = wide establishing,
B = close-up). Verbatim example (the 1982 vector arcade concept):

    Five reference anchors:
    Battlezone; Tempest; Star Wars arcade; Lunar Lander; Red Baron.

    Prompt A — wide establishing shot
    Prompt: 1982 vector arcade wireframe future, wide establishing shot inside
    a dark neighborhood arcade, one glowing cabinet at center showing a black
    void battlefield of neon green and phosphor blue wireframe tanks, red
    warning triangles, convex CRT glass reflecting a teenager's hands on the
    controls, blacklight carpet and dusty cabinet side-art visible, low camera
    near coin slot, attract-mode loop, screen flicker, phosphor trails, analog
    hum, future reduced to luminous geometry.
    Negative prompt: No modern arcade bar, no LCD screen, no pixel-art sprite
    game, no 3D textured graphics, no cyberpunk city, no VR headset, no clean
    emulator capture, no cinematic neon realism, no widescreen display.

    Prompt B — close-up
    Prompt: 1981 vector arcade CRT close-up, extreme close shot of glowing
    green wireframe horizon grid and a simple blue outline enemy ship rotating
    against pure black, phosphor bloom around every line, faint burn-in, dust
    specks on glass, red vector explosion expanding as sharp polygons,
    reflection of a quarter slot at the bottom edge, mathematical motion,
    cabinet hum and oscillator blast implied, sacred minimal hardware future.
    Negative prompt: No raster pixels, no modern glow plugin, no realistic
    spaceship texture, no particle effects, no full-color 3D render, no UI
    health bars, no clean digital lines, no contemporary game capture.

Also observed: "aesthetic mining runs" that generate dozens of NEW style
families with one-line theses (e.g. "1990s Legal Deposition Videotape —
testimony became aesthetic: beige conference rooms, fixed camera…").

## Wiring into jevmax-creative-v2 (layer 1 -> layer 4)

| Lost Future section        | v2 schema field                          |
|----------------------------|------------------------------------------|
| Style family (S01–S50)     | `grade.look` + `environment.*` + `scene` |
| Concept TITLE + TAGLINE    | `video.hook_line` (spoken hook)          |
| Shot type (Prompt A/B/C…)  | `camera.pov` / `camera.framing` `*_options` |
| "Five reference anchors"   | style anchors — translator guidance only, never the painter prompt |
| Negative prompt            | `constraints.avoid` (translator-side; negations still never enter the painter prompt, see pipeline rules) |

Key insight: Lost Future's Prompt bodies are ALREADY painter-paragraphs in our
render order (era prefix -> scene -> subject -> product-ish anchor -> light ->
camera -> grade). They can drop into `flatten()` output nearly as-is — the v2
schema's job is to make the VARIABLE parts (subject, product, hook) swappable
while the style family stays frozen, exactly like the character block.

One ask pattern that works (observed): "Full aesthetic mining run — NEW
TERRITORY ONLY, no summaries" -> families with theses -> then per family,
concepts -> then per concept, shot prompt pairs.
