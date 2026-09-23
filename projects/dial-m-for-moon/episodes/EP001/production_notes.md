# EP001 — Production & Mix Record

**Title:** The Voice on 14 Megacycles · **Date:** 2026-09-23 · **Pipeline:** native/in-house (no Kling/PixVerse)

## Picture
- Locked picture: `assembly/EP001_video_1055.mp4`
  - 105.5 seconds, 720×1280 vertical, H.264 yuv420p, 24fps
  - 6s title card, S01–S10 winners in order, act-break black holds, end hold/card
  - Winners: S01 t2 (0.80), S02 t1 (0.86), S03 t1 (0.74), S04 t1 (0.78), S05 t1 (0.97),
    S06 t1 (0.98), S07 t1 (0.61 soft win), S08 t1 (0.99), S09 t2 (0.51 coin flip), S10 t3 (0.77)
  - QC: S09 near coin flip (take1 kept as swap); S05 468×832 crop right-shifted to preserve
    «не опознано»; S07 weak on period look but usable

## Sound
- Build script: `audio/build_audio.py` (105.5s timeline, graceful skip on missing dialogue)
- Mix: `audio/EP001_audio_mix.wav` — mono, 48kHz, 16-bit, peak-normalized (peak pre-norm 0.511)
- Dialogue present: SEVEN-THREE S01 English («Seven-three.») → `seven_three_s01_radio.wav`
- Sound bed (in-house synthesized): room tone, hum, switchboard hiss, plug click,
  rising crackle, breath, pencil knock/scratch, corridor bed, hinge, boots, floor creak,
  paper, stove tick, latch, two static knocks

## Final
- `assembly/EP001_final_v1.mp4` — 105.5s, 720×1280, H.264 + AAC 192k, built 2026-09-23
- Screening: `review.html` (final cut is the primary player)

## ⚠ Pending: Russian dialogue patch (v2)
Four lines blocked 2026-09-23 — the TTS backend deterministically rejects the exact
line text (returns truncated/empty audio), confirmed across voices:
1. `seven_three_s03.mp3` — «Скажи им. Я ещё здесь.» (avocado_v2:vincent)
2. `korabelnikov_s07.mp3` — «Ночной журнал, старшина.» (avocado_v2:magnus)
3. `valya_s07.mp3` — «Обычный лунный шум, товарищ майор.» (avocado_v2:myrtle)
4. `korabelnikov_s09.mp3` — «Интересная ночь, старшина.» (avocado_v2:magnus)

Word probes showed the failures are tied to specific words (ещё, Ночной, Интересная,
Обычный, лунный) — other Russian words render fine, so it's a backend/text issue,
not the voices. Do NOT rewrite the lines without Jay's approval; options offered:
finish now + patch later (chosen), approve replacement lines, or keep retrying.

**Patch procedure (v2):** once WAVs exist, convert s03 MP3 → `_radio.wav`, rebuild
`audio/EP001_audio_mix.wav` via build_audio.py, mux as `EP001_final_v2.mp4`, update
review.html + this record.
