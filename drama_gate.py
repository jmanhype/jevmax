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
    python3 drama_gate.py episodes episode_map.csv [--advance 5] [--out ranked_episodes.csv]
    python3 drama_gate.py canon bible.yaml episode.md [--entities "Name;Prop"] [--out canon_report.json]
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


HOOK_EP_LEVELS = [
    "Dead air: opens on setup or recap, no tension, scroll-away",
    "Weak: some motion but the first beat is administrative",
    "Decent: clear promise but a familiar pattern for the genre",
    "Strong: cold-opens on trouble in progress, question raised in seconds",
    "Exceptional: instant pattern-interrupt, the hook IS the premise",
]
CLIFF_LEVELS = [
    "None: episode resolves cleanly, no reason to return",
    "Soft: mild curiosity, easily abandoned",
    "Decent: real question raised but predictable",
    "Strong: threat or reversal lands on the final beat, unresolved",
    "Exceptional: gut-punch button that demands the next episode immediately",
]
PRODUCE_LEVELS = [
    "Expensive: new locations, new cast, crowd or action set-pieces",
    "Costly: mostly new sets or one new principal character",
    "Moderate: mix of existing sets and a couple of new elements",
    "Cheap: existing sets and cast, new blocking only",
    "Cheapest: single existing set, Element-anchored principals only",
]


def episodes(csv_path, advance, out_path):
    """Gate the episode map BEFORE any shot is budgeted (~60 cr/shot downstream)."""
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        ep_col = find_named(fields, ["episode", "ep", "number"]) or fields[0]
        title_col = find_named(fields, ["title"])
        beat_col = find_named(fields, ["beat", "summary", "episode", "ep", "synopsis", "description", "concept"]) or fields[-1]
        cliff_col = find_named(fields, ["cliffhanger", "button", "end"])
        rows = [r for r in reader if (r.get(beat_col) or "").strip()]

    state = {}
    questions = {}
    for i, row in enumerate(rows):
        state[f"e{i}"] = {
            "episode": (row.get(ep_col) or str(i + 1)).strip(),
            "title": (row.get(title_col) or "").strip() if title_col else "",
            "beat": row[beat_col].strip(),
            "cliffhanger": (row.get(cliff_col) or "").strip() if cliff_col else "",
        }
        questions[f"e{i}_hook"] = {
            "type": "score",
            "instructions": f"How strong is the OPENING hook of episode `e{i}` — would it hold a vertical-drama viewer past the first seconds?",
            "criteria": HOOK_EP_LEVELS,
        }
        questions[f"e{i}_cliff"] = {
            "type": "score",
            "instructions": f"How strong is the ENDING button of episode `e{i}` — cliffhanger field if present, else the beat as written?",
            "criteria": CLIFF_LEVELS,
        }
        questions[f"e{i}_cost"] = {
            "type": "score",
            "instructions": f"How cheap is episode `e{i}` to produce with existing sets and Element-anchored principals? Higher = fewer new assets needed.",
            "criteria": PRODUCE_LEVELS,
        }

    print(f"Gating {len(rows)} episode(s)...")
    answers, usage = ask(state, questions)

    out_rows = []
    for i, row in enumerate(rows):
        a = (answers[f"e{i}_hook"]["score"], answers[f"e{i}_cliff"]["score"], answers[f"e{i}_cost"]["score"])
        r = dict(row)
        r["hook"], r["cliffhanger_score"], r["producibility"] = (f"{x:.2f}" for x in a)
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
        print(f"  {r['gate']:<7} total {r['total']:>5}  hook {r['hook']}  cliff {r['cliffhanger_score']}  cheap {r['producibility']}  | ep {r.get('episode', '?')}")
    print(f"Usage: {usage['input_tokens']} in / {usage['output_tokens']} out tokens")


CANON_OPTIONS = {
    "consistent": "The script's use of the entity matches the bible's specification in every visible detail",
    "contradicts": "The script's use of the entity conflicts with a specific fact in the bible",
    "bible_silent": "The bible does not specify what the script asserts about this entity",
}
AUTO_ACCEPT = 0.80


def canon_verdict(option, prob):
    if option == "contradicts" and prob >= AUTO_ACCEPT:
        return "FAIL"
    if option == "consistent" and prob >= AUTO_ACCEPT:
        return "PASS"
    return "REVIEW"


def canon(bible_path, script_path, entities_arg, out_path):
    """Citation-check transplant: script facts vs the story/identity bible.

    Deterministic pass first (entity mentioned at all — free), then one Choice
    per mentioned entity: consistent / contradicts / bible_silent. Verdicts are
    confidence-banded; anything not auto-accepted goes to the human.
    """
    bible = open(bible_path, encoding="utf-8").read()
    script = open(script_path, encoding="utf-8").read()
    entities = [e.strip() for e in entities_arg.split(";") if e.strip()]
    if not entities:
        import re
        entities = sorted(set(re.findall(r"^\s*name:\s*(.+)$", bible, re.M)))

    mentioned = [e for e in entities if e.lower() in script.lower()]
    missing = [e for e in entities if e not in mentioned]
    if missing:
        print(f"  not mentioned in script (free check): {', '.join(missing)}")
    if not mentioned:
        print("canon: no bible entities appear in the script — nothing to check.")
        return

    state = {"bible": bible, "script": script}
    questions = {}
    for e in mentioned:
        questions[f"canon_{e}"] = {
            "type": "choice",
            "instructions": f"Judging `bible` and `script` together: how does the script's use of '{e}' relate to the bible's specification of '{e}'?",
            "criteria": CANON_OPTIONS,
        }
    answers, usage = ask(state, questions)

    report = []
    for e in mentioned:
        a = answers[f"canon_{e}"]
        option = max(a["probabilities"], key=a["probabilities"].get)
        prob = a["probabilities"][option]
        verdict = canon_verdict(option, prob)
        report.append({"entity": e, "judgment": option, "probability": f"{prob:.2f}", "verdict": verdict})
        print(f"  {verdict:<6} {e}: {option} at {prob:.2f}")
    flagged = [r for r in report if r["verdict"] != "PASS"]
    print(f"  -> {len(report) - len(flagged)} pass, {len(flagged)} need a human look" if flagged else f"  -> all {len(report)} auto-passed")
    print(f"Usage: {usage['input_tokens']} in / {usage['output_tokens']} out tokens")
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"bible": bible_path, "script": script_path, "entities": report, "usage": usage}, f, indent=2)


def selftest():
    assert verdict_band({"buy": 0.9, "era_authentic": 0.8, "unique": 0.95})[0] == "GREENLIT"
    assert verdict_band({"buy": 0.9, "era_authentic": 0.6, "unique": 0.95}) == ("CONDITIONAL", "era_authentic")
    assert verdict_band({"buy": 0.4, "era_authentic": 0.9, "unique": 0.95})[0] == "KILLED"
    assert canon_verdict("consistent", 0.93) == "PASS"
    assert canon_verdict("contradicts", 0.97) == "FAIL"
    assert canon_verdict("consistent", 0.55) == "REVIEW"
    assert canon_verdict("bible_silent", 0.9) == "REVIEW"
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
    e = sub.add_parser("episodes")
    e.add_argument("csv_path")
    e.add_argument("--advance", type=int, default=5)
    e.add_argument("--out", default="ranked_episodes.csv")
    n = sub.add_parser("canon")
    n.add_argument("bible_path")
    n.add_argument("script_path")
    n.add_argument("--entities", default="", help="';'-separated entities; default: name: fields from the bible")
    n.add_argument("--out", default=None)
    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "rank":
        rank(args.csv_path, args.advance, args.out)
    elif args.cmd == "episodes":
        episodes(args.csv_path, args.advance, args.out)
    elif args.cmd == "canon":
        canon(args.bible_path, args.script_path, args.entities, args.out)
    else:
        prior = [p.strip() for p in args.prior.split(";") if p.strip()]
        cannon(args.title, args.tagline, args.era, args.concept, args.poster, prior, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
