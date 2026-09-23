# EP001 — Take gates (2026-09-23)

Method: 2 frames/take (25%, 75%) vision-described against the shot record's
beat + gate criterion, then Jev-selected via TypeSafe (`jev_gate.py` method:
narrow judgments, rotated criteria order ×4, none_of_these option, weights in
code — beat 0.6 / period look 0.4). API note: `api.typesafe.ai` was dropping
multi-question requests today, so gates ran one question per call with
retry-on-disconnect (see parent report for the workaround script).

| Shot | Winner | Score | Rationale |
|------|--------|-------|-----------|
| S01 | take2 | 0.800 | Stronger calm→alarm arc: frontal close-up alarm + window/dish world detail. |
| S02 | take1 | 0.863 | Needle settles at red 14, КАНАЛ 14 lamp bloom legible; take2 had "KODAK 1959" prompt-leak text on the housing and vaguer channel numbers. |
| S03 | take1 | 0.741 | Hand hovering over the red cut-key holds the focal-shift beat; take2 played alarm instead of listening. (look dim soft: none_of_these 0.43) |
| S04 | take1 | 0.776 | Placard reads «СЕКЦИЯ 7 — НЕЗАРЕГИСТРИРОВАННЫЙ ПЕРЕХВАТ = ИЗМЕНА» correctly; take2 printed the opposite word (РЕГИСТРИРОВАННЫЙ). |
| S05 | take1 | 0.969 | Entry «14.09.59 / 14 / не опознано» legible in period Cyrillic hand; take2's writing was generic scribble. |
| S06 | take1 | 0.979 | Korabelnikov fills the doorway backlit, never enters; take2 had him inside offering cigarettes (wrong beat). |
| S07 | take1 | 0.613* | His face sharp over her shoulder, hand extended to the book; take2 repeated the cigarette-offer beat. *Soft win — Jev lukewarm (none_of_these 0.27). |
| S08 | take1 | 0.991 | Smeared ink smudge reads erased-not-torn; wedding band on right hand per lock. |
| S09 | take2 | 0.514* | Marginally stronger zero-play stillness. *REVIEW — coin-flip vs take1 (0.419), stable across 8 rotations; either take defensible, both kept. |
| S10 | take3 | 0.765 | Centered Valya, lamps ringing, red pencil raised as the only proof, clean cut to black. |

## 9:16 crops (winner.mp4 per shot, originals kept)

- S02, S04: already 720×1280 — stream-copied.
- S01, S03, S06, S07, S08, S09, S10: 832×1104 → center crop 621×1104.
- S05: landscape 1104×832 → 468×832 window right-shifted (x=420) to keep the
  log entry («не опознано») and the writing hand; a true center crop would
  have cut the payoff word. Her face at frame edge is sacrificed — noted,
  beat ("she logs it") survives via hand + entry.

All winners: native pipeline, 0 Kling/PixVerse. 1959 Ektachrome look holds
across the set; prompt-leak text ("KODAK…") appears on equipment in losing
takes only.
