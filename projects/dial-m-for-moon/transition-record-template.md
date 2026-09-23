# Transition Record Template

One record per cut (shot A → shot B). Fill the plan; Jev judges it; Jay owns
escalations. See `editing-doctrine.md` for the grammar and the routing rules.

```markdown
## Transition S__ -> S__

**Beat intent:** (the dramatic job this cut must do, one line)

**Shot A ends:**   (final frame, action, gaze, audio out)
**Shot B opens:**  (first frame, action, gaze, audio in)

### Jev verdict (tools/cut_grammar.py)
- cut_type:            (choice + top probabilities)
- line_discipline:     (choice + confidence)
- flow:                (score /3 + confidence)
- audio_bridge:        (p — J/L-cut advised?)
- tension:             (score /3 — pacing arc)
- composite:           (0..1, code weights)

### Routing
- escalated: (yes/no — which rule fired)
- jay_decision: (final grammar, or "accept Jev")

### Generation handoff
- Shot B prompt must: (e.g. "open mid-reach completing S__'s gesture;
  camera on the same side of the 180° line; SEVEN-THREE line starts under
  the tail of S__ (J-cut)")
- Audio edit note: (J-cut / L-cut / hard cut + offset in frames)
```
