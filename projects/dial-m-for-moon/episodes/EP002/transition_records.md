# EP002 transition records — pre-generation gate

Decided BEFORE the shot budget is spent. Jev judges; Jay owns escalations.

---

## Transition S01 -> S02

**Beat intent:** her suspicion leaves the book and lands on the stove — the page was burned

**Shot A ends:** fingers on the torn stub, eyes downcast at the gap; paper whisper dying, room hum
**Shot B opens:** the cast-iron stove across the bay — the object of her lifted gaze; stove ticking under room hum

**Plan (Cosmo's draft):** eyeline match. S01 ends on her downcast eyes; S02
opens on what she looks up at. The gaze is the bridge. Audio cuts hard with
picture (room hum is continuous bed, no offset needed).

### Jev verdict (tools/cut_grammar.py)
- cut_type: eyeline_match (matches the pre-generation plan)
- line_discipline: line_honored @ 0.49
- flow: 2.61
- audio_bridge: p=0.73 — Jev leans J/L; plan said hard cut
- tension: 2.16 (build)
- composite: 0.945

### Routing
- escalated: YES — line_discipline confidence 0.49 < 0.6 floor (honest: no real
  180° line exists between a person and a stove; "honored" is a guess)
- jay_decision: pending — note the audio disagreement: Jev wants the room hum
  to bridge (0.73), plan said hard cut. Recommend accepting Jev's bridge.

### Generation handoff
- Shot B prompt must: open on the stove as the object of Valya's eyeline out
  of S01 — the thing she is looking at, framed as a looked-at object.
- Audio edit note: hard cut; room hum continuous under both.

---

## Transition S02 -> S03

**Beat intent:** dread arrives before the image — then the reveal: the supervisor is dead

**Shot A ends:** burnt paper corner glowing in the ash; stove ticking, fire murmur
**Shot B opens:** slow push-in to the supervisor slumped at his desk, headphones
on, lamp 14 burning; near-silence, faint lamp hum

**Plan (Cosmo's draft):** J-cut. The channel-14 lamp hum starts under the tail
of S02's embers, then picture cuts HARD to the desk — a deliberate shock
reveal. Audio leads, image ruptures. No axis issue (both shots face into the
bay; no shared 180° line to cross).

### Jev verdict (tools/cut_grammar.py)
- cut_type: j_cut (matches the pre-generation plan)
- line_discipline: no_line_applies
- flow: 2.22 @ 0.55
- audio_bridge: p=0.90 — strong yes to the J-cut
- tension: 2.99 (spike — the reveal)
- composite: 0.893

### Routing
- escalated: YES — flow confidence 0.55 < 0.6 floor (the shock reveal reads as
  choppy-to-seamless depending on the viewer; Jay's call on whether the hard
  entrance lands)
- jay_decision: pending

### Generation handoff
- Shot C prompt must: expect the lamp hum to arrive early — open on the
  reveal composed for a hard entrance, no pickup of S02's motion.
- Audio edit note: J-cut, lamp hum ~12 frames early; picture cuts hard.
