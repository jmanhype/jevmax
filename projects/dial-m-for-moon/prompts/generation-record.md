# DIAL M FOR MOON — generation prompt record

Exact prompts used for every rendered asset, so any machine can reproduce or
continue from the repo alone. (Model routing: Kling MCP `text_to_image` /
`image_to_image` / `image_to_video`.)

## poster-v1.png — gpt-image-2, 2:3, 2k, high (35 cr)

> Cinematic movie poster for "DIAL M FOR MOON", a 1959 Cold War thriller. Late-1950s Saul Bass-influenced minimal geometric design: a single black telephone plug cord spirals upward and becomes the trajectory line to a bold crescent moon shape, all set on a two-tone field of deep charcoal and signal orange. Title "DIAL M FOR MOON" large in period condensed grotesque sans-serif capitals, tagline "ONE FREQUENCY. TWO EMPIRES. NO SIGN-OFF." in small letterspaced caps beneath. PERIOD STOCK: 1959 one-sheet, 35mm Eastmancolor-derived offset lithography print, muted period ink palette, slight ink misregistration at edges. AGING: fresh print. Clean negative space across bottom 15 percent for a billing block. No modern typography, no gloss, no lens flares, no gibberish text.

## Character bible — gpt-image-2 (image_to_image canonical name `gpt-image2`), 2k, high, 35 cr/page

Prompts: `bibles/valentina-orlova/all_8_prompts.md` (all 8 pages + common lock).
Page 1 anchor generated text-to-image (2 attempts; attempt 2 is canon — sky-blue
piping fixed, scar abandoned), pages 2-8 generated with page 1 as `image_1`
reference. QC: unique MD5s; identity verified on pages 2/4/8.

## Kling Element — id 322149783311120 "Valya Orlova" (free)

Cover: bible page 1 (attempt 2). Secondary: pages 2 (turnaround), 4 (expressions),
5 (details). Tag: Characters. Cover immutable — replacing the anchor means
delete + recreate.

## shot_01_switchboard_mayday.mp4 — kling-video-v3_0, 5s, 1080p, audio, single shot (60 cr)

- first_image: bible page 1
- elements: [{"id":"322149783311120","bindName":"Valya"}]
- prompt:

> <<<id>>> sits at her night switchboard in the secret lunar listening post, 1959. She inserts a black plug with one precise motion, rows of small signal-orange lamps glowing under her face. Her expression shifts from calm professional focus to sudden stillness as a faint crackle breaks through her headset — she leans in sharply toward the board. Slow cinematic push-in from behind the switchboard toward her face, gentle handheld drift. Period sound: heavy switchboard clicks, low room hum, static crackle rising, her sharp intake of breath. 16mm Ektachrome reversal film look, slight halation on the practical lamps, organic grain.

## Not yet generated (awaiting writing sprint)

Script, storyboard, per-shot image/video prompts — the short-drama / sw-workflow
stage. Nothing to record until written; format call (vertical 9:16 series vs
16:9 short film) still open with the user.
