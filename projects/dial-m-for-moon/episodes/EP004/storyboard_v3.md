# EP004 — "TWO TAPES" (Storyboard v3 — rebuilt from scratch, keyframes FINAL)

v3 is a new storyboard, not a revision. Same premise, same slot, same
constraints — but every shot re-examined starting at S01.

**Status 2026-09-24:** all 10 shots have final keyframes. S02/S03/S05
were rebuilt from zero per Jay's order ("get rid of those") after he
rejected the v2 keyframes for floating objects and a disconnected hand.
All keyframes passed the physical-plausibility gate in
`keyframe-qc.md`. No animation approved yet.

## Directing doctrine

**Hitchcock, primary.** The audience knows the danger before she
finishes taking it (copying a classified tape in a Soviet listening
post is treason — the bomb is under the table from S02 on). Suspense
comes from watching her risk it. Tools: look → see → reaction;
reaction over action; objects as emotional carriers; silence and
ordinary detail.

**Borrowed:** Polanski (the headset stays ambiguous — someone was here,
or she's breaking; never answered). Kurosawa (S07 holds stillness).

**Value map:** every beat moves her safer → less safe. No exceptions.

**Framing arc — the vise:** medium-wide in the bay, tightening to
close-ups as her safety shrinks. Nowhere left for the camera, or her,
to go.

**Caption voice:** her private voice only — defiance, self-calming.
Where the face carries it, no caption.

**Standing constraints:** one visible character; the operator exists
only as the warm headset; struck-through name, never invented; hard
cuts default, match-on-action only for hand-carried objects; S07→S08
unconditioned time gap; tape hiss bridges ruptures; title ≤3–4s; red
pencil anchors the labeling; final face held longer than comfortable;
quiet bay (reel mechanics, pencil, silence around the reveal);
locked-off cameras; strict continuity gates.

## The suspense spine

She discovers the lie → **decides** to keep the proof → commits the
crime → buries it → feels watched → the deck explodes → finds the
proof gone → finds someone was listening → doesn't know what's next.

## Beats (11 shots + cold open, ~112s)

### COLD OPEN — the spark-out, detail (2s, no caption)
`shots/S08/coldopen-spark-detail.png` (tight 9:16 crop of the S08 keyframe)
Pure kinetic abstraction: the tape deck erupting in white-orange sparks,
no Valya, no context. Tape hiss underneath, then the bang. Then the
title card, then rewind. The audience spends the whole quiet episode
waiting for the explosion they know is coming — the bomb under the
table, Hitchcock's trade: suspense instead of surprise.
*Feeling:* what the hell was that.
*Value:* calm → question. The hook inside 3 seconds.

Keyframe base path: `episodes/EP004/shots/`

### S01 — title card (3s)
`shots/S01/title_card.png` — clean typographic card, built with PIL so
the type can't garble: DIAL M FOR MOON / "TWO TAPES" / EPISODE FOUR.

### S02 — the coordinates (NEW keyframe, v3)
`shots/S02/media-generation-ep004-s02-v5-realization-0-d0d65e51-73a5-450c-8c50-d227b78670cb.webp`
She leans over the desk. The chart and the mayday slip both lie FLAT
in desk-plane perspective; her right hand grips the red pencil, tip on
the chart. Her eyes move between slip and chart — and stop. The
realization lands on her face: these are not American coordinates.
*Feeling:* professional certainty curdling into dread.
*Value:* routine → dread.
Caption: "These are not American coordinates."
QC: pass. Nit (open): the slip's text is English ("NOT AMERICAN
COORDS"); the v2 version was Russian. Jay's call whether to switch it.

### S03 — the erased man (NEW keyframe, v3)
`shots/S03/media-generation-ep004-s03-v3-flat-file-0-25a831d3-d3cf-46f6-9913-525171bb6d0a.webp`
(note: file lives in the S02 folder)
The flight file lies FLAT on the desk. She leans over it, her index
finger resting on the thick black redaction bar striking through the
cosmonaut's name — fingertip in contact with the paper. The name stays
redacted and unreadable; no invented name. Her eyes are on the
struck-through name. Archive stamp beside it.
*Feeling:* the chill of understanding. The state erased a man — and now
she knows too much to walk away.
*Value:* suspicion → certainty.
Caption: "He never flew."
QC: pass.

### S04 — the decision: the choice (peak moment, not setup)
`shots/S04/media-generation-ep004-s04-v2-the-choice-0-5ba48878-306c-4b77-ac7a-cb89bb5fc1c5.webp`
Her hand grips a blank reel on the shelf — the reach. Her face in
profile: resolved, afraid, decided. The reach is the decision; no
caption. This is the episode's moral center: she goes from discovery
to crime only through a choice, and the choice costs her, on screen.
*Value:* certainty → resolve. She chooses the danger.
Sound: the deck stops. Silence. (S05 opens with the dub's first turn.)
QC: pass.

### S05 — the crime (NEW keyframe, v3)
`shots/S05/media-generation-ep004-s05-v4-no-badge-0-98eb7476-bcea-4522-a0eb-ffd4bdf11b19-clean.webp`
(note: file lives in the S04 folder)
Shot from behind her shoulder: her arm runs visibly from her shoulder
to the deck — the hand on the dub control is unambiguously hers. Her
head turned in profile, eyes glancing toward the door (visible in the
background), afraid of the sound the reels are about to make. Directed
like treason, not office work.
*Feeling:* fear, held under control. She's trying not to shake.
*Value:* resolve → criminal. Done; can't be undone.
Caption: "One copy. For me." (the vow, spoken while afraid)
QC: pass. Nit (open): a "KODAK" badge on the deck — a Soviet machine
wouldn't carry it. Small; Jay's call.

### S06 — the cover-up (NEW keyframe, v1)
`shots/S06/media-generation-ep004-s06-v4-the-burial-0-ac662faf-8808-4251-adf0-027fa54ea535.webp`
Her hands lower the labeled reel into the open wooden crate of folded
cloth headbands — both hands visibly holding the reel above the crate.
Her face: fragile relief, the kind you don't trust.
*Feeling:* exposure, then fragile relief. (This relief is what S08
takes away — it has to read.)
*Value:* criminal → exposed → hidden.
Caption: "No one looks here." (self-calming)
QC: pass. Nit (open): the reel label reads "ХРАНИТЬ / 23.IX.59 /
ДНЕПР-7 / УНИЧТОЖ." — "keep" and "destroy" contradict each other.
Barely legible in motion, but Jay reads frames closely. Regenerate the
label on his word.

### S07 — the pause (Kurosawa stillness) (NEW keyframe, v1)
`shots/S07/media-generation-ep004-s07-v1-stillness-0-8ccb708a-ea91-4f1e-b5d8-4c1d16601e1f.webp`
Extreme close-up. Headset on. She is utterly still — eyes unfocused at
mid-distance, breath held, listening. Nothing happens. The silence
stretches longer than comfortable.
*Feeling:* the animal sense that something is wrong, with no proof.
*Value:* hidden → watched? (the question, not the answer)
No caption. Silence is the beat.
QC: pass.

### S08 — the spark-out (kinetic spike) (photoreal retouch, v2)
`shots/S08/media-generation-ep004-s08-v2-photoreal.webp`
The Soviet reel-to-reel deck shorts out in a shower of white-orange
sparks and thin smoke — an electrical fault, not a fireball. Valya
recoils, arm shielding her face, mouth open. The machine at the center
of her crime destroys itself. The bang is what sends her to check the
crate: spectacle that turns the plot.
*Feeling:* shock. The room turns hostile.
*Value:* watched → attacked.
Caption: none — the bang is the caption.
QC: pass with local retouch — the generator's first pass scattered
symmetrical digital starburst sparkles with no ballistic origin (a
photo-realism failure: real sparks are motion-blurred streaks from one
point). A fresh generation was refused by the image pipeline, so the
fake floaters around her head were removed locally from the v1 frame;
skin tones protected, deck burst core untouched, her flinch performance
kept. First retouch attempt smeared her cheek (luminance-only mask) and
was discarded; v2 uses a low-saturation guard and is verified clean.

### S09 — the empty crate (time gap, hard cut in, unconditioned)
(NEW keyframe, v1)
`shots/S08/media-generation-ep004-s08-v1-empty-crate-0-7f6e23a9-42cb-4303-a397-3afb7a20cb25.webp`
Over her shoulder, down into the open crate: folded headbands only.
The labeled reel is GONE. Her hands grip the crate's edges. Her
shoulders have dropped. The absence is the image. Lamp light different
from S06 — time has passed.
*Feeling:* violation. The one safe place wasn't safe.
*Value:* relief → violation.
Caption: "Gone."
QC: pass.

### S10 — the warm headset (Polanski ambiguity)
`shots/S10/media-generation-ep004-s09-v1-warm-headset-0-c4601c8a-8884-4aad-acb4-797d9aec5206.webp`
Close-up: the Bakelite headset rests on the desk. Her hand hovers just
above the earcup — not touching, feeling for warmth in the air. Her arm
connects back to her body. Behind the hand, her face: troubled,
uncertain. Someone was here — or she's breaking. Do not answer it.
*Feeling:* the floor dropping out.
*Value:* violation → presence.
No caption. Silence around the reveal. (Warmth identified by her
touch, never by a visual change.)
QC: pass.

### S11 — the hook
`shots/S10/media-generation-ep004-s10-v1-final-look-0-e2203ddc-96be-4a1d-9e69-3520ed99f140.webp`
Held close-up. Her face turned toward the door, half carved out of
shadow by the tungsten lamp. Eyes fixed on the door. She doesn't know
what happens next — and neither do we. Hold longer than comfortable.
*Feeling:* dread with no object.
*Value:* presence → unknown. Ends open.
No caption.
QC: pass.

## Character anchors (every shot prompt)
Valentina "Valya" Orlova, 27. Ash-blonde low bun, dark-olive ribbon,
sky-blue signals piping on the tunic, Bakelite headset, red pencil
over right ear. 1959 16mm Kodak Ektachrome, vertical 9:16,
period-true, no modern sci-fi. The locked night-bay reference was
passed as the identity image for every keyframe.

## Wardrobe/prop lock notes
- The tape reel label: her handwriting; identical S06 → S08. (See S06
  nit — label text needs a verdict.)
- The headband crate: same wooden crate, folded cloth headbands,
  S06/S08.
- The headset: the "warm" earcup identified by touch only, S09.
- The red pencil: over her right ear in every shot; taken down to
  label in S06's action (keyframe shows it still over her ear — the
  labeling beat itself is inside the animated shot).

## What changed from v1/v2, and why
- **Scrapped per Jay's order:** the S02 winner video, the S03
  (s02b) winner video, and the S04 threading/reel-lift keyframes. The
  v2 replacement keyframes for S02/S03/S05 were rejected by Jay for
  floating objects and a disconnected hand.
- **All-new keyframes, all 10 shots:** rebuilt under the v3 doctrine
  from the start — reaction over action, the crime as a held breath,
  the decision as the moral center.
- **Keyframe QC gate adopted** (`keyframe-qc.md`): six physical-
  plausibility checks (gravity, grip, hand–body continuity, eyeline,
  surface perspective, one character). Every keyframe is checked
  before Jay sees it; failures regenerate.
- **New S04 (the decision):** the episode's moral center was missing
  in v1. Now the choice is on screen, and it costs her.
- **Merged old S05+S06 into new S06:** three procedural beats in a row
  risked monotony. The middle is now decision → crime → cover-up —
  three shots, three emotional colors.
- **Unchanged:** premise, constraints, runtime (~103s), caption voice,
  doctrine, the warm-headset ambiguity, the open hook.

## Sound spotting (decided pre-animation, 2026-09-24)
Temp sound for the animatic is synthesized, not final. Rule: the
soundscape is quiet — reels, pencil, fabric, breathing, silence. Every
sound below was spotted before any video is generated.

- COLD OPEN (0-2s): tape hiss up under the spark crop, then the BANG.
  Hard cut to silence into the title.
- S01 title (2-5s): low room tone, faint hiss. Nothing else.
- S02 (5-15s): pencil-scratch hiss bed that STOPS DEAD mid-shot — the
  absence of the scratch is the realization. Silence to end of shot.
- S03 (15-25s): soft paper handling, two small rustle swells. Low.
- S04 (25-35s): room tone; one soft wooden clunk as the reel leaves
  the shelf.
- S05 (35-45s): deck hum (low) under hiss. The crime sounds ordinary —
  that's the point.
- S06 (45-55s): fabric rustle as headbands are smoothed over the reel;
  one soft thud. Then back to near-quiet.
- S07 (55-65s): near-silence. Faint room tone only. Her listening is
  the loudest thing in the room.
- S08 (65-75s): the BANG — electrical crack, low thump, then a thin
  high ringing that decays across the rest of the shot.
- S09 (75-85s): ringing gone by mid-shot; fabric rustle as she tears
  through the crate. The violation has a sound.
- S10 (85-95s): TOTAL SILENCE around the warm-headset reveal. No tone,
  no hiss. The quiet is the scare.
- S11 (95-107s): faint room tone creeps back in. Nothing resolves.
  Cut on tone, not on silence.
