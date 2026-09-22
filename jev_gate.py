"""Jev judgment gate — the skill-correct ranking pattern as a reusable tool.

Method (docs.typesafe.ai/agent-skill):
  - one NARROW judgment per question over a factual state
  - weights combined in code, never in the prompt
  - a none_of_these option so the model can reject the candidate set
  - criteria order rotated across requests and averaged (permutation
    invariance, per TypeLLM/pijev) so no candidate wins by listing order

Usage:
    python3 jev_gate.py gate.json [--rotations 4] [--out result.json]

gate.json shape:
    {
      "state":     { ... factual context, no judgment criteria ... },
      "criteria":  { "id": "candidate description", ... },
      "dimensions":{ "dim": "single-judgment question", ... },
      "weights":   { "dim": 0.30, ... }   # must sum ~1.0
    }

Answer shape follows the raw systemone API: answers[id] carries the chosen
option plus a probabilities map; probabilities drive the ranking, not choice.
"""
import argparse
import json
import random
import sys
from pathlib import Path

from typesafe import ask

NONE_LABEL = "none_of_these"


def rotate(criteria, seed):
    items = list(criteria.items())
    random.Random(seed).shuffle(items)
    return dict(items)


def run_gate(gate, rotations=4, model="jev-latest"):
    state = gate["state"]
    dims = gate["dimensions"]
    weights = gate["weights"]
    criteria = dict(gate["criteria"])
    names = list(criteria) + [NONE_LABEL]

    total = sum(weights.values())
    if abs(total - 1.0) > 0.01:
        sys.exit(f"weights sum to {total:.3f}, expected ~1.0")

    scores = {n: 0.0 for n in names}
    per_dim = {}
    for rot in range(rotations):
        rotated = rotate(criteria, seed=rot)
        questions = {
            dim: {
                "type": "choice",
                "instructions": q,
                "criteria": {**rotated, NONE_LABEL: "None of these candidates is strong enough."},
            }
            for dim, q in dims.items()
        }
        answers, usage = ask(state, questions, model=model)
        for dim in dims:
            ans = answers[dim]
            probs = ans.get("probabilities", ans) if isinstance(ans, dict) else ans
            per_dim.setdefault(dim, {n: 0.0 for n in names})
            for n, v in probs.items():
                per_dim[dim][n] += v / rotations
                if n in scores:
                    scores[n] += weights[dim] * v / rotations
    return scores, per_dim


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gate", help="gate JSON file (state/criteria/dimensions/weights)")
    ap.add_argument("--rotations", type=int, default=4)
    ap.add_argument("--out", help="write full result JSON here")
    args = ap.parse_args()

    gate = json.loads(Path(args.gate).read_text())
    scores, per_dim = run_gate(gate, rotations=args.rotations)

    print("\n== dimension winners ==")
    for dim, probs in per_dim.items():
        top = max(probs.items(), key=lambda kv: kv[1])
        print(f"  {dim:<20} {top[0]:<24} {top[1]:.2f}")

    print("\n== weighted total ==")
    for n, s in sorted(scores.items(), key=lambda kv: -kv[1]):
        print(f"  {s:.3f}  {n}")

    if args.out:
        Path(args.out).write_text(json.dumps(
            {"gate": gate, "scores": scores, "per_dimension": per_dim,
             "rotations": args.rotations}, indent=1))
        print(f"\nresult -> {args.out}")


if __name__ == "__main__":
    main()
