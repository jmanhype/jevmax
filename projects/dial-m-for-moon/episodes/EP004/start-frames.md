# EP004 — Key-pose / start-frame set (2026-09-24)

Board approved by Jay 2026-09-24. Board panels stage PEAK moments; the video
model inbetweens from a START frame, so each animation shot gets its own key:
usually one beat BEFORE the board peak. Locked camera on every shot.
Photo and physics realism throughout.

| Shot | Board peak | Start frame (key) | Motion start→peak | Source |
|------|-----------|-------------------|-------------------|--------|
| CO (2s) | Full spark burst macro | Deck running normally; single thin arc just forming at one contact point; her face calm, unaware | Arc blooms into burst; light flickers | NEW |
| S01 (3s) | Title card | Title card (static) | Fade in from black (edit) | REUSE |
| S02 (10s) | Pencil stopped, eyes lifting to mayday slip | Pencil still moving, writing; eyes DOWN on the logbook | Pencil stops dead; eyes lift to the slip | NEW |
| S03 (10s) | Redacted file flat | Same flat file (micro-motion only) | Finger tremor / slight settle | REUSE |
| S04 (10s) | Hand takes reel, eyes cut to door | Hand reaching, not yet grasping; eyes still on the reel | Fingers close on reel; eyes cut to door | NEW |
| S05 (10s) | Operating dub control, watching door | Hand moving toward the control | Hand lands on control; deck engages | NEW |
| S06 (10s) | Hands smoothing headbands over reel | Hands holding folded headband above the reel | Headband laid down; hands smooth it flat | NEW |
| S07 (10s) | Frozen listening | Same frozen pose (micro-motion only) | Breath, blink | REUSE |
| S08 (10s) | Full burst, her recoil | Deck normal; her face calm, hand near controls | Short-out: burst + flash; she recoils (head turns away, shoulders hunch) | NEW |
| S09 (10s) | Empty crate discovered | Hands lifting headbands, about to discover | Headbands lifted; empty crate revealed; her reaction | NEW |
| S10 (10s) | Fingers at earcup, warmth detected | Board v1 already stages the pre-touch beat (hand hovering, neutral face); motion = hand descends, touches, micro-flinch | REUSE board v1 |
| S11 (12s) | Held look toward the door | Mid-turn toward the door | Turn completes; gaze locks; held beyond comfort | NEW |

All start frames QC'd against keyframe-qc.md before presentation.

## Batch 1 QC (2026-09-24)
- CO start: PASS with note — single thin arc at one contact point, calm face.
  Wardrobe flag: she wears the pilotka cap; S08 start has no cap (bun +
  pencil behind ear). Same physical moment → must match. REDO without cap.
- S02 start: PASS — pencil mid-stroke, eyes down on logbook, Russian mayday
  slip legible, plausible grip, wrist-sleeve continuity, eyeline on page.
- S04 start: REJECT — generated the peak, not the key: hand already holding
  the reel AND eyes already toward the door. Spec needs: hand extended, not
  yet grasping; eyes still ON the reel. REDO with stronger wording.
- S08 start: PASS — deck normal, no sparks, calm focused face, hand near
  controls. Pencil behind ear matches S04's pencil placement.

## Batch 2 QC (2026-09-24)
- CO v2: PASS — cap removed (bun + red pencil behind ear), matches S08 start
  wardrobe. Single thin arc at one contact point, calm face.
- S04 v2: REJECT — hand extended toward the DOOR, eyes toward the door; the
  model anchored on the door mention. v3 (door removed from frame and prompt):
  PASS (acceptable) — hand extended toward the reel shelf, eyes on the shelf,
  reads clearly as the pre-grasp key.
- S05 v1: REJECT — hand already ON the knob (spec: hovering) plus large gray
  blur blocks over the deck's right side.
- S06 start: PASS — hands holding headband above the reel, about to lay it
  down. Reel label "ХРАНИТЬ 23.IX.59" matches the approved S06 board v4.

## Batch 3 QC (2026-09-24)
- S05 v2/v3: REJECT — gray blur blocks persist across framings (safety-layer
  redaction over the deck's right side, not a render flaw). v4 with flipped
  composition (deck left, her right in profile): PASS — no blur, hand
  hovering above the controls, touching nothing, calm.
- S09 start: PASS — hands lifting headbands, contents still hidden, face
  intent and curious, no premature reaction.
- S10 v1: REJECT — hand already on the earcup with the wary face = the peak.
  v2 duplicated the board v1 composition, revealing the approved board panel
  already stages the pre-touch beat. Verdict: REUSE S10 board v1 as the start
  frame (motion = hand descends → touches earcup → micro-flinch at warmth).
- S11 start: PASS — caught mid-turn, eyes traveling toward the door, tense
  but not frozen.

Final set: 8 new keys (CO, S02, S04, S05, S06, S08, S09, S11) + 4 reuses
(S01 title, S03 board v3, S07 board v1, S10 board v1).
