# Character Lock Database — Franchise Scale Generation

## The Formula

One locked style prefix + one locked character description per character = infinite diverse images without training a LoRA.

```
[STYLE PREFIX] + [CHARACTER LOCK] + [SHOT TYPE] + [SCENE]
```

**The style prefix IS your LoRA.** It's the same text block pasted at the start of every single prompt. That's what makes your grid look cohesive even when posting completely different shot types, characters, and scenes.

## Style Prefix Example (Found Footage)

```
1995 Hi8 camcorder found footage, VHS timestamp in bottom-left corner, overcast 
flat natural lighting, grainy low resolution, amateur documentary style, real 
costumes real vehicles real mud, not cinematic not polished
```

This prefix is pasted verbatim at the start of EVERY prompt. It never changes.

## Character Lock Example

```
[LOCK] Italian-American man, 5 foot 6, compact muscular build, short stocky 
proportions. Wearing a faded red baseball cap with a white "M" patch (sweat-
stained, fraying edges), red long-sleeve cotton shirt stained with mud and 
engine grease, blue denim work overalls with a worn leather belt and brass 
buckle, white cotton gloves caked in dried mud, thick black handlebar mustache 
(costume-grade, slightly crooked and peeling at edges). Dark brown eyes, 
weathered face with stubble shadow. 
Vehicle: Battered red-and-white go-kart racing chassis, hand-painted number "1" 
on side panel with visible brush strokes, "Mario's Plumbing" faded text on rear, 
exposed engine block caked in grease, chipped paint showing bare metal, real 
racing tires worn and mud-caked.
```

This lock is copied verbatim into any prompt featuring this character. Only the SHOT TYPE and SCENE change.

## Shot Type Library (16 types per episode)

| # | Shot Type | What Changes |
|---|-----------|-------------|
| 1 | Hero face-off | Both characters + scene |
| 2 | Action wide | Camera angle + movement |
| 3 | Character portrait | Expression/emotion only |
| 4 | Villain portrait | Body language only |
| 5 | Vehicle A detail | Texture/materials only |
| 6 | Vehicle B detail | Texture/materials only |
| 7 | Empty environment | No characters at all |
| 8 | Crowd reaction | Spectators, not racers |
| 9 | Pit area | Behind the scenes |
| 10 | Prop close-up | Single object |
| 11 | Before/after | Same vehicle, two states |
| 12 | Night/atmosphere | Lighting changes |
| 13 | Crash moment | Action + chaos |
| 14 | POV shot | Camera position |
| 15 | Macro detail | Extreme close-up |
| 16 | Establishing wide | Wide landscape |

## Scale Math

```
24 characters (12 Mario Kart + 12 Twisted Metal)
× 35 solo shots per character (5 expressions × 3 angles + 10 vehicle + 5 environment)
= 840 solo images

+ 144 VS matchups (12 × 12)
× 16 shot types per matchup
= 2,304 matchup images

+ 200+ group shots, environments, props
= 3,000+ unique images from one franchise
```

## How It Works in Practice

Same character, 4 completely different images:

```
# Portrait
[STYLE PREFIX] Close-up portrait of [MARIO LOCK]. He stares directly at the 
camera with intense determination, mud splattered across his face and cap.

# Vehicle detail
[STYLE PREFIX] Close-up detail shot of a battered red-and-white go-kart engine 
block, exposed pistons caked in dried mud, hand-painted number 1 on chipped 
side panel, grease stains and oil drips, wrench resting on the engine.

# Environment (no character)
[STYLE PREFIX] Wide establishing shot of an empty muddy dirt track, hay bale 
barriers, red and white mushroom props scattered on the ground, overcast sky, 
no people visible, eerie silence.

# Action wide (both characters)
[STYLE PREFIX] Wide tracking shot of [MARIO LOCK] in his red go-kart racing 
alongside [SWEET TOOTH LOCK] in a rusted ice cream truck with SWEET TOOTH 
spray-painted on the side, both vehicles kicking up mud spray on a dirt track, 
spectators behind barriers.
```

Same prefix. Same character lock. Completely different images. That's how you get grid variance without a LoRA.

## Key Principles

1. **Style prefix never changes** — it IS the visual identity
2. **Character lock never changes** — physical description stays identical
3. **Only shot type and scene change** — that's where diversity comes from
4. **Characters are described as REAL PEOPLE in costumes** — not cartoon characters. This is what makes found footage look like recovered documentary footage instead of fan art.
5. **Vehicle descriptions are part of the character lock** — the kart/truck is an extension of the character

## Character Lock Database Structure

Organize as one master file with all characters:

```
CHARACTER LOCK DATABASE — [Franchise Name]
├── STYLE PREFIX (paste at start of every prompt)
├── ROSTER A (e.g., Mario Kart — 12 characters)
│   ├── CHARACTER_NAME [LOCK] ... full description + vehicle
│   ├── CHARACTER_NAME [LOCK] ...
│   └── ...
├── ROSTER B (e.g., Twisted Metal — 12 characters)
│   ├── CHARACTER_NAME [LOCK] ...
│   └── ...
├── QUICK REFERENCE — all names
└── CROSS-MATCHUP MATRIX (Roster A × Roster B = matchups)
```

## Reference Implementation

See: `/Users/speed/launch_pdfs/CHARACTER_LOCK_DATABASE.md`
- 24 characters (Mario Kart + Twisted Metal)
- Found footage style prefix
- 144 cross-matchup combinations
- 3,000+ image potential
