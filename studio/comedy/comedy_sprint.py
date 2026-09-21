#!/usr/bin/env python3
"""Jevmax Comedy Test Sprint: premise swarm, filters, and Jev tournaments."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from typesafe import ask_batch


PERSONAS = {
    "absurdist": {
        "label": "Absurdist",
        "angles": [
            "treats the product as an impossible civic institution",
            "extends one small audio annoyance into cosmic bureaucracy",
        ],
    },
    "cynic": {
        "label": "Cynic",
        "angles": [
            "exposes productivity culture as a status performance",
            "frames the promise as a small rebellion against upgrade theater",
        ],
    },
    "worrier": {
        "label": "Worrier",
        "angles": [
            "imagines the most socially awkward low-stakes catastrophe",
            "turns ordinary call noise into an anxious inner monologue",
        ],
    },
    "innocent": {
        "label": "Innocent Literalist",
        "angles": [
            "takes the product promise with embarrassing literal precision",
            "misunderstands a normal social cue because the audio is too clear",
        ],
    },
    "status": {
        "label": "Status Obsessive",
        "angles": [
            "treats the accessory as an unexpected class signal",
            "converts a mundane audio choice into a rivalry",
        ],
    },
    "antimarketing": {
        "label": "Anti-Marketing Critic",
        "angles": [
            "rejects exaggerated technology language in favor of one boring benefit",
            "calls out the absurd gap between ad fantasy and daily reality",
        ],
    },
}

CONTEXTS = [
    "a crowded morning train",
    "an open-plan office",
    "a coffee shop with one broken table leg",
    "a kitchen where dinner is burning",
    "an airport gate with four delayed flights",
    "a home office shared with a loud pet",
    "a library that permits whispering only",
    "a sidewalk construction zone",
    "a family video call with three people talking at once",
    "a hotel lobby with suspiciously perfect furniture",
]

BANNED_CLAIM_PATTERNS = (
    r"\bguarantee[d]?\b",
    r"\b100% safe\b",
    r"\bcures?\b",
    r"\bmedical(?:ly)? (?:proven|grade)\b",
    r"\bbest in the world\b",
    r"\bforever\b",
    r"\bunlimited battery\b",
    r"\bFDA\b",
)

BANNED_NAMES = (
    "elon musk",
    "tim cook",
    "bill gates",
    "mark zuckerberg",
    "jeff bezos",
    "donald trump",
    "taylor swift",
    "kanye west",
)

RATIONALE_LABELS = {
    "specific_tension": "A concrete product tension is visible and capable of escalation.",
    "social_recognition": "The situation is immediately recognizable to the audience.",
    "strong_pattern_interrupt": "The premise changes the expected advertising pattern.",
    "product_organic": "The product is necessary to the joke rather than decorative.",
    "weak_generic": "The joke could apply to any product and needs sharper specificity.",
    "unclear_mapping": "The comedic idea is not yet visually or verbally clear.",
}


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def premise_text(brief: dict[str, Any], persona: str, context: str, variant: int, pain: str) -> str:
    product = brief["product"]
    promise = brief["promise"]
    if persona == "absurdist":
        if variant == 2:
            return f"A neighborhood board in {context} certifies {product} as the only object allowed to explain {pain}."
        return f"{context.capitalize()} appoints {product} as the only legal witness to a public argument about {pain}."
    if persona == "cynic":
        if variant == 2:
            return f"In {context}, a startup demo calls {product} liberation from {pain}, though nothing changes except the wire."
        return f"In {context}, a productivity coach promotes {product} as the moral solution to {pain}."
    if persona == "worrier":
        if variant == 2:
            return f"In {context}, someone rehearses one sentence for minutes, convinced {product} will expose their fear of {pain}."
        return f"In {context}, someone becomes convinced that {product} are broadcasting every private thought about {pain}."
    if persona == "innocent":
        if variant == 2:
            return f"In {context}, someone assumes {product} can legally resolve {pain} because the package said '{promise}'."
        return f"In {context}, someone takes the phrase '{promise}' literally while everyone else reacts to {pain}."
    if persona == "status":
        if variant == 2:
            return f"In {context}, a stranger treats {product} as a quiet membership badge while blaming {pain} on everyone else."
        return f"In {context}, two strangers silently judge each other's rank because one owns {product} and one blames {pain}."
    if variant == 2:
        return f"In {context}, an ad crew promises {product} will erase {pain}, but the director keeps shouting the opposite."
    return f"In {context}, an advertisement for {product} promises escape from {pain}, but the crew refuses to leave."


def generate_premises(brief_path: Path, output: Path) -> None:
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    write_json(output / "brief.json", brief)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for persona_index, (persona, persona_def) in enumerate(PERSONAS.items(), start=1):
        count = 0
        pains = [item.strip() for item in brief["pain"].split(",")]
        pains[-1] = pains[-1].removeprefix("and ").strip()
        for context_index, context in enumerate(CONTEXTS):
            for angle_index, angle in enumerate(persona_def["angles"], start=1):
                count += 1
                pain = pains[(context_index * 2 + angle_index - 1) % len(pains)]
                text = premise_text(brief, persona, context, angle_index, pain)
                key = normalized(text)
                if key in seen:
                    raise ValueError(f"Duplicate generated premise: {text}")
                seen.add(key)
                rows.append(
                    {
                        "premise_id": f"P{persona_index:02d}-{count:02d}",
                        "persona": persona,
                        "persona_label": persona_def["label"],
                        "context": context,
                        "angle": angle,
                        "text": text,
                        "product_tension": f"{pain} / {brief['promise']}",
                        "passed_deterministic_filter": "",
                        "filter_reason": "",
                    }
                )
    write_csv(output / "premises.all.csv", rows)
    print(f"Generated {len(rows)} premises -> {output / 'premises.all.csv'}")


def apply_filters(output: Path) -> None:
    source = load_csv(output / "premises.all.csv")
    if len(source) != 120:
        raise ValueError(f"Expected 120 premises, found {len(source)}")
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in source:
        text = row["text"]
        reasons: list[str] = []
        if row["persona"] not in PERSONAS:
            reasons.append("unknown_persona")
        if not 25 <= len(text) <= 240:
            reasons.append("length_out_of_bounds")
        key = normalized(text)
        if key in seen:
            reasons.append("duplicate_normalized_text")
        seen.add(key)
        if not row.get("product_tension", "").strip():
            reasons.append("missing_product_tension")
        if not re.search(r"\b(earbuds?|audio|calls?|sound|wire|listen|voice)\b", text, re.I):
            reasons.append("missing_product_link")
        if any(re.search(pattern, text, re.I) for pattern in BANNED_CLAIM_PATTERNS):
            reasons.append("unsupported_claim")
        if any(name in text.casefold() for name in BANNED_NAMES):
            reasons.append("real_person")
        disposition = not reasons
        out = dict(row)
        out["passed_deterministic_filter"] = str(disposition).lower()
        out["filter_reason"] = ";".join(reasons)
        (accepted if disposition else rejected).append(out)
    write_csv(output / "premises.filtered.csv", accepted)
    write_csv(output / "premises.rejected.csv", rejected or [{"premise_id": "", "reason": "none"}])
    report = {
        "stage": "deterministic_filter",
        "input_count": len(source),
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "persona_counts": dict(Counter(row["persona"] for row in source)),
        "checks": [
            "valid persona",
            "length between 25 and 240 characters",
            "normalized text uniqueness",
            "non-empty product tension",
            "product/audio/call link",
            "unsupported claim pattern",
            "real-person name",
        ],
        "ordering": "filter precedes TypeSafe tournament",
    }
    write_json(output / "filter_report.json", report)
    print(f"Filter: {len(accepted)} accepted, {len(rejected)} rejected")


def build_questions(rows: list[dict[str, str]], brief: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    state: dict[str, Any] = {
        "brief": {
            "product": brief["product"],
            "category": brief["category"],
            "audience": brief["audience"],
            "promise": brief["promise"],
            "pain": brief["pain"],
            "brand_constraints": brief["brand_constraints"],
        }
    }
    questions: dict[str, Any] = {}
    for index, row in enumerate(rows):
        key = f"p{index}"
        state[key] = {
            "persona": row["persona_label"],
            "premise": row["text"],
            "product_tension": row["product_tension"],
        }
        questions[f"{key}_potential"] = {
            "type": "score",
            "instructions": f"Score the comedic premise potential of `{key}` for a paid-social audience.",
            "criteria": [
                "Flat or generic",
                "Weak premise with little escalation",
                "Recognizable but familiar",
                "Strong specific tension worth developing",
                "Exceptional pattern interrupt with clear escalation",
            ],
        }
        questions[f"{key}_fit"] = {
            "type": "noul",
            "instructions": f"Does `{key}` fit the product, audience, and brand constraints?",
            "criteria": {
                "true": "Could plausibly become this brand's ad",
                "false": "Wrong audience, decorative product, or constraint conflict",
            },
        }
        questions[f"{key}_clarity"] = {
            "type": "score",
            "instructions": f"How clear is `{key}` as a five-second vertical video premise?",
            "criteria": [
                "Impossible to stage",
                "Confusing or overloaded",
                "Understandable but crowded",
                "Clear visual situation",
                "Instantly legible and stageable",
            ],
        }
        questions[f"{key}_rationale"] = {
            "type": "choice",
            "instructions": f"Select the best rationale category for `{key}`.",
            "criteria": dict(RATIONALE_LABELS),
        }
    return state, questions


def run_tournament(output: Path, round_number: int, input_name: str, output_name: str, survivor_count: int) -> None:
    brief_path = output / "brief.json"
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    rows = load_csv(output / input_name)
    if round_number == 1:
        rows = [row for row in rows if row["passed_deterministic_filter"] == "true"]
    jobs = []
    for start in range(0, len(rows), 20):
        chunk = rows[start : start + 20]
        state, questions = build_questions(chunk, brief)
        jobs.append((state, questions))
    try:
        answers_list, usage = ask_batch(jobs, workers=3)
    except Exception as exc:
        status_path = output / "network-status.json"
        if status_path.is_file():
            status = json.loads(status_path.read_text(encoding="utf-8"))
        else:
            status = {}
        status.update(
            {
                "stage": f"round{round_number}_live_jev_tournament",
                "status": "unavailable",
                "attempts": int(status.get("attempts", 0)) + 1,
                "last_attempt_utc": datetime.now(timezone.utc).isoformat(),
                "error_type": type(exc).__name__,
                "error": str(exc),
                "endpoint": "https://api.typesafe.ai/v1/systemone",
                "live_scores_recorded": False,
                "input_tokens_recorded": 0,
                "output_tokens_recorded": 0,
                "mock_scores_used": False,
                "input_preserved": input_name,
                "next_safe_action": "Retry after DNS/network connectivity returns; do not substitute selftest answers for live Jev evidence.",
            }
        )
        write_json(status_path, status)
        print(
            f"ERROR: live Jev round {round_number} unavailable; recorded {status_path}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    scored: list[dict[str, Any]] = []
    for row_index, row in enumerate(rows):
        job_index = row_index // 20
        answers = answers_list[job_index]
        key = f"p{row_index % 20}"
        potential = float(answers[f"{key}_potential"]["score"])
        fit = float(answers[f"{key}_fit"]["noul"])
        clarity = float(answers[f"{key}_clarity"]["score"])
        rationale_code = answers[f"{key}_rationale"]["choice"]
        total = potential * 2 + fit * 5 + clarity
        scored.append(
            {
                **row,
                "round": str(round_number),
                "potential_score": f"{potential:.2f}",
                "brand_fit": f"{fit:.2f}",
                "clarity_score": f"{clarity:.2f}",
                "total_score": f"{total:.2f}",
                "rationale_code": rationale_code,
                "rationale": RATIONALE_LABELS[rationale_code],
                "selected": "",
            }
        )
    ranked = sorted(scored, key=lambda row: (-float(row["total_score"]), row["premise_id"]))
    selected_ids = {row["premise_id"] for row in ranked[:survivor_count]}
    for row in ranked:
        row["selected"] = str(row["premise_id"] in selected_ids).lower()
    write_csv(output / f"round{round_number}.scores.csv", ranked)
    survivors = [row for row in ranked if row["selected"] == "true"]
    write_csv(output / output_name, survivors)
    round_report = {
        "round": round_number,
        "model": "jev-latest",
        "input_count": len(rows),
        "survivor_count": len(survivors),
        "expected_survivor_count": survivor_count,
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "requests": len(jobs),
        "scores_path": f"round{round_number}.scores.csv",
        "survivors_path": output_name,
        "rationales": "rationale column in scores CSV",
        "formula": "potential*2 + brand_fit*5 + clarity",
    }
    write_json(output / f"round{round_number}.json", round_report)
    print(f"Round {round_number}: {len(rows)} -> {len(survivors)}; usage {usage}")


def mutate(output: Path) -> None:
    rows = load_csv(output / "round1.survivors.csv")
    mutations = {
        "absurdist": "The civic committee escalates the wire into a public transit heirloom.",
        "cynic": "The coach reveals the upgrade ritual was always about visibility, not sound.",
        "worrier": "The private thought becomes a courtroom exhibit nobody asked for.",
        "innocent": "The literal interpretation causes a completely unnecessary evacuation.",
        "status": "The rivalry expands into a silent lobby ranking system.",
        "antimarketing": "The ad crew quits and films the boring wire instead.",
    }
    output_rows: list[dict[str, Any]] = []
    for row in rows:
        mutation = mutations[row["persona"]]
        text = f"{row['text']} {mutation}"
        if len(text) > 320:
            text = f"{row['text'][:260].rsplit(' ', 1)[0]}... {mutation}"
        output_rows.append(
            {
                **row,
                "original_premise_id": row["premise_id"],
                "premise_id": f"{row['premise_id']}-M",
                "text": text,
                "mutated_from": row["premise_id"],
            }
        )
    write_csv(output / "round1.mutated.csv", output_rows)
    report = {
        "input_count": len(rows),
        "mutated_count": len(output_rows),
        "mutation_policy": "persona-specific escalation while preserving product tension",
    }
    write_json(output / "mutation_report.json", report)
    print(f"Mutated {len(output_rows)} survivors")


def prepare_boards(output: Path) -> None:
    rows = load_csv(output / "round2.finalists.csv")
    prompts = output / "boards" / "prompts"
    prompts.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        candidate_id = f"C{index:03d}"
        prompt = (
            f"Create a vertical 9:16 product-only visual comedy board inspired by this premise: {row['text']} "
            "Translate the comedic tension into one staged object scene using unbranded white wired earbuds, "
            "their cable, and everyday props. No people, no readable text, no captions, no logos, no UI, "
            "no brand name, no extra products, and no real-person likeness. Keep the earbuds and cable sharp, "
            "central, and immediately recognizable. Use clear social-feed lighting and a readable visual joke."
        )
        path = prompts / f"{candidate_id}.txt"
        path.write_text(prompt + "\n", encoding="utf-8")
        manifest.append(
            {
                "candidate_id": candidate_id,
                "premise_id": row["premise_id"],
                "persona": row["persona"],
                "prompt_path": str(path),
                "model": "gpt-image-2.5-sunburst",
                "quality": "1440p",
                "aspect_ratio": "9:16",
            }
        )
    write_json(output / "boards" / "manifest.json", {"boards": manifest})
    print(f"Prepared {len(manifest)} board prompts")


def make_report(output: Path) -> None:
    brief = json.loads((output / "brief.json").read_text(encoding="utf-8"))
    filter_report = json.loads((output / "filter_report.json").read_text(encoding="utf-8"))
    round1 = json.loads((output / "round1.json").read_text(encoding="utf-8"))
    round2 = json.loads((output / "round2.json").read_text(encoding="utf-8"))
    mutation_report = json.loads((output / "mutation_report.json").read_text(encoding="utf-8"))
    finalists = load_csv(output / "round2.finalists.csv")
    persona_counts = Counter(row["persona"] for row in load_csv(output / "premises.all.csv"))
    lines = [
        "# Comedy Test Sprint report",
        "",
        f"## Brief: {brief['product']}",
        "",
        f"Audience: {brief['audience']}.",
        "",
        "## Method",
        "",
        "1. Generated 120 premises from six independent comedic personas.",
        "2. Applied deterministic product, safety, uniqueness, and length filters.",
        "3. Ran the first Jev tournament to 24 survivors.",
        "4. Mutated all 24 survivors.",
        "5. Ran a second Jev tournament to eight finalists.",
        "6. Prepared free GPT Image 2.5 boards for all finalists.",
        "",
        "## Measured selection cost",
        "",
        f"- Round 1: {round1['input_tokens']} input / {round1['output_tokens']} output tokens",
        f"- Round 2: {round2['input_tokens']} input / {round2['output_tokens']} output tokens",
        f"- Total: {round1['input_tokens'] + round2['input_tokens']} input / {round1['output_tokens'] + round2['output_tokens']} output tokens",
        "",
        "## Persona coverage",
        "",
        "| Persona | Premises |",
        "|---|---:|",
    ]
    lines.extend(f"| {PERSONAS[key]['label']} | {count} |" for key, count in sorted(persona_counts.items()))
    lines.extend(
        [
            "",
            "## Deterministic filter",
            "",
            f"- Input: {filter_report['input_count']}",
            f"- Accepted: {filter_report['accepted_count']}",
            f"- Rejected: {filter_report['rejected_count']}",
            "- Ordering: filters ran before Jev scoring.",
            f"- Mutated survivors: {mutation_report['mutated_count']}/{mutation_report['input_count']}",
            "",
            "## Finalists",
            "",
            "| Rank | ID | Persona | Score | Rationale | Premise |",
            "|---:|---|---|---:|---|---|",
        ]
    )
    for index, row in enumerate(finalists, start=1):
        premise = row["text"].replace("|", "/")
        lines.append(
            f"| {index} | {row['premise_id']} | {row['persona_label']} | {row['total_score']} | {row['rationale']} | {premise} |"
        )
    lines.extend(
        [
            "",
            "## Production policy",
            "",
            "- Boards: free GPT Image 2.5 Sunburst, 1440p, 9:16.",
            "- Videos: V6 720p, five seconds, no audio, at most two renders.",
            "- Premium video models: excluded.",
            "",
            "## Limitations",
            "",
            "- This is a premise-selection test, not a live performance test.",
            "- No ROAS, conversion lift, or comedy-performance claim is made.",
            "- Humor quality requires human review before client delivery.",
            "- Visual boards and video QA are recorded separately.",
        ]
    )
    (output / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {output / 'REPORT.md'}")


def selftest() -> None:
    global ask_batch
    original_ask_batch = ask_batch

    def fake_ask_batch(jobs, workers=3):
        answers_list = []
        usage = {"input_tokens": 0, "output_tokens": 0}
        for state, questions in jobs:
            answers = {}
            for question_key, question in questions.items():
                index = int(question_key[1:].split("_", 1)[0])
                if question["type"] == "score":
                    answers[question_key] = {"score": 4.0 if index < 4 else 2.0}
                elif question["type"] == "noul":
                    answers[question_key] = {"noul": 1.0 if index < 4 else 0.7}
                else:
                    answers[question_key] = {
                        "choice": "specific_tension" if index < 4 else "weak_generic"
                    }
            answers_list.append(answers)
            usage["input_tokens"] += 1000
            usage["output_tokens"] += 100
        return answers_list, usage

    ask_batch = fake_ask_batch
    try:
        with tempfile.TemporaryDirectory(prefix="jevmax-comedy-selftest-") as temp:
            output = Path(temp) / "run"
            brief_path = Path(__file__).parent / "briefs" / "airpods-wired-2026-09-21.json"
            generate_premises(brief_path, output)
            apply_filters(output)
            run_tournament(output, 1, "premises.filtered.csv", "round1.survivors.csv", 24)
            mutate(output)
            run_tournament(output, 2, "round1.mutated.csv", "round2.finalists.csv", 8)
            prepare_boards(output)
            make_report(output)
            assert len(load_csv(output / "round1.survivors.csv")) == 24
            assert len(load_csv(output / "round1.mutated.csv")) == 24
            assert len(load_csv(output / "round2.finalists.csv")) == 8
            assert len(json.loads((output / "boards" / "manifest.json").read_text())["boards"]) == 8
            subprocess.run(
                [sys.executable, str(Path(__file__).with_name("validate_run.py")), str(output)],
                check=True,
            )
            board_manifest = json.loads((output / "boards" / "manifest.json").read_text(encoding="utf-8"))
            board_result = {
                "results": [
                    {
                        "id": f"board_{row['candidate_id']}",
                        "status": "success",
                        "task_id": f"fake-board-{index}",
                        "local_path": row["prompt_path"],
                        "cost_credits": 0,
                        "command": f"pixverse create image ... C{index:03d}.txt",
                    }
                    for index, row in enumerate(board_manifest["boards"], start=1)
                ]
            }
            board_result_path = output / "boards" / "queue-result.json"
            write_json(board_result_path, board_result)
            from studio.comedy.finalize_production import append_production_report, record_boards, record_qa, record_videos

            record_boards(output, board_result_path)
            subprocess.run(
                [sys.executable, str(Path(__file__).with_name("prepare_videos.py")), "--run", str(output), "--count", "2"],
                check=True,
            )
            plan = json.loads((output / "render" / "plan.json").read_text(encoding="utf-8"))
            render_result = {
                "results": [
                    {
                        "id": f"video_{row['candidate_id']}",
                        "status": "success",
                        "task_id": f"fake-video-{index}",
                        "local_path": row["prompt_path"],
                        "cost_credits": 40,
                        "command": "pixverse create video --model v6 --quality 720p --duration 5 --no-audio",
                    }
                    for index, row in enumerate(plan["videos"], start=1)
                ]
            }
            render_result_path = output / "render" / "queue-result.json"
            write_json(render_result_path, render_result)
            record_videos(output, render_result_path)
            qa_result = {
                "reports": [
                    {"generation_status": "success", "issues": [], "model": "v6", "report_path": str(path)}
                    for path in [row["prompt_path"] for row in plan["videos"]]
                ]
            }
            qa_result_path = output / "render" / "qa-report.json"
            write_json(qa_result_path, qa_result)
            record_qa(output, qa_result_path)
            append_production_report(output, human_review=True)
            subprocess.run(
                [sys.executable, str(Path(__file__).with_name("validate_run.py")), str(output), "--full"],
                check=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).with_name("build_pixverse_commands.py")),
                    "--run",
                    str(output),
                    "--stage",
                    "boards",
                    "--project",
                    "jevmax-comedy-selftest-boards",
                ],
                check=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).with_name("build_pixverse_commands.py")),
                    "--run",
                    str(output),
                    "--stage",
                    "videos",
                    "--project",
                    "jevmax-comedy-selftest-videos",
                ],
                check=True,
            )
            assert (output / "boards" / "queue-commands.sh").is_file()
            assert (output / "render" / "queue-commands.sh").is_file()
        print("comedy selftest OK")
    finally:
        ask_batch = original_ask_batch


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    generate = sub.add_parser("generate")
    generate.add_argument("--brief", type=Path, required=True)
    generate.add_argument("--output", type=Path, required=True)

    filter_parser = sub.add_parser("filter")
    filter_parser.add_argument("--output", type=Path, required=True)

    tournament = sub.add_parser("tournament")
    tournament.add_argument("--output", type=Path, required=True)
    tournament.add_argument("--round", type=int, choices=(1, 2), required=True)

    mutation = sub.add_parser("mutate")
    mutation.add_argument("--output", type=Path, required=True)

    boards = sub.add_parser("boards")
    boards.add_argument("--output", type=Path, required=True)

    report = sub.add_parser("report")
    report.add_argument("--output", type=Path, required=True)

    sub.add_parser("selftest")

    args = parser.parse_args()
    if args.cmd == "generate":
        args.output.mkdir(parents=True, exist_ok=True)
        write_json(args.output / "brief.json", json.loads(args.brief.read_text(encoding="utf-8")))
        generate_premises(args.brief, args.output)
    elif args.cmd == "filter":
        apply_filters(args.output)
    elif args.cmd == "tournament":
        if args.round == 1:
            run_tournament(args.output, 1, "premises.filtered.csv", "round1.survivors.csv", 24)
        else:
            run_tournament(args.output, 2, "round1.mutated.csv", "round2.finalists.csv", 8)
    elif args.cmd == "mutate":
        mutate(args.output)
    elif args.cmd == "boards":
        prepare_boards(args.output)
    elif args.cmd == "report":
        make_report(args.output)
    elif args.cmd == "selftest":
        selftest()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
