# Jev in the writing stage — placement doctrine

Companion to `drama_gate.py`. Rule: **Jev never writes.** It ranks candidates,
verifies claims against canon, and routes uncertainty to the human. The writer
model (with the sw-* / short-drama skills) generates; the user owns canon.
Source: the typesafe-ai skill + TypeSafe docs (hierarchical classification,
citation check, use-case map) + measured runs on this repo (see
`dial_m_poster_verdict.json`, `ranked_concepts.csv`).

## Where the gates go (writing arrows)

| Arrow | Judgment | Hardened? |
|---|---|---|
| Logline → concept pick | Score hook/era/engine per concept | `drama_gate.py rank` |
| Concept → poster spend | Noul Buy/Era/Uniqueness on poster description | `drama_gate.py cannon` |
| Beats → episode map | Score hook/cliffhanger/producibility per episode; ADVANCE top N to the shot budget | `drama_gate.py episodes` |
| Arc branch points | Beam-search Choice over branch tree (keep K=3, geometric-mean path score); near-tie top-two = human taste call | ad hoc (pijev — Choice ordering matters) |
| Scene → script | Noul per scene: does it turn (value A → B)? enter late / leave early? | ad hoc |
| Script → dialogue QC | Semantic lint: on-the-nose detection, exposition-as-information, one-voice | ad hoc |
| Draft → canon | Citation-check transplant: deterministic mention pass (free), then one Choice per entity vs the bible — consistent / contradicts / bible_silent; ≥0.80 auto-accepts, the rest go to the human | `drama_gate.py canon` |
| Character action | Would this character do X given the identity lock? Noul, lock as state | ad hoc |
| Notes → revision | Rank findings now / soon / note (audit.py pattern) | ad hoc |

## Kept OUT of Jev

- Prose quality, thematic intent, "is it good" — non-operationalizable. Score
  levels must describe concrete situations; translating vibes into levels is
  the writer's job.
- Canon decisions on REVIEW verdicts — the escalation path belongs to the human
  (proven: poster v1 shipped via user override of a gate KILLED).

## Mechanics learned on this stack

- Per-item **Score** questions are order-invariant by construction — no pijev
  needed. **Choice** questions over sibling candidates get pijev.
- Score answers return on a 0–5 scale per question; Noul is 0–1. Bands:
  ≥0.75 / ≥0.50 / below for Noul gates (GREENLIT / CONDITIONAL / KILLED).
- Batch all independent questions over the same state in one request
  (~12x cheaper and faster than serial).
- Cost of a full gate pass: 1–2k tokens, fractions of a cent. The things it
  guards: 35 cr per image render, 60 cr per 5s shot, 280–315 cr per bible.
