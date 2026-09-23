# EP003 transition records — pre-generation gate (2026-09-23)

## Transition S01 -> S02
- planned_cut: **match_on_action**
- why: S01 ends with her hand pulling the patch cord free; S02 must open
  mid-gesture, the same hand carrying the same cord toward the new socket.
  Screen direction of the pull continues. Tail-frame conditioning applies.
- line: the hand's travel stays on one screen axis; keep it.
- audio plan: room hum continuous under the cut; the plug's click lands in S02.
- beat_intent: one unbroken gesture — the connection is a single movement.

## Transition S02 -> S03
- planned_cut: **match_on_action**
- why: S02 ends with her fingers releasing the seated plug; S03 opens with
  her turn completing away from the board toward the desk, the red pencil
  coming down from over her ear to the logbook. The turn is the matched action.
- line: her body turn keeps its rotational direction across the cut.
- audio plan: room hum continuous; pencil scratch enters in S03.
- beat_intent: the work finishes the way it started — by hand, in the book.

### Jev verdicts — actuals (2026-09-23)
- T1: S02 take1 (generator reframed to a wider shot) judged match_on_action
  @ composite 0.722 with THREE escalations (line_discipline 0.44,
  flow 0.28, audio ambiguous 0.52) — Jev correctly caught the weak handoff.
  S02 take2 with explicit no-reframe instruction ("do NOT pull back, do NOT
  change angle") holds the close framing and continues the gesture:
  re-judged match_on_action, flow 2.93, **composite 0.991, zero escalations**.
  Lesson: for match on action, the prompt must forbid reframing, not just
  ask for continuation. Winner: take2.
- T2: match_on_action, flow 2.76, audio_bridge 0.63, tension 0.62,
  composite 0.968. Clean pass, no escalation. (S03 was conditioned on S02
  take1's tail; take2's tail ends equivalently — patch done, hand released —
  so the handoff holds.)
- S03 take1 had SET DRIFT (Jay spotted it): the camera rotated with her turn
  and the wall behind her morphed across three arrangements (clock row →
  МОСКВА/ЛОНДОН clocks + meter panel → ДЕЖУРНЫЙ ЖУРНАЛ pinboard); bun changed
  shape and the headset vanished mid-shot. S03 take2 fixed it with a
  LOCKED-OFF camera ("camera does not move, pan, tilt, or rotate at any
  point; background stays exactly the same") — background, headset, bun, and
  red pencil all hold across the shot. Re-judged T2 with take2:
  match_on_action, composite 0.973, zero escalations. Winner: take2.
  Doctrine lesson: when the camera moves inside a generated shot, the model
  invents new background per angle — lock the camera for set continuity.

Assembly: assembly/EP003_test_3shot.mp4 (30s, 720x1280) =
S01 take1 + S02 take2 + S03 take1.
v2 assembly: assembly/EP003_test_3shot_v2.mp4 = S01 take1 + S02 take2 + S03 take2.
