# Eyecandy source grammar — 2026-09-20

Source: [Eyecandy](https://eyecannndy.com/), fetched live on 2026-09-20.
The site exposes 138 technique categories. Jevmax uses it as the visual grammar
layer, then maps named techniques into `camera`, `motion`, `environment`, and
`grade` fields in the creative schema.

## Techniques selected for the first Ava test

### Camera Roll

Source: <https://eyecannndy.com/technique/camera-roll>

Eyecandy definition: “The rotation of an entire scene, usually 180 degrees.”
Related label on the page: *Whip Roll*.

Jevmax mapping:

- `motion.camera`: controlled whole-frame roll
- `motion.world`: horizon and frame rotate together
- continuity constraint: Ava, earbud cable, and face remain centered

### Floating UI

Source: <https://eyecannndy.com/technique/digital-overlay>

Eyecandy definition: “When a digital interface is shown on the screen in an
abstract way to help us better understand the content.”

Jevmax mapping:

- abstract `motion.world` overlay
- no readable claim text or fake product UI

### Vintage

Source: <https://eyecannndy.com/technique/vhs>

Eyecandy definition: “A film technique in which the images are presented as if
they were part of a video or film recording that was later discovered.” The
page associates the technique with archival footage, vintage graphics, shaky
camera, and documentary realism.

Jevmax mapping:

- `grade.look`
- analog tape texture
- `motion.camera` imperfection

### Central Framing

Source: <https://eyecannndy.com/technique/central-framing>

Eyecandy definition: “Centering the subject in film framing emphasizes
symmetry, drawing attention to convey visual impact and significance in a
shot.”

Jevmax mapping:

- `camera.framing`
- stable subject anchor during the camera roll

## Technique gate result

The Jev gate ranked the late-1980s local-sponsor-bumper concept highest
(`6.34` total; hook `2.27`, fit `0.70`, survival `0.57`). The first paid test
therefore uses **Central Framing** as the dominant technique; Vintage supplies
the production register and protects the discovered-tape feeling. Camera Roll
and Floating UI are intentionally withheld from the first render to avoid
overpacking a five-second test.
