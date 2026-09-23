# DIAL M FOR MOON — decision log

## 2026-09-23 — Poster v1 APPROVED (human override)

- Rank gate (Jev): ADVANCE, total 7.85 (hook 2.58 / era 3.46 / engine 1.81) — beat THE NEEDLE'S EYE (7.35, engine 0.76) and PIVOT (2.28, killed).
- Cannon gate run 1 (my hypothetical poster description): KILLED — era_authentic 0.47 (mixed-era typography: Constructivist + Polish-school + Ektachrome).
- Fix applied: single coherent 1959 language — Saul Bass geometry, three-color litho palette, 1959 offset lithography.
- Poster v1 generated: gpt-image-2 via Kling, 2:3, 2k, high — 35 credits. Vision description: correct spelling, strict palette, cord-plugs-into-moon pun, uniform fresh aging.
- Cannon gate run 2 (vision-derived description of actual image): KILLED — era_authentic 0.33 (reads as modern homage, not period artifact), buy 0.67, unique 0.86.
- **Decision: user APPROVED poster v1 as canon key art, overriding the gate's era criterion.** Rationale (implicit): buy/unique both pass; homage-vs-artifact strictness is a stylistic call the human owns. Poster: `poster-v1.png`. Gate output: `../jevmax/dial_m_poster_verdict.json`.
- Next stage triggered: character bible (sgflix-create-character-bible), 8 pages, lead character Valentina Orlova.

## 2026-09-23 — Character bible COMPLETE (Valentina Orlova)

- 8/8 pages generated (gpt-image-2 via Kling image_to_image, page 1 anchor → pages 2-8 referenced to it). 315 credits total (incl. one anchor retry).
- QC: all 8 MD5 hashes unique (no duplicate cascade). Page 2 turnaround: same woman across front/side/back, bun + olive ribbon visible from behind, rank stripe + sky-blue piping pass. Page 8 motion sheet: same identity across poses, correct Cyrillic color-chip labels, coherent set signage, no anatomy/modern errors.
- Lock amendment: left-eyebrow scar demoted to SCRIPT-ONLY canon after two failed render attempts (see identity_lock.yaml comment). Hair ribbon is soft-visible: describe, don't QC-fail on lighting.
- Files: `bibles/valentina-orlova/{identity_lock.yaml, all_8_prompts.md, images/page_01..08.png}` (+ `_page_01_attempt1_scarless.png` kept for record).
- Session spend to date: 386 credits (62 lighthouse demo + 35 poster + 315 bible), balance 5,672.
- Next stage options: Kling Element upload (pages 1, 2, 4, 5 as image subject) for video generation; supporting-character bibles; script development via sw-workflow / short-drama-write.

## 2026-09-23 — Element created + SHOT 01 animated (user: "approve")

- Kling Element `322149783311120` "Valya Orlova" — cover: page 1 anchor; secondary: pages 2 (turnaround), 4 (expressions), 5 (details). Tag: Characters. Note: Element cover is immutable per Kling — replacing the anchor later means delete + recreate.
- SHOT 01 "switchboard mayday": kling-video-v3_0, first_image = page 1, elements = [322149783311120], 5s, 1080p, native audio, single shot. 60 credits. Beat: calm focus → plug insert → crackle → sharp lean-in; push-in + handheld drift, Ektachrome look. File: `shot_01_switchboard_mayday.mp4` (9.6 MB).
- Session spend: 446 credits, balance 5,612.
