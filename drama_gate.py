#!/usr/bin/env python3
"""Workflow #11 — Drama concept gates: the shared brain on the arrows.

Two gates for the drama production line, both run BEFORE render credits:

  rank   Rank competing concepts (title + tagline + concept columns). Uses
         per-item Score judgments — order-invariant by construction, so no
         Choice-ordering bias and no pijev needed. The top --advance concepts
         are flagged ADVANCE and earn the ~2-credit poster render.

  cannon Score the text-side Cannon criteria (Buy / Era / Uniqueness) for one
         concept against a poster description (from a vision model or your own
         read of the generated poster). Glance and Thumbnail remain visual
         criteria — judge the actual image at thumbnail size; this gate covers
         the three a judgment model can calibrate.

Verdicts are probability-banded: the probabilities tell you what, the band
tells you whether to act. CONDITIONAL names the weakest criterion so any
regeneration is targeted, not vibes.

Usage:
    python3 drama_gate.py rank concepts.csv [--advance 1] [--out ranked_concepts.csv]
    python3 drama_gate.py cannon --title "T" --tagline "T" --era "1970s giallo" \
        --concept "..." --poster "description of the poster" \
        [--prior "prior key visual;another prior"] [--out verdict.json]
    python3 drama_gate.py selftest
"""
import argparse
import csv
import json
import sys

from typesafe import ask

CONCEPT_TEXT_COLUMNS = ["concept", "premise", "logline", "idea", "brief", "text"]

HOOK_LEVELS = [
    "No image: concept has no singular visual moment; any poster would be generic",
    "Weak: a key visual exists but is stock-familiar",
    "Decent: clear key visual, though seen in this genre before",
    "Strong: one explosive, specific image sells the concept instantly",
    "Iconic: the poster image alone is the pitch, legible at thumbnail size",
]
ERA_LEVELS = [
    "Anywhere: no period identity, could be any decade",
    "Faint: era is claimed but adds no look or texture",
    "Present: era informs palette and wardrobe",
    "Exploitable: era delivers free production design and a distinctive texture",
    "Iconic: the era IS the hook — stock, palette, and typography sell it",
]
ENGINE_LEVELS = [
    "One gag: single gimmick, dead after one episode",
    "Thin: premise carries a pilot but little beyond",
    "Solid: a season of conflict from the core situation",
    "Generative: the premise regenerates episodes on its own",
    "Endless: compounding premise — new hooks arrive naturally",
]


def find_named(fieldnames, names):
    for cand in names:
        for f in fieldnames:
            if f.strip().lower() == cand:
                return f
    return None


def resolve_columns(fieldnames):
    title_col = find_named(fieldnames, ["title", "name"])
    tagline_col = find_named(fieldnames, ["tagline", "hook"])
    concept_col = find_named(fieldnames, CONCEPT_TEXT_COLUMNS)
    if concept_col is None:
        concept_col = next(
            (f for f in fieldnames if f not in (title_col, tagline_col)), fieldnames[0]
        )
    return title_col, tagline_col, concept_col


def rank(csv_path, advance, out_path):
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        title_col, tagline_col, col = resolve_columns(reader.fieldnames)
        rows = [r for r in reader if (r.get(col) or "").strip()]

    state = {}
    questions = {}
    for i, row in enumerate(rows):
        state[f"c{i}"] = {
            "title": (row.get(title_col) or "").strip() if title_col else "",
            "tagline": (row.get(tagline_col) or "").strip() if tagline_col else "",
            "concept": row[col].strip(),
        }
        questions[f"c{i}_hook"] = {
            "type": "score",
            "instructions": f"How strong is the poster moment of concept `c{i}` — would it sell in ONE image to a scrolling viewer?",
            "criteria": HOOK_LEVELS,
        }
        questions[f"c{i}_era"] = {
            "type": "score",
            "instructions": f"How distinct and exploitable is the era/aesthetic of concept `c{i}` as a visual identity?",
            "criteria": ERA_LEVELS,
        }
        questions[f"c{i}_engine"] = {
            "type": "score",
            "instructions": f"How much series engine does concept `c{i}` have — can the premise keep generating episodes and hooks without exhausting itself?",
            "criteria": ENGINE_LEVELS,
        }

    print(f"Ranking {len(rows)} concept(s)...")
    answers, usage = ask(state, questions)

    out_rows = []
    for i, row in enumerate(rows):
        a = answers[f"c{i}_hook"]["score"], answers[f"c{i}_era"]["score"], answers[f"c{i}_engine"]["score"]
        r = dict(row)
        r["hook"], r["era"], r["engine"] = (f"{x:.2f}" for x in a)
        r["total"] = f"{sum(a):.2f}"
        out_rows.append(r)
    out_rows.sort(key=lambda r: float(r["total"]), reverse=True)
    for j, r in enumerate(out_rows):
        r["gate"] = "ADVANCE" if j < advance else "HOLD"

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    for r in out_rows:
        print(f"  {r['gate']:<7} total {r['total']:>5}  hook {r['hook']}  era {r['era']}  engine {r['engine']}  | {(r.get('title') or r[col])[:60]}")
    print(f"Usage: {usage['input_tokens']} in / {usage['output_tokens']} out tokens")


def verdict_band(probs):
    weakest = min(probs, key=probs.get)
    lo = probs[weakest]
    if lo >= 0.75:
        return "GREENLIT", weakest
    if lo >= 0.50:
        return "CONDITIONAL", weakest
    return "KILLED", weakest


def cannon(title, tagline, era, concept, poster, prior, out_path):
    state = {"title": title, "tagline": tagline, "era": era, "concept": concept,
             "poster": poster, "prior_runs": prior}
    questions = {
        "buy": {
            "type": "noul",
            "instructions": "Judging `title`, `tagline`, `concept` and `poster` together: would a casual scrolling viewer act on this poster alone — click, watch, or remember it?",
            "criteria": {"true": "The poster makes one specific promise the viewer wants; a clear watch trigger",
                          "false": "Generic or confusing promise; scroll-past material"},
        },
        "era_authentic": {
            "type": "noul",
            "instructions": "Does `poster` read as authentically from `era` — period-correct stock, palette, typography, composition — rather than a modern image with vintage styling?",
            "criteria": {"true": "Period-authentic craft choices throughout",
                          "false": "Modern cleanliness, wrong stock or typography, era cosplay"},
        },
        "unique": {
            "type": "noul",
            "instructions": "Is the key visual of `poster` distinct from `prior_runs` (if any) and from interchangeable AI-poster patterns?",
            "criteria": {"true": "Distinct key visual; not interchangeable with prior posters",
                          "false": "Interchangeable with prior runs or stock AI-poster look"},
        },
    }
    answers, usage = ask(state, questions)
    probs = {k: answers[k]["noul"] for k in questions}
    verdict, weakest = verdict_band(probs)

    result = {"title": title, "era": era, "criteria": {k: f"{v:.2f}" for k, v in probs.items()},
              "verdict": verdict, "weakest_criterion": weakest,
              "pending_visual_criteria": ["glance", "thumbnail"],
              "usage": usage}
    print(f"  buy {probs['buy']:.2f}  era {probs['era_authentic']:.2f}  unique {probs['unique']:.2f}")
    print(f"  -> {verdict} (weakest: {weakest} at {probs[weakest]:.2f})")
    if verdict == "CONDITIONAL":
        print(f"     Regenerate with a targeted fix to '{weakest}', not a full redo.")
    print("  Pending visual criteria: glance + thumbnail — judge the actual image at thumbnail size.")
    print(f"Usage: {usage['input_tokens']} in / {usage['output_tokens']} out tokens")
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)


def selftest():
    assert verdict_band({"buy": 0.9, "era_authentic": 0.8, "unique": 0.95})[0] == "GREENLIT"
    assert verdict_band({"buy": 0.9, "era_authentic": 0.6, "unique": 0.95}) == ("CONDITIONAL", "era_authentic")
    assert verdict_band({"buy": 0.4, "era_authentic": 0.9, "unique": 0.95})[0] == "KILLED"
    tmp = ROOT / "selftest_concepts.csv"
    tmp.write_text("title,tagline,concept\nT1,G1,C1\nT2,G2,C2\n", encoding="utf-8")
    with open(tmp, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        title_col, tagline_col, col = resolve_columns(reader.fieldnames)
        rows = list(reader)
    assert (title_col, tagline_col, col) == ("title", "tagline", "concept")
    assert len(rows) == 2 and rows[1][title_col] == "T2"
    tmp.write_text("idea\nJust one column\n", encoding="utf-8")
    with open(tmp, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        title_col, tagline_col, col = resolve_columns(reader.fieldnames)
        assert title_col is None and col == "idea"
    tmp.unlink()
    print("drama_gate selftest: PASS (verdict bands, column resolution; no API calls)")
    return 0


ROOT = __import__("pathlib").Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("rank")
    r.add_argument("csv_path")
    r.add_argument("--advance", type=int, default=1)
    r.add_argument("--out", default="ranked_concepts.csv")
    c = sub.add_parser("cannon")
    c.add_argument("--title", required=True)
    c.add_argument("--tagline", default="")
    c.add_argument("--era", required=True)
    c.add_argument("--concept", required=True)
    c.add_argument("--poster", required=True)
    c.add_argument("--prior", default="", help="Prior run key visuals, ';'-separated, for uniqueness")
    c.add_argument("--out", default=None)
    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "rank":
        rank(args.csv_path, args.advance, args.out)
    else:
        prior = [p.strip() for p in args.prior.split(";") if p.strip()]
        cannon(args.title, args.tagline, args.era, args.concept, args.poster, prior, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
