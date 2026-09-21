# Category Signal Sprint — Internal Dogfood Deliverable

## Executive summary

This package combines the current AirPods-category signal, live account audit,
Lost Future/Eyecandy concept gate, and the existing V6-only creative batch into
one client-facing deliverable. No new generation credits were spent while
assembling this report.

## Category signal

- Unique ads in current bounded sample: **50**
- Tagged ads: **21**
- Top advertisers: VOLTA Charger (5), Kure for Hypnotherapy (4), J7506v-en.myshopify.com (3), Heddz.co (3), Jay Saint (2)
- Hook mix: direct_offer 14, curiosity_claim 5, (untagged) 2
- Offer mix: other_product 19, (untagged) 2

This is a bounded sample, not a whole-library census.

## Account readiness

Account **Jay Guthrie** (49852068) is
ACTIVE.

Campaigns:

- [Airpod Pros] Marketplace listing boosted on 07/26/2022: PAUSED
- Airpods Leads Campaign: PAUSED

Pixel status:

- Jay Guthrie's Pixel: never fired

Page status:

- Jay Guthrie Airpods: lead-gen ToS not accepted

## Creative system

Top concepts from the Jev gate:

- **SPONSORED MINUTE** — One minute of quiet, courtesy of tomorrow.  
  Style: 1986–1992 Local Sponsor Bumper  
  Eyecandy technique: Central Framing  
  Gate score: 6.34
- **SOUND CHOICE** — The clearest thing on this beach is not the water.  
  Style: 1994–1998 Regional Retail VHS Accessory Demo Tape  
  Eyecandy technique: Camera Roll  
  Gate score: 5.87
- **CLEAR CALLS** — Your forecast: clear calls, scattered noise.  
  Style: 1990–1998 Local Broadcast Forecast Scanline  
  Eyecandy technique: Floating UI  
  Gate score: 5.22
- **TRY BEFORE 2000** — The future called. It sounds amazing.  
  Style: 1993–1998 CD-ROM Kiosk Product Tour  
  Eyecandy technique: Screen in Screen  
  Gate score: 4.77

## V6 asset manifest

The following V6-only variants are already on disk:

- `V002-E01` — 9:16, 5s, video: `creative/pixverse/V002-E01.mp4`
- `V002-E02` — 9:16, 5s, video: `creative/pixverse/V002-E02.mp4`
- `V002-E03` — 9:16, 5s, video: `creative/pixverse/V002-E03.mp4`
- `V002-E04` — 9:16, 5s, video: `creative/pixverse/V002-E04.mp4`
- `V002-E05` — 9:16, 5s, video: `creative/pixverse/V002-E05.mp4`
- `V002-E06` — 9:16, 5s, video: `creative/pixverse/V002-E06.mp4`
- `V002-E07` — 9:16, 5s, video: `creative/pixverse/V002-E07.mp4`
- `V002-E08` — 9:16, 5s, video: `creative/pixverse/V002-E08.mp4`

## Decision

The current package is strong enough to show a client, but two account issues
should be fixed before paid launch:

1. Install and fire the pixel.
2. Accept lead-gen ToS if lead campaigns are in scope.

## Next actions

1. Refresh the category sample next Monday.
2. Keep the current 8-variant V6 batch as the dogfood creative set.
3. Use the winning Lost Future concept as the next paid-test candidate.
4. Re-run the account audit after pixel and ToS fixes.

## Cost note

Assembling this deliverable used existing artifacts only. The historical V6
batch cost is already recorded in the render log. Future V6-only production
should use the currently measured 40-credit/no-audio route rather than the
older 50-credit/audio route.
