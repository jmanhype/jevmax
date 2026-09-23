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

## 2026-09-23 — WRITING SPRINT COMPLETE (user: "write it")

- Format: **vertical short-drama series** (12 × ~110s, 9:16) recommended and written to; 16:9 short-film fallback documented in story-bible.md (reversible at storyboard). Rationale: engine score 1.81 = premise's series virtue; stack-native; Cannon Buy criterion = vertical audience.
- `story-bible.md` (sw-workflow state file): premise, controlling idea, the lie of the world, cast (Valya / Korabelnikov / Riva / SEVEN-THREE), 12-episode arc, both format analyses, production checklist, resume protocol.
- `episode-map.csv` gated (6,050 in / 562 out tokens): eps 1-9 ADVANCE (pilot 10.21, ep 6 father-tape 10.18; cliffhanger tier 3.1-3.8 throughout). HOLDs 7/10/8 structural (8.16-8.78, near-miss); ep 12 finale hook 1.02 = measurement artifact (finales open quiet; its job is payoff) — human note, not a defect.
- `episodes/EP001/script.md` written (short-drama-write format; opening beat = canon shot 01).
- Canon gates on real script: vs identity lock 4/4 PASS (0.94-0.99); vs story bible first run flagged "Section 7: bible_silent" → REVIEW (correct: script invented a world-fact) → Section 7 canonized into story-bible.md → re-gate 5/5 PASS (0.96-1.00). Total ~9.4k tokens for all sprint gates.
- Next: Korabelnikov 4-page bible (supporting tier), storyboard + prompts for EP001 (eps 2-12 after), then batch animation.

## 2026-09-23 — GRAMMAR LAYER INSTALLED: Eyecandy + platform adoptions

- Reviewed the closed-platform landscape (Dramagic/BytePlus, Slate/xAI). Adopted into the open stack: Dramagic's structured shot table + matched assets; Slate's director's brief + takes (generate N, gate, keep best). Not adopted: their platforms.
- **Eyecandy (eyecannndy.com) is now the grammar layer** (jevmax layer 3): full live catalog fetched 2026-09-23 — 136 techniques — as `jevmax/creative/eyecandy-catalog.md` (site had 138 on the author's 09-20 fetch; 2 since reorganized). Existing `creative/eyecandy-source-grammar.md` (Ava mappings) restored to the working copy from the GitHub clone.
- New `jevmax/creative/shot-record-template.md`: per-shot record = ONE dominant Eyecandy technique mapped to camera/motion/world/grade, non-empty `withheld` list (anti-overpacking), matched assets, audio beats, takes ≥2 with vision→Jev selection, verbatim prompt appended after render. Episode header = director's brief. Rules: no technique, no shot; no two dominants; episodes must have ADVANCE'd before shot budgets.
- DIAL M registers pre-mapped in the catalog: series grade = Vintage/Halation/Vignette; switchboard grammar candidates = Central Framing, Cut-ins, Over the Shoulder, Split Diopter, Focal shift, Locked-On, Voyeur, Typography.
- First application: EP001 storyboard (next stage) will be built as shot records per this template.

## 2026-09-23 — EP001 STORYBOARD + KORABELNIKOV BIBLE (user: "go")

- `episodes/EP001/storyboard.md`: 10 shot records per template — director's brief header (110s, 9:16, grade lock, cast Elements, grammar budget 5) + shots S01-S10 with one dominant Eyecandy technique each (Central Framing ×2, Cut-ins ×4, Focal shift ×2, Over the Shoulder, Split Diopter), non-empty withheld lists, matched assets, audio beats, takes=2 + gates. Note: shot 01 (16:9) = S01 proof master; vertical re-render queued.
- Korabelnikov 4-page supporting bible complete (140 cr): `bibles/korabelnikov/` — anchor QC full pass (single-star boards, cornflower piping, glasses-on-chain, folder; set Cyrillic «ЦЕНТРАЛЬНЫЙ ПУНКТ СВЯЗИ» correctly spelled); 4/4 unique MD5s; generated from Valya's page 1 as world-consistency reference, no face-bleed.
- Kling Element **322152680652417** "Major Korabelnikov" (cover anchor; secondary 02/04/07).
- Episode cast is now fully Element-anchored. **Render budget for EP001 (awaiting go): 10 shots × 2 takes × 60 cr = 1,200 credits.**

## 2026-09-23 — PREVIZ LAYER ADOPTED: Shot Composer + platform routing

- **Shot Composer** (github.com/Anujatk1999/open-media, MIT) installed at `C:\Users\ged\AppData\Local\Programs\open-media`, dev server localhost:5173, MCP `shot-composer` registered in ZCode config (stdio, absolute node path; tools live in new sessions; needs browser tab bridged over ws://39217). Free, local, no account.
- Pipeline v1.1: `previz` field added to shot-record template — REQUIRED for complex blocking (S06/S07/S09/S10), explicit skip for simple inserts; captured PNG doubles as generation reference frame. Free gate before 40–60 cr takes.
- **Platform routing rule** (template rule 7): PixVerse v6 for inserts + atmosphere drafts (gpt-image-2.5 seeds free on Pro, 40–50 cr/take, `--seed`/`--idempotency-key`/`--off-peak`); Kling 3.0 for dialogue/audio-critical finals (Elements, prompted sound design). Record actual credit delta per render — Kling quoted costs drift (observed 2× on image batch 2026-09-23).
- Wallets: PixVerse 7,145 (re-authorized this machine; single-session tokens — the other machine's PixVerse auth is now dead, it must re-login if it renders), Kling 5,332.
