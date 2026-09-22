# Cursed-realistic seeds — genre grammar, locked to Lost Futures production rules

2026-09-22. Source reasoning: the internet "cursed image" genre (mundane
setting + ONE impossible thing + evidence-camera framing + never explain),
run through the board's spec pipeline instead of a lazy one-line prompt.

## Genre law (applies to all five)

1. **One wrong thing per image.** Not three. One.
2. **Nobody in-frame reacts.** The wrongness is invisible to them.
3. **Evidence camera, never art camera.** The image must read as a file, not
   a composition.
4. **Caption never explains.** One line, flat tone, implies a record exists.
5. **Rights lane: ownable.** No IP, no brands, no real people.

## CU-01 — "Row 2, third from left"

Corporate safety-award Polaroid, 1991. Twenty employees posed in a warehouse
break room around a plaque: "500 DAYS WITHOUT AN INCIDENT." Everyone smiles at
the camera — except one person, dead center, facing the wrong way, back of
head to lens. Same uniform. Nobody's expression acknowledges them.

```json
{
  "id": "CU-01",
  "spec": {
    "meta": { "aspect_ratio": "4:5", "camera": "1991 instant Polaroid, flash-on-camera", "style": "corporate documentary photo", "quality": "photographic" },
    "scene": { "location": "warehouse break room", "time_of_day": "fluorescent noon", "atmosphere": "posed group photo, award plaque on easel" },
    "environment": { "palette": "beige, foam-cup white, safety-vest yellow", "lighting": { "source": "harsh on-camera flash", "effect": "hot falloff, glossy skin sheen" } },
    "subject": { "identity": "original fictional employees", "core": "19 smiling workers in matching uniforms, one figure dead-center facing away from camera", "action": "group pose around plaque reading 500 DAYS WITHOUT AN INCIDENT" },
    "camera_perspective": { "pov": "tripod-height group photo, everyone equidistant", "framing": "whole group centered, plaque legible" },
    "texture": "instant film border, cyan color shift, fingerprint on emulsion"
  },
  "caption": "Row 2, third from left.",
  "route": "GPT-Image still (0 cr) first; i2v upgrade only if it wins"
}
```

## CU-02 — "Camera 6 stopped transmitting after this"

Trail-camera night frame, low-res IR. Three deer grazing, calm. At the
treeline behind them, a shape the size of a house — only its leg and flank
enter the frame, flash-lit, too big to resolve. The deer have not noticed.

```json
{
  "id": "CU-02",
  "spec": {
    "meta": { "aspect_ratio": "1:1", "camera": "2003 trail camera, infrared flash", "style": "wildlife monitoring still", "quality": "low-res sensor grain" },
    "scene": { "location": "pine treeline at night", "time_of_day": "3 AM", "atmosphere": "monitoring still, nothing staged" },
    "environment": { "palette": "IR monochrome green-black", "lighting": { "source": "IR flash", "effect": "eyeshine, nearest objects brightest" } },
    "subject": { "identity": "original wildlife", "core": "three calm deer in foreground; an immense flank and single leg entering frame right at treeline, rest out of frame", "action": "deer graze, unaware" },
    "camera_perspective": { "pov": "fixed trail-cam height, slight downward angle", "framing": "deer lower third, wrongness cropped by frame edge" },
    "texture": "sensor noise, timestamp bar bottom corner, water-spotted lens"
  },
  "caption": "Camera 6 stopped transmitting after this.",
  "route": "GPT-Image still (0 cr)"
}
```

## CU-03 — "Dinner for two, aisle 7"

Disposable-camera flash photo, 1992, taped into a store newsletter. An
ordinary grocery aisle, restocked and clean — except one shopping cart parked
mid-aisle, set with a full formal dinner for two: cloth, candles lit, wine
poured. Shelf stockers visible far down the aisle, working around it.

```json
{
  "id": "CU-03",
  "spec": {
    "meta": { "aspect_ratio": "4:5", "camera": "1992 disposable camera + photolab print", "style": "store newsletter snapshot", "quality": "photolab color shift" },
    "scene": { "location": "suburban grocery aisle", "time_of_day": "store hours", "atmosphere": "routine restock night" },
    "environment": { "palette": "fluorescent neutral, cardboard tan, one warm candle accent", "lighting": { "source": "overhead fluorescents", "effect": "even wash, candle glow fighting it" } },
    "subject": { "identity": "original setting", "core": "single shopping cart mid-aisle formally set for dinner for two, candles lit, wine poured; stockers working past it in background", "action": "nothing — the table is simply there" },
    "camera_perspective": { "pov": "employee snapshot angle, slightly tilted", "framing": "cart dominant, long aisle receding" },
    "texture": "photolab print grain, date stamp, tape residue corners"
  },
  "caption": "Dinner for two, aisle 7.",
  "route": "GPT-Image still (0 cr)"
}
```

## CU-04 — "He was enrolled through June"

Camcorder freeze-frame, 1996, from a family birthday tape. Living room, kid
blowing out seven candles, relatives mid-cheer. At the edge of the sofa, one
more party guest sits perfectly still, hands folded, in focus like everyone
else — in a tape nobody remembers a seventh guest on.

```json
{
  "id": "CU-04",
  "spec": {
    "meta": { "aspect_ratio": "4:3 letterboxed to 4:5", "camera": "1996 shoulder camcorder, paused-tape frame", "style": "home video still", "quality": "VHS-grade freeze with scan noise" },
    "scene": { "location": "carpeted living room", "time_of_day": "afternoon party", "atmosphere": "birthday cheer mid-motion" },
    "environment": { "palette": "tube-TV warmth, wood paneling, camcorder blue", "lighting": { "source": "window + camcorder light", "effect": "blown highlights on frosting" } },
    "subject": { "identity": "original fictional family", "core": "child at cake, five relatives cheering mid-motion; one additional seated guest at sofa edge, perfectly still, hands folded", "action": "everyone else blurred mid-cheer; the extra guest is the only still thing" },
    "camera_perspective": { "pov": "parent-operated handheld, slight drift", "framing": "cake center, sofa edge guest half-in frame" },
    "texture": "interlacing lines, timestamp, tracking wobble, paused-frame softness"
  },
  "caption": "He was enrolled through June.",
  "route": "GPT-Image still (0 cr); strongest i2v candidate (paused-tape motion)"
}
```

## CU-05 — "The floor plan ends here"

Estate-agent 35mm flash photo, 1990, from a property listing. Ordinary
apartment hallway — except the last door is wrong: slightly too tall, its
frame running into the ceiling, the door itself ajar onto flat black. The
agent's note card is taped to the wall beside it, facedown.

```json
{
  "id": "CU-05",
  "spec": {
    "meta": { "aspect_ratio": "4:5", "camera": "1990 35mm point-and-shoot, flash", "style": "real-estate listing photo", "quality": "amateur flash photo" },
    "scene": { "location": "rental apartment hallway", "time_of_day": "vacant-unit afternoon", "atmosphere": "showing walk-through" },
    "environment": { "palette": "landlord beige, brass, one black void", "lighting": { "source": "on-camera flash", "effect": "flat falloff down the hall, last door swallowing light" } },
    "subject": { "identity": "original setting", "core": "hallway of identical doors ending in one door slightly too tall for its frame, ajar onto featureless black; a facedown note card taped beside it", "action": "nothing — hallway, door, void" },
    "camera_perspective": { "pov": "eye-level showing shot, centered", "framing": "hall converging on the wrong door" },
    "texture": "35mm grain, slightly missed focus, listing-photo ordinariness"
  },
  "caption": "The floor plan ends here.",
  "route": "GPT-Image still (0 cr)"
}
```

## Why these five

Each is a different evidence register (corporate Polaroid / trail cam /
newsletter snapshot / home video / listing photo) so the account never looks
like one trick. Every one passes the genre law: single wrongness, no in-frame
reaction, file-photo camera, caption that implies a record and explains
nothing. All ownable, all 0-credit on the still route.

Integration: these are **reach-lane candidates for slate 01** — any of them
can replace or backfill R1–R4 slots without touching the mix.
