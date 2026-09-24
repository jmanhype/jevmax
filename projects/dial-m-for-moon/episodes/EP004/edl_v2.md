# EP004 v2 — Edit Decision List

**Assembly:** `assembly/EP004_assembly_v2.mp4`
**Format:** 720×1280, 30fps, H.264 + AAC, 103.5s (~31.4 MB)
**Grammar:** hard cuts between shots; SEQ A / SEQ B are match-on-action by
construction (last-frame→first-frame chains, cut exactly at chain points).
**Captions:** burned in, DejaVu Serif 44pt, bottom third (y = 0.80h), white
with soft shadow, no box. Two captions only.
**Sound:** synthesized (adapted from `assembly/build_audio.sh` →
`assembly/build_audio_v2.sh`). Tape-hiss bed carries across picture cuts
(the "steam").

## Picture table

| # | Shot | Source | Window | Dur | Absolute |
|---|------|--------|--------|-----|----------|
| 1 | CO | assembly/EP004_video_only.mp4 | 0.0–2.0 | 2.0 | 0.0–2.0 |
| 2 | Title | assembly/title.mp4 | full | 3.5 | 2.0–5.5 |
| 3 | A1 wide pan (desk) | shots/v2_SEQA/media-generation-seqa-a1-wide-pan-0-2533ede0-ae5d-4e5f-87f4-7b254e2a58d9.mp4 | 0.0–8.0 | 8.0 | 5.5–13.5 |
| 4 | A2 OTS (chained) | shots/v2_SEQA/media-generation-seqa-a2-ots-nocap-0-4ec1f711-44ef-428e-8519-282cdaf4dabe.mp4 | 0.0–5.0 | 5.0 | 13.5–18.5 |
| 5 | A3 pencil-stop ECU | shots/v2_SEQA/media-generation-seqa-a3-pencil-stop-0-e5a3a27b-0139-46f9-8d63-6bfcc815792d.mp4 | **2.5–5.5** | 3.0 | 18.5–21.5 |
| 6 | A4 file pan | shots/v2_SEQA/media-generation-seqa-a4-file-pan-r2-0-a98051de-0010-4fad-b60a-dae3dd763b52.mp4 | 0.0–6.0 | 6.0 | 21.5–27.5 |
| 7 | B1 archive wide (reach lands late) | shots/v2_SEQB/B1_winner.mp4 | **5.0–10.0** | 5.0 | 27.5–32.5 |
| 8 | B2 30° over (chained) | shots/v2_SEQB/B2_winner.mp4 | 0.0–4.0 | 4.0 | 32.5–36.5 |
| 9 | B3 reel insert (chained) | shots/v2_SEQB/B3_winner.mp4 | 0.0–3.0 | 3.0 | 36.5–39.5 |
| 10 | S05R drift | shots/v2_S05R/media-generation-ep004-s05r-drift-r1-0-f03f28e3-b2bc-4032-abe2-0391029744f4.mp4 | **1.0–9.0** | 8.0 | 39.5–47.5 |
| 11 | S06 (v1 keep) | assembly/EP004_video_only.mp4 | 45.5–55.5 | 10.0 | 47.5–57.5 |
| 12 | S07R push-in | shots/v2_S07R/media-generation-ep004-s07r-push-r1-0-b504330d-2a45-4f3f-9aaa-24937fe18c1e.mp4 | 0.0–8.0 | 8.0 | 57.5–65.5 |
| 13 | S08 (v1 keep) | assembly/EP004_video_only.mp4 | 65.5–75.5 | 10.0 | 65.5–75.5 |
| 14 | C2 empty crate | shots/v2_SEQC/media-generation-seqc-c2-anim-r3-0-b571cb71-c42d-42e5-a492-afd599509500.mp4 | **1.0–9.0** | 8.0 | 75.5–83.5 |
| 15 | S10R arc | shots/v2_S10R/media-generation-ep004-s10r-arc-r2-0-425d24b4-c314-4a60-83ae-601c04958805.mp4 | 0.0–6.0 | 6.0 | 83.5–89.5 |
| 16 | INS-S10b earcup ECU | shots/v2_S10R/media-generation-ep004-ins-s10b-r2-0-3fbfcef9-93cf-404b-a574-6948696de061.mp4 | 0.0–4.0 | 4.0 | 89.5–93.5 |
| 17 | S11 (v1 keep) | assembly/EP004_video_only.mp4 | 95.5–105.5 | 10.0 | 93.5–103.5 |

Total: 2+3.5+8+5+3+6+5+4+3+8+10+8+10+8+6+4+10 = **103.5s**

## Trim rationale (bolded windows above)

- **A3 (2.5–5.5):** the winner clip's first ~2.5s include the chained settle
  from A2's tail frame; the locked ECU of the pencil stopping dead lives in
  2.5–5.5. Only that window is used.
- **B1 (5–10):** the reach lands late in the generated clip; the first 5s are
  the walk-in. The last 5s (reach → door glance) are the match-action window
  B2 continues from.
- **S05R (1–9):** skip the first second (generation settle), keep the clean
  drift; end 1s early to avoid any tail-frame motion decay.
- **C2 (1–9):** same reasoning — skip generation settle at head, drop the
  last second so the hover/tremble resolves without model drift.

## Caption spotting (absolute timecodes)

| Caption | In | Out | Over |
|---------|----|-----|------|
| "He never flew." | 25.5 | 27.5 | A4 (finger on the redaction bar) |
| "Gone." | 79.5 | 82.5 | C2 (empty depression found) |

Nothing else is captioned. No generated-captions look.

## Sound spotting (absolute timecodes)

| Element | Time | Notes |
|---------|------|-------|
| Tape-hiss bed | 0–103.5 | pink noise, lowpass 3k, vol 0.05 |
| Bed ducked near-zero | 2.0–5.5 | under title |
| Spark burst + low thump | **1.3** | CO payoff (verified: 0 dB peak 1.0–1.8s) |
| Pencil scratch (tremolo) | 5.5–21.0 | bandpassed noise; **hard stop at 21.0** with A3 picture |
| Bed silence | 83.5–93.5 | warm-headset beat (S10R + INS-S10b) |
| Bed dip to 20% | 79.5–81.5 | empty depression found in C2 |
| Bed faint return (40%) | 93.5–103.5 | under S11 |
| S08 crack + thump + ring | **66.5** | verified: 0 dB peak 66.3–67.1s |

## Build notes

- Every source scaled to fill 720×1280 + center crop (704×1248 winners upscale
  cleanly), conformed to 30fps via `fps=30`, `setsar=1`. Single-pass ffmpeg
  concat of 17 trims; captions burned in the same pass.
- Audio: `assembly/build_audio_v2.sh` → `assembly/temp_audio_v2.wav` (103.5s),
  muxed with `-c:v copy`, AAC 128k, faststart. Intermediates kept:
  `EP004_assembly_v2_video.mp4` (picture only), `temp_audio_v2.wav`.
- Verification: duration 103.500s; burst peak 0 dB @1.0–1.8s vs −28 dB
  pre-burst; crack peak 0 dB @66.3–67.1s; silence zone 89–90s at −91 dB;
  pencil present at 20.5–20.9s (−23 dB), gone at 21.2–21.6s (−31 dB, bed
  only); title duck −56 dB; C2 dip −44 dB. Caption frames eyeballed at
  t=26 and t=80.5.
