# EP004 v2 — full re-block in continuous-action grammar

Authorized by Jay 2026-09-24: new renders, OTS/POV/B-cam, EDL, last-frame→
first-frame continuation allowed. Native pipeline only (`media.generate_video`).
Supersedes `reshoot_shot_list_v2.md` (its R-S05/R-S07/R-S10/INS specs are
folded in below unchanged).

Reference grammar (bathhouse video): one continuous action per sequence, camera
does the work (slow pan/push), inserts punctuate, micro-performance, key light
locked from frame left, tape hiss as the bridge (our "steam").

Standing locks: one visible character (Valya only); lamp-left rule; red pencil
over right ear; Bakelite headset; sky-blue piping; ash-blonde low bun;
no generated captions/text; photo+physics realism; 9:16 vertical (match v1
704×1248 masters); hard cuts between sequences, match-on-action within.

Chaining method: extract last frame of clip N (ffmpeg), pass as `kind:image`
input to clip N+1 with "same action continues" — never a text description of
a planned frame. `resume_from_snapshot_id` chains the same context across turns.

## SEQ A — DESK (one desk, one lamp, one continuous action) ~20s
Replaces S02+S03. Same desk, same brass lamp left — the lamp jump is gone by
construction. Action: writing the log → the writing stops → the file is already
there under her other hand.

- A1 WIDE PAN: slow pan right across the desk. Ledger open, her right hand
  writing with the red pencil. Start image: new wide desk keyframe (ledger +
  file both on desk, brass lamp left). 10s.
- A2 OTS: same writing action continues, camera settles over her shoulder.
  Chained from A1 tail frame. 6s.
- A3 INSERT (pencil stops): ECU, pencil halts mid-stroke dead. Chained from
  A2 tail (or standalone if chain breaks). 4s. Sound: scratch stops dead.
- A4 FILE PAN: camera pans left to the flight file already on the desk; her
  left index finger rests on the black redaction bar. Same lamp, same desk.
  Chained from A3 tail. 8s. Caption (burned in edit, not generated): "He never flew."

## SEQ B — ARCHIVE (the pull, match-on-action) ~14s
Replaces S04. Action: the reach for the blank reel, covered in 3 angles.

- B1 WIDE: lateral camera follow as she crosses to the shelf, hand reaching
  for the blank reel. Start image: v1 S04 keyframe
  (`shots/S04/media-generation-ep004-s04-v2-the-choice-0-5ba48878-306c-4b77-ac7a-cb89bb5fc1c5.webp`). 6s.
- B2 30° OVER: same reach, same arm extension, same reel — cut mid-motion.
  Chained from B1 tail frame. 5s.
- B3 INSERT: reel in her hand, label visible; her eyes cut to the door.
  Chained from B2 tail. 4s. No caption (the reach is the decision).

## S05R — MIXER (lateral drift) 10s
Spec unchanged from reshoot_shot_list_v2.md (R-S05). Start image: v1 S05
keyframe (`shots/S05/media-generation-ep004-s05-v4-no-badge-0-98eb7476-bcea-4522-a0eb-ffd4bdf11b19-clean.webp`).

## SEQ C — CRATE RHYME (same setup, reel present vs. absent)
C1 = v1 S06 (keep): OTS, hands part the folded headbands, lower the labeled
reel, smooth the bands over it. 10s.
C2 = NEW S09: the *same* OTS setup, same crate, same blanket-parting motion,
same hand speed — POV down reveals the empty depression where the reel was.
NOT literally chained (time gap); matched by setup instead. Hard cut in,
unconditioned, hiss bridge. Her hands grip the crate edges; shoulders drop.
Caption (edit): "Gone." 10s. Start image: generate matching OTS crate keyframe
with NO reel (empty depression visible).

## S07R — THE PAUSE (slow push-in) 10s
Spec unchanged (R-S07). Start image: v1 S07 keyframe
(`shots/S07/media-generation-ep004-s07-v1-stillness-0-8ccb708a-ea91-4f1e-b5d8-4c1d16601e1f.webp`).

## S08 — SPARK-OUT (keep v1) + CO (keep v1)

## S10R — WARM HEADSET (arc to earcup) 10s + INS-S10b (earcup ECU) 4s
Specs unchanged. Start image: v1 S10 keyframe
(`shots/S10/media-generation-ep004-s09-v1-warm-headset-0-c4601c8a-8884-4aad-acb4-797d9aec5206.webp`).

## S11 — FINAL LOOK (keep v1)

## v2 assembly map (picture)
CO 2s → title 3.5s → SEQ A ~20s → SEQ B ~14s → S05R 10s → C1 10s → S07R 10s →
S08 10s → C2 10s → S10R 10s (+INS-S10b 4s inside) → S11 10s ≈ 103s.
Sound design carries over from v1 (hiss bed, pencil stop, spark bang, S10
silence, S11 tone return), re-spotted to new cut points in the v2 EDL.

## QC gates per clip (before assembly)
1. `qc_continuity.py` pass or human-reviewed flag (same bar as v1).
2. Identity: same face as v1 S02 winner (spot-check 3 frames).
3. Lamp-left: key light from frame left, warm brass — reject green/cool jumps.
4. Hands: no morph/clip-through on contact frames; pencil stays red and placed.
5. Chain check: first frame of clip N+1 must continue clip N's tail action
   (same hand position ±small motion delta), not restart it.
