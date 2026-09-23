# Editing Doctrine — Inter-Shot Cut Grammar

Adopted 2026-09-23 by Jay. Companion to the per-shot Eyecandy grammar layer (`jevmax/creative/eyecandy-catalog.md`).
That layer governs what each shot **is**; this one governs how shots **connect**.

## 1. The problem it solves

EP001 final v1 was assembled from ten independently generated hero takes placed in
storyboard order — "postcard cutting." Each take starts and ends in its own world:
no match on action between shots, no eyeline handoffs, no audio leading or
lingering across cuts. The result reads as a mood piece rather than a directed
film: the pacing sits flat, the officer's entrance lands soft, and the ending
stops instead of landing.

Diagnosis: the project had a grammar for shots but no grammar for **transitions**.

## 2. The grammar

Two families of cuts. A film needs both, and each transition is a deliberate choice.

**Continuity cuts (invisible — the audience should not feel them):**

| Cut | Rule of use |
|---|---|
| Match on action | Cut mid-movement (reach, turn, rise). The motion masks the edit. Frame size must change noticeably across the cut or it becomes a jump cut. |
| Eyeline match | A gaze in shot A creates a debt: shot B must pay it by showing what was seen, from a position consistent with that gaze. |
| Shot / reverse shot | Dialogue workhorse. Alternate singles from one side of the 180° line, respecting eyeline and the 30° rule. |
| J-cut | Incoming shot's audio arrives *before* its picture. Pulls the audience forward; builds tension. |
| L-cut | Outgoing shot's audio lingers *over* the next picture. Gives release and reflection. |

**Hard cuts (felt — the audience should notice the break):**

| Cut | Rule of use |
|---|---|
| Smash cut | Abrupt collision for shock or irony. Spend it rarely. |
| Jump cut | Same subject, same angle (<30° shift or same framing) with implied time skipped. Reads as rupture — never use it accidentally. |
| Graphic match | Shape/color/motion rhymes across shots; can carry a visual metaphor. |

**Spatial law (applies to every transition):** the 180° rule is a rule, not a
guideline. Crossing the axis without a motivated neutral shot is an error,
however good the take. Deliberate crossing to disorient is allowed — but break it
hard enough that nobody mistakes it for an accident. Screen direction is a
promise made in the first shot; keep it or pay it off.

**Audio law:** audio transitions are cut independently from picture transitions.
Synchronized audio-image cuts at every transition are assembly editing, not
finished editing. Every transition needs an explicit audio decision (J-cut,
L-cut, or hard cut with cause).

**Murch's law (supersedes all of the above):** emotion is the first criterion.
A technically perfect continuity match between two takes of the wrong emotional
temperature produces a seamless cut of the wrong moment. Deliberate deviations
from continuity must be deliberate, never accidental.

## 3. Jev's role (per the TypeSafe skill and docs)

Jev is TypeSafe's System One model: it returns **typed judgments and
probabilities, not generated text**. It is not a chat or code-completion LLM and
is not a drop-in replacement for the coding agent. The correct architecture is:
the agent/code proposes, Jev **judges**.

This project already uses Jev this way (the skill's *select instead of generate*
pattern): rank gates, poster gates, and take selection — Jev scores and selects
between candidates the pipeline produced. It never writes.

The editing layer follows the same contract:

- **I (Cosmo) draft** the transition plan — the creative writing.
- **Jev judges** each transition with typed answers (Choice / Score / Noul).
- **Code owns the workflow**: routing, confidence gating, composite weights,
  escalation. Policy is explicit and weights are retunable in code without
  re-running inference.

Jev fits this job for the three reasons the docs name: the cut type is a route to
a fixed set of destinations, flow is a rubric score to branch on, and typed
answers replace fragile "return JSON" prompting.

## 4. The judgment design

One TypeSafe request per transition (shot A → shot B). All independent and
speculative questions are asked **together** — they run in parallel at ~no extra
latency, and code consumes the applicable answers. Questions cannot see one
another's answers, so audio and picture judgments stay independent by
construction.

**State** (named JSON fields, complete meaning in the fields — the model never
sees our question ids):

```json
{
  "episode": "EP002",
  "transition": "S03->S04",
  "style_policy": "1959 16mm Kodak Ektachrome, 9:16 vertical, period-true",
  "shot_a": { "summary": "...", "ending_frame": "...", "ending_action": "...", "ending_gaze": "...", "audio_out": "..." },
  "shot_b": { "summary": "...", "opening_frame": "...", "opening_action": "...", "opening_gaze": "...", "audio_in": "..." },
  "beat_intent": "the dramatic job this transition must do"
}
```

**Questions** (exact schema lives in `tools/cut_grammar.py`):

1. `cut_type` — **Choice.** Which grammar best serves this transition?
   Options: `match_on_action`, `eyeline_match`, `shot_reverse_shot`, `j_cut`,
   `l_cut`, `graphic_match`, `smash_cut`, `straight_cut`, `none_of_above`.
   Each option carries what it covers and what it excludes, so the options are
   separable. `none_of_above` is mandatory — the model cannot choose an omitted
   value, so the list must admit its own incompleteness.
2. `line_discipline` — **Choice.** `line_honored`, `crossed_intentional`,
   `crossed_accidental`, `no_line_applies`.
3. `flow` — **Score** on concrete ordered levels:
   0 = disorienting, breaks the scene · 1 = choppy, the edit shows ·
   2 = serviceable, carries the beat · 3 = seamless, the cut disappears.
4. `audio_bridge` — **Noul.** Probability that the audio should lead or linger
   across the picture cut (J- or L-cut) rather than cutting with it. Near 0.5
   means genuine ambiguity, not "medium" — see routing.
5. `tension` — **Score** on the escalation curve: 0 = release / exhale ·
   1 = hold · 2 = build · 3 = spike. This is descriptive (what the beat demands),
   not a quality grade; it feeds the pacing arc, not the composite.

## 5. Confidence-gated routing → escalation to Jay

Confidence is the second axis: the answer tells us *what*, confidence tells us
*whether to act*. Thresholds scale with consequence (per the docs' canonical
pattern — check a balance at 0.6, approve a transfer at 0.85):

- **0.6 floor (any question):** below it, the transition routes to Jay. This is
  the existing project rule ("near-0.5 / low-confidence escalates"), now with a
  number the docs bless.
- **`audio_bridge` in [0.4, 0.6]:** ambiguous by definition → Jay.
- **`line_discipline = crossed_accidental`:** always escalates. It is an error,
  not a style.
- **`cut_type = smash_cut` or `crossed_intentional`:** high-stakes, audience-felt
  cuts — need confidence > 0.85 or they go to Jay.
- **`cut_type = none_of_above`:** escalates. The grammar list failed; a human
  invents the treatment.
- **Low stakes auto-apply:** `straight_cut` at ≥ 0.6 confidence needs no human.

## 6. Composite scoring (code-owned weights)

"Does this transition work" is one composite number from atomic judgments, so
Jay can retune the recipe without re-running inference:

```
composite = 0.40 * (flow / 3)
          + 0.30 * cut_type.confidence
          + 0.20 * line_ok          # 1 unless crossed_accidental
          + 0.10 * audio_decided    # 1 unless audio_bridge in [0.4, 0.6]
```

Weights live in `tools/cut_grammar.py`. Changing them changes the edit sheet,
never the Jev calls.

## 7. Workflow placement

- **EP002+:** pre-generation gate. Every storyboarded transition gets a
  transition record (`transition-record-template.md`) with its Jev verdict and
  Jay's call on escalations *before* shot budgets are spent. Shot B's prompt is
  then written to honor the decided grammar (e.g. "opens mid-reach, completing
  the gesture from S03").
- **EP001 retro:** run the judge over the 9 existing transitions and score where
  the postcard cutting shows. Spot-check Jev's answers against Jay's judgment —
  the docs require validating in the target domain before trusting the gate.

## 8. Norms

- Jev judges; it does not write. The transition plan is drafted by the agent.
- Jay owns directorial calls. Jev is the second opinion and the tiebreaker on
  ambiguous transitions — never the auteur.
- Typed output guarantees the interface, not the truth. Spot-check, then trust.

## 9. Tail-frame conditioning (validated 2026-09-23, EP002 test)

For continuity cuts, extract shot A's last frame and pass it into shot B's
generation:
- **Match on action / eyeline match / graphic match:** pass A's tail frame
  as B's reference. For eyeline matches, state explicitly that the new shot
  is the *object of the gaze* — and if the person must not appear, say so
  outright ("she does not appear"), or the generator will continue them
  instead of cutting away (observed EP002 S02 v2).
- **J-cut / L-cut / smash / collision:** do NOT condition the picture on
  A's tail frame. The rupture is the point. For J/L-cuts, carry the bridge
  in the sound description instead.
- Measured effect (EP002): T1 eyeline composite 0.945 → 0.953 and the
  line_discipline escalation cleared; T2 J-cut composite 0.893 → 0.864,
  flow escalation unchanged — conditioning helped the continuity cut and
  did nothing for the rupture, as predicted.
- For match on action, the prompt must explicitly FORBID reframing
  ("do NOT pull back, do NOT change angle"), not just ask for continuation —
  otherwise the generator widens the shot and the gesture breaks
  (EP003 S02 take1: 0.722 with 3 escalations → take2: 0.991, zero).
- Intra-shot set continuity: when the camera moves inside a generated shot,
  the model invents new background per angle — the room morphs (EP003 S03
  take1: three different walls in 10 seconds). Fix: lock the camera
  ("does not move, pan, tilt, or rotate at any point") and state the
  background stays identical; the performer moves within the fixed frame.
  Caveat learned 2026-09-23: the locked camera fixed take1's gross morph and
  take2 holds headset, bun, and red pencil — but the model can still
  RE-DRESS the set under a locked camera (take2: the right-side jackfield
  becomes a meter panel between head and tail). The lock is necessary but
  not sufficient; verify with the QC below.
- QC step: run `tools/qc_continuity.py` on every take (supersedes
  `tools/qc_shot_lock.py`, kept as a classical fallback). Three signals,
  all CPU-friendly: CLIP ViT-B/32 cosine similarity across 8 evenly-sampled
  frames (min consecutive-frame sim, head-vs-tail sim), Farneback dense
  optical flow median magnitude at 320px width (motion energy), and
  consecutive grayscale MSE as an informational change detector. FLAG if
  min_consecutive < 0.90, head_tail < 0.85, or max median flow > 2.0px.
  Calibrated 2026-09-23: LOCKED (S02 take2) 0.931/0.927/0.6px -> PASS;
  DRIFT (S03 take1) 0.903/0.779/19.6px -> FLAG; REDRESS (S03 take2)
  0.866/0.831/13.5px -> FLAG (both CLIP branches — the subtle re-dress is
  real); SWEEP (S01 take1, legit action) 0.875/0.861/26.9px -> FLAG. A FLAG
  means human review, not auto-reject; use --allow-motion for action shots
  where the subject legitimately sweeps the frame (there flow is
  informational and CLIP still flags for review).
- The depth model (Depth-Anything-V2-Small) was tried for this QC job and
  REJECTED 2026-09-23: its relative depth is scene-context dependent — the
  same wall scores different depth when foreground composition changes, so a
  truly locked take scored the same "drift" as a drifting one. Depth maps
  are independently inferred and normalized per frame (scale/shift
  ambiguity, no temporal constraint) — cross-frame depth comparison is
  invalid by construction; the model is reserved for single-frame creative
  work (keyframe structure gating, depth-driven post, 3D Ken Burns
  fillers). Continuity QC is CLIP + optical flow + MSE; DINO/ORB and
  heavier point trackers are available if this minimal stack ever misses,
  but are not needed today.

## Full-library audit 2026-09-23 — gate scope correction
- Ran `tools/qc_continuity.py --allow-motion` over all 42 takes of
  EP001/EP002/EP003: 41 FLAG, 1 PASS (EP003 S02 take2, the known-locked
  shot — the tool behaves exactly as calibrated).
- The flags are almost entirely CLIP-similarity, not motion: EP001/EP002
  moving-camera shots (push-ins, rack focuses, S10's vignette/flicker
  finale) sit at 0.65–0.89 head-tail, below gates calibrated on locked-off
  EP003 material. S10 scores ~0.48–0.53 (deliberate stylization, already
  shipped as EP001 v1 — the flag describes the style, it does not
  invalidate it).
- Correction: the 0.90/0.85 gates are a PASS/FAIL rule ONLY for locked-
  camera continuity shots (the EP004 discipline). For shots with deliberate
  camera movement, a FLAG means "eyeball the head/tail frames," not fail.
  Shipped episodes are unaffected; the one EP003 winner flag (S03 take2,
  0.866/0.831) is the known, accepted subtle re-dress.
- Going forward: keep EP004 cameras locked wherever the storyboard allows
  it, run the QC on every take, and require PASS on locked shots.
