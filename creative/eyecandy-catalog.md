# Eyecandy catalog — the visual grammar layer

Source: [eyecannndy.com](https://eyecannndy.com/) (by Jacobi — "Learn. Don't
gatekeep."), fetched live 2026-09-23. Technique pages live at
`https://eyecannndy.com/technique/<slug>`; slugs are kebab-case names except
known exceptions (Floating UI → `digital-overlay`, Vintage → `vhs`).
Working subset with field mappings: `eyecandy-source-grammar.md`.

## Rule (jevmax layer 3 — GRAMMAR)

Every shot names **ONE dominant technique** from this catalog, mapped into
concrete `camera` / `motion` / `world` / `grade` fields in the shot record
(`shot-record-template.md`). Extras are listed under `withheld` — naming what
you are NOT using prevents overpacking a 5-second shot. Camera language is
loose in generation models; the technique NAME is the anchor ("models read
camera language loosely — say it twice, concretely": workflow.md gotcha #3).

## Catalog (136 techniques, 2026-09-23)

Aerial · Altered state · Animation · Anthropo · Arc · Architexture · Bolt Cam ·
Boomerang · BTS · Bullet Time · Camera Roll · Central Framing · Choreo ·
Cinemagraph · Close-Up · Collage · Color Shift · Conveyor · Crash cut ·
Cut-ins · Datamosh · Diorama · Distortions · Dolly · Dolly Zoom · Double
Dolly · Double Exposure · Dreamcore · Duplication · Dutch Angle · Dystopian ·
Echo print · Epiphany · Falling · Fast Motion · Feedback · First-Person ·
Fisheye · Fixed Cam · Flash Cut · Floating UI · Focal shift · Fourth Wall ·
FPV Drone · Freeze Frame · Generative · Gesture · Ground Level · Halation ·
Handheld · Hard Light · Haze · High Angle · Infinite Loop · Interview ·
Jump cut · Kaleidoscope · Lazy Susan · Levitation · Light Flash · Locked-On ·
Low Angle · Magical realism · Magnification · Masking · Match Cut · Match
motion · Match Split · Maximalism · Mixed Media · Morphing · Motion Blur ·
Night Vision · Object Portal · Object POV · Omnidirectional · Overhead ·
Over the Shoulder · Pan · Parallax · Pass Through · Pedestal ·
Photogrammetry · Photography · Pixel Art · Probe · Product · Profile ·
Projections · Quick Cuts · Ratio Switch · Reflections · Scale Shift ·
Screen in Screen · Set Transition · Shadow Box · Shallow Focus · Silhouette ·
Slit-scan · Slow Motion · Snorricam · Speed Ramp · Split Diopter ·
Split Screen · Spotlight · Step-print · Stop Motion · Stutter ·
Stylistic Suck · Tableau · Thermal · Tilt · Tilt Shift · Tracking ·
Transformation · Transitions · Trucking · Two Shot · Typography · Ultra Wide ·
Underwater · Video Game · Video Portraits · Vignette · Vintage · Void ·
Voyeur · Wandering · Weirdcore · Whip Pan · Wide shot · Wigglegram ·
Worms-Eye · X-Ray · Zoetrope · Zoom

## Period drama registers (DIAL M FOR MOON)

Grade-register techniques (apply series-wide, never per-shot): **Vintage**
(discovered-footage register; our 16mm Ektachrome lock), **Halation** (on
practicals only), **Vignette** (mild, archive-lens feel). Shot-grammar
candidates for the switchboard world: Central Framing (Valya's anchor
framing), Cut-ins (plug/hand/lamp inserts), Over the Shoulder (Korabelnikov
demanding the log), Split Diopter (Valya + board lamps both sharp), Focal
shift (attention as focus pull), Locked-On (surveillance dread), Voyeur
(the traced transmitter), Typography (Cyrillic log placards, [画面文字]).

## Prompt-language layer (Cinematique, vvsvs.pro/cinematique — adopted 2026-09-23)

Cinematique is a free 150+ technique library whose value to us is the
*prompt phrasing* layer: Eyecandy NAMES the dominant technique; Cinematique
supplies the tested language that makes a generator deliver it. Role chain:
**Eyecandy names it → Cinematique phrases it → PERIOD STOCK constrains it →
Shot Composer verifies it → wallet renders it.** Open source (based on
grokfilm.app); free for any use per their FAQ.

Most useful vocabulary for the DIAL M register (period-filtered):

- **Lighting** (our thinnest layer): low-key (deep shadow, select
  illumination — the night-shift default), chiaroscuro (sculpted
  tenebrism — Korabelnikov interrogations), practical lighting (the board
  lamps ARE the sources — motivated, Barry Lyndon doctrine), hard light
  (bare tungsten bulbs, sharp shadow edges), short lighting (key on the
  far side of the face — thriller default for Valya), side lighting
  (bisected faces, moral duality), kicker (edge separation in dark rooms),
  eye light (signal-lamp catchlights — "eyes without catchlights appear
  dead"), gobo (venetian-blind/window-frame shadow patterns), color
  temperature as dramaturgy (tungsten amber = the board, cool spill =
  the corridor/Moscow).
- **Composition**: framing-within-frame (doorways and window frames —
  Korabelnikov never enters far, the frame traps; Ford/Hitchcock lineage),
  deep focus (both planes critical — pairs with Split Diopter), figure-
  ground (noir merging of subject into shadow), negative space (the empty
  bay after he leaves), leading lines (cord webs, corridor perspective).
- **Editing grammar** (edit-sheet stage): the insert/cut-in, reaction shot
  (Kuleshov), cutaway, smash cut (to black on the button), cross-cutting
  (two empires), dissolve (the tape flashbacks), in medias res + cliffhanger
  (already our episode doctrine — external validation).

**PERIOD GATE (mandatory):** all Cinematique gear citations pass the 1959
lock before entering a prompt. Allowed: tungsten practicals, reflected/
bounce light, 16mm Ektachrome reversal, period spherical primes, halation,
gate weave. Forbidden: ARRI/Vision3/Master Primes and any post-1959 stock,
lens, or digital grade language — the template text is modern; the era
wins.
