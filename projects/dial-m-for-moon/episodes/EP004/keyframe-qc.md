# Keyframe QC — physical plausibility gate

Every generated keyframe is checked against this list BEFORE being shown
to Jay. A keyframe that fails any item is regenerated, not presented.
Adopted 2026-09-24 after Jay caught floating objects and a disconnected
hand in the EP004 v2 keyframes (S02 slip + pencil floating; S03 file
hovering; S05 hand reading as someone else's).

## The six checks

1. **Gravity.** Every object either rests on a visible surface or is
   gripped by a visible hand. Nothing floats, hovers, or levitates —
   no floating pencils, slips, or papers.
2. **Grip.** A held object must show fingers in contact with it, wrapped
   plausibly. A hand near an object is not holding it.
3. **Hand–body continuity.** Any hand in frame must connect visibly to
   the character (wrist → sleeve → arm → shoulder) or be unambiguously
   hers by position and angle. A hand that could belong to a second
   person fails — this episode has one visible character, no exceptions.
4. **Eyeline.** The character looks at something that exists in the
   frame, at a plausible angle and distance. No staring past the object
   she's supposed to be reading.
5. **Surface perspective.** Papers lie in the desk plane with correct
   perspective. No upright cards floating in front of faces; no paper
   angled in ways a real sheet couldn't hold without support.
6. **One character.** No second person's hands, arms, or body parts
   anywhere in frame.

## How to prompt for it

Don't hope the model gets physics right — direct it:
- Say where things rest: "the slip lies FLAT on the desk," "the file
  lies flat; she leans over it."
- Say what holds what: "her right hand grips the red pencil, tip on
  the chart."
- For hands near controls, shoot over-her-shoulder so the arm's
  connection to her body is visible in frame.
- Prefer leaning-over-desk staging over holding-papers-up staging;
  gravity does the QC for you.

## Process

1. Generate the keyframe.
2. Run the six checks. Be adversarial — assume it failed until proven.
3. Fail → regenerate with the physics stated more explicitly.
4. Pass → present to Jay with the check results noted.
