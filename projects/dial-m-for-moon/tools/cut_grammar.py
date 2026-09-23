"""Cut-grammar judge for Dial M for Moon transitions.

One TypeSafe (Jev) request per transition (shot A -> shot B), five questions in
parallel. Jev JUDGES the cut; it never writes the transition plan. Code owns
the workflow: routing, confidence gating, composite weights, escalation.

Usage:
    python tools/cut_grammar.py transitions.json [--dry-run]

transitions.json: list of
    {"episode": "EP002", "transition": "S03->S04",
     "shot_a": {"summary": ..., "ending_frame": ..., "ending_action": ...,
                "ending_gaze": ..., "audio_out": ...},
     "shot_b": {"summary": ..., "opening_frame": ..., "opening_action": ...,
                "opening_gaze": ..., "audio_in": ...},
     "beat_intent": "..."}

Exit code 0 = no escalations, 2 = one or more transitions need Jay.
Stdlib only — uses the repo-root typesafe.py client.
"""
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
from typesafe import ask  # noqa: E402

STYLE_POLICY = "1959 16mm Kodak Ektachrome reversal, 9:16 vertical, period-true production design, no modern sci-fi visuals"

# --- Confidence routing (editing-doctrine.md section 5) -----------------------
CONF_FLOOR = 0.6          # below this on any question -> escalate to Jay
HIGH_STAKES_CONF = 0.85   # audience-felt cuts need this or they escalate
AUDIO_AMBIGUOUS = (0.4, 0.6)  # noul band that means genuine ambiguity
HIGH_STAKES_CUTS = {"smash_cut"}

# --- Composite weights (editing-doctrine.md section 6). Code-owned: ---------
# retune freely without re-running Jev.
WEIGHTS = {
    "flow": 0.40,
    "cut_confidence": 0.30,
    "line_ok": 0.20,
    "audio_decided": 0.10,
}

QUESTIONS = {
    "cut_type": {
        "type": "choice",
        "instructions": (
            "Given shot A's ending (final frame, action, gaze, outgoing audio) and "
            "shot B's beginning, which cut grammar best serves this transition? "
            "Choose the single option whose coverage matches the dramatic job."
        ),
        "criteria": {
            "match_on_action": "A movement, gesture, or turn begins in shot A and completes in shot B; the motion masks the edit. Covers continuous physical action across the cut; does NOT cover dialogue exchanges or static-to-static cuts.",
            "eyeline_match": "A character gazes off-screen in shot A and shot B reveals what they saw, from a position consistent with that gaze. Covers gaze->object handoffs; does NOT cover dialogue shot/reverse-shot.",
            "shot_reverse_shot": "Alternating singles of two subjects in dialogue, on one side of the 180-degree line. Covers conversation; does NOT cover action continuation.",
            "j_cut": "Shot B's audio should arrive BEFORE its picture — the incoming sound pulls the audience forward. Covers tension-building scene entries; does NOT cover exits or reflection.",
            "l_cut": "Shot A's audio should linger OVER shot B's picture — the outgoing sound gives release. Covers reflective exits; does NOT cover building forward momentum.",
            "graphic_match": "Shape, color, or motion rhymes across the cut, possibly carrying a visual metaphor. Covers formal rhymes; does NOT cover invisible continuity.",
            "smash_cut": "Deliberate abrupt collision for shock, irony, or rupture. High-stakes: the audience must feel the break as intentional.",
            "straight_cut": "A plain assembly cut with no special grammar — adequate when the shots already connect and nothing is gained by a device.",
            "none_of_above": "None of these grammars fits; the transition needs a custom or unlisted treatment.",
        },
    },
    "line_discipline": {
        "type": "choice",
        "instructions": (
            "Does this transition respect the 180-degree rule and screen direction? "
            "A line exists whenever two subjects or a consistent movement direction are involved."
        ),
        "criteria": {
            "line_honored": "Camera stays on one side of the axis; screen positions and movement direction are consistent across the cut.",
            "crossed_intentional": "The axis is crossed deliberately and hard enough to read as intentional disorientation (chase, panic, rupture).",
            "crossed_accidental": "The axis is crossed or screen direction flips with no dramatic justification — an error.",
            "no_line_applies": "No axis of action exists between these shots (e.g. pure insert, graphic match between unrelated spaces).",
        },
    },
    "flow": {
        "type": "score",
        "instructions": "How well does this transition carry the scene's rhythm and legibility?",
        "criteria": [
            "Disorienting; breaks the scene. The audience loses space, time, or the thread.",
            "Choppy; the edit shows. Understandable but mechanical — assembly-cutting.",
            "Serviceable; carries the beat. The cut does its job without calling attention.",
            "Seamless; the cut disappears. Space, time, and emotion read as continuous.",
        ],
    },
    "audio_bridge": {
        "type": "noul",
        "instructions": "Should the audio lead or linger across the picture cut (a J-cut or L-cut) rather than cutting with the picture?",
        "criteria": {
            "true": "The transition is better served by offsetting audio from picture: incoming audio arrives early (J-cut) or outgoing audio lingers over the next shot (L-cut).",
            "false": "Audio should cut together with the picture — a hard, synchronized audio-image cut is correct here.",
        },
    },
    "tension": {
        "type": "score",
        "instructions": "What dramatic register does this transition demand on the episode's escalation curve? (Descriptive, not a quality grade.)",
        "criteria": [
            "Release / exhale. The scene lets go here.",
            "Hold. Sustains the current pressure without raising it.",
            "Build. Pressure rises across the cut.",
            "Spike. A jolt, revelation, or rupture.",
        ],
    },
}


def build_state(episode, transition, shot_a, shot_b, beat_intent):
    """Named JSON fields — complete meaning in the fields; Jev never sees our ids."""
    return {
        "episode": episode,
        "transition": transition,
        "style_policy": STYLE_POLICY,
        "shot_a": shot_a,
        "shot_b": shot_b,
        "beat_intent": beat_intent,
    }


def judge_transition(state, retries=3):
    import time

    last = None
    for attempt in range(retries):
        try:
            answers, _usage = ask(state, QUESTIONS)
            return answers
        except OSError as e:  # transient drops through the egress proxy
            last = e
            time.sleep(2.0 * (attempt + 1))
    raise last


def composite(answers, weights=WEIGHTS):
    flow = answers["flow"]["score"] / 3.0
    cut_conf = answers["cut_type"]["confidence"]
    line_ok = 0.0 if answers["line_discipline"]["choice"] == "crossed_accidental" else 1.0
    p_audio = answers["audio_bridge"]["noul"]
    audio_decided = 0.0 if AUDIO_AMBIGUOUS[0] <= p_audio <= AUDIO_AMBIGUOUS[1] else 1.0
    return (
        weights["flow"] * flow
        + weights["cut_confidence"] * cut_conf
        + weights["line_ok"] * line_ok
        + weights["audio_decided"] * audio_decided
    )


def route(answers):
    """Confidence-gated routing. Returns (verdict_summary, escalations list)."""
    escalations = []

    def check(name, ans):
        if ans.get("confidence", 1.0) < CONF_FLOOR:
            escalations.append(f"{name}: confidence {ans['confidence']:.2f} below floor {CONF_FLOOR}")

    cut = answers["cut_type"]
    line = answers["line_discipline"]
    flow = answers["flow"]
    check("cut_type", cut)
    check("line_discipline", line)
    check("flow", flow)

    if cut["choice"] == "none_of_above":
        escalations.append("cut_type: none_of_above — grammar list failed, needs a human treatment")
    if cut["choice"] in HIGH_STAKES_CUTS and cut["confidence"] < HIGH_STAKES_CONF:
        escalations.append(
            f"cut_type: {cut['choice']} is high-stakes, needs > {HIGH_STAKES_CONF} confidence (got {cut['confidence']:.2f})"
        )
    if line["choice"] == "crossed_intentional" and line["confidence"] < HIGH_STAKES_CONF:
        escalations.append(
            f"line_discipline: deliberate crossing needs > {HIGH_STAKES_CONF} confidence (got {line['confidence']:.2f})"
        )
    if line["choice"] == "crossed_accidental":
        escalations.append("line_discipline: crossed_accidental — axis error, must be re-blocked")
    p_audio = answers["audio_bridge"]["noul"]
    if AUDIO_AMBIGUOUS[0] <= p_audio <= AUDIO_AMBIGUOUS[1]:
        escalations.append(f"audio_bridge: p={p_audio:.2f} is ambiguous — Jay decides J/L/hard")

    verdict = {
        "cut_type": cut["choice"],
        "line_discipline": line["choice"],
        "flow": round(flow["score"], 2),
        "audio_bridge_p": round(p_audio, 2),
        "tension": round(answers["tension"]["score"], 2),
        "composite": round(composite(answers), 3),
    }
    return verdict, escalations


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    with open(argv[1]) as f:
        transitions = json.load(f)
    dry_run = "--dry-run" in argv

    any_escalation = False
    for t in transitions:
        tid = f"{t['episode']} {t['transition']}"
        state = build_state(t["episode"], t["transition"], t["shot_a"], t["shot_b"], t["beat_intent"])
        if dry_run:
            print(f"--- {tid} (dry run)")
            print(json.dumps({"state": state, "questions": QUESTIONS}, indent=2, ensure_ascii=False)[:2000])
            print("... [truncated]")
            continue
        answers = judge_transition(state)
        verdict, escalations = route(answers)
        print(f"--- {tid}")
        print(json.dumps(verdict, indent=2, ensure_ascii=False))
        if escalations:
            any_escalation = True
            for e in escalations:
                print(f"  ESCALATE: {e}")
    return 2 if any_escalation else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
