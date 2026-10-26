## 2026-09-21

```
2 snapshot(s), 2026-09-20 .. 2026-09-21; newest has 81 live IDs
No baseline is 60+ days old yet (earliest is 1d). First survival number readable on 2026-11-19.
```

Bonus diagnostic (NOT the official metric — 1-day overlap vs 2026-09-20 baseline, mostly reflects the newest-first result window, not true churn):
```
2 snapshot(s), 2026-09-20 .. 2026-09-21; newest has 81 live IDs
SURVIVAL (live 1+ days, baseline vs newest snapshot): 27/74 overall (36%)
  baseline 2026-09-20  n=74   alive=27   36%

BY HOOK (tagged at baseline only):
  direct_offer     n=44   43%
  curiosity_claim  n=18   44%
  (untagged)       n=12   0%

BY OFFER (tagged at baseline only):
  other_product    n=53   51%
  (untagged)       n=12   0%
  saas_subscription n=9    0%
```

Scans: keyword 50 (est 5785) / comfrt 25 (est 2941) / goodell 3 / neyoa 2 / lucas 1. Snapshot: 81 unique IDs (prev 74, delta +7).
## 2026-09-28

```
3 snapshot(s), 2026-09-20 .. 2026-09-28; newest has 80 live IDs
No baseline is 60+ days old yet (earliest is 8d). First survival number readable on 2026-11-19.
```

7-day window diagnostic (NOT official — newest-first window effect dominates; page-scoped scans are where true survivors surface: NEYOA's two 09-21 ads are both still live a week later):
```
3 snapshot(s), 2026-09-20 .. 2026-09-28; newest has 80 live IDs
SURVIVAL (live 7+ days, baseline vs newest snapshot): 3/155 overall (2%)
  baseline 2026-09-20  n=74   alive=1    1%
  baseline 2026-09-21  n=81   alive=2    2%

BY HOOK (tagged at baseline only):
  direct_offer     n=44   2%
  curiosity_claim  n=18   0%
  (untagged)       n=12   0%

BY OFFER (tagged at baseline only):
  other_product    n=53   2%
  (untagged)       n=12   0%
  saas_subscription n=9    0%
```

Scans: keyword 50 (est 5921) / comfrt 25 (est 4006) / goodell 1 / neyoa 4 / lucas 0. Snapshot: 80 unique IDs (prev week 81, delta -1).
## 2026-10-05

```
4 snapshot(s), 2026-09-20 .. 2026-10-05; newest has 78 live IDs
No baseline is 60+ days old yet (earliest is 15d). First survival number readable on 2026-11-19.
```

Diagnostics (window churn, NOT official): 14d=0/184, 7d=3/264. Real page-set signal: NEYOA 09-28 pair survived a week (2 of today's 3 7d-hits), but the 09-21 NEYOA veterans that survived week 1 died in week 2; Goodell's Nike re-post now 2 weeks live.
```
4 snapshot(s), 2026-09-20 .. 2026-10-05; newest has 78 live IDs
SURVIVAL (live 7+ days, baseline vs newest snapshot): 3/264 overall (1%)
  baseline 2026-09-20  n=103  alive=0    0%
  baseline 2026-09-21  n=81   alive=0    0%
  baseline 2026-09-28  n=80   alive=3    4%

BY HOOK (tagged at baseline only):
  direct_offer     n=44   0%
  curiosity_claim  n=18   0%
  (untagged)       n=12   0%

BY OFFER (tagged at baseline only):
  other_product    n=53   0%
  (untagged)       n=12   0%
  saas_subscription n=9    0%
```

Scans: keyword 50 (est 6484) / comfrt 25 (est 2336, full creative swap: Dreamer Blanket + Airplane Mode Travel Hoodie) / goodell 1 / neyoa 2 / lucas 0. Snapshot: 78 unique IDs (prev 80, delta -2).
## 2026-10-12

```
5 snapshot(s), 2026-09-20 .. 2026-10-12; newest has 79 live IDs
No baseline is 60+ days old yet (earliest is 22d). First survival number readable on 2026-11-19.
```

**METHODOLOGY CORRECTION + FINDING:** NEYOA's Sep-21 pair (2367876897085532, 1740385033840426) reappeared this week after being absent on 10-05 — they FLAPPED (pause/resume or Library visibility), they did not die. Last week's 'died in week 2' note was wrong. Implication: snapshot absence != death; the survival metric should eventually count an ad alive if seen in ANY snapshot within its window (survival.py refinement TODO), and the 60-day baseline remains the right denoiser.

```
5 snapshot(s), 2026-09-20 .. 2026-10-12; newest has 79 live IDs
SURVIVAL (live 21+ days, baseline vs newest snapshot): 3/184 overall (2%)
  baseline 2026-09-20  n=103  alive=1    1%
  baseline 2026-09-21  n=81   alive=2    2%

BY HOOK (tagged at baseline only):
  direct_offer     n=44   2%
  curiosity_claim  n=18   0%
  (untagged)       n=12   0%

BY OFFER (tagged at baseline only):
  other_product    n=53   2%
  (untagged)       n=12   0%
  saas_subscription n=9    0%
```

Scans: keyword 50 (est 5994) / comfrt 25 (est 4540; 'Cozy With Something to Fidget' wave + Dreamer Blanket/hoodie carryover) / goodell 0 (Nike re-post died wk3) / neyoa 4 / lucas 0. Snapshot: 79 unique IDs (prev 78, delta +1).
## 2026-10-26

NOTE: 2026-10-19 scan MISSED (cron did not run that Monday) — one week gap in snapshot continuity.

```
6 snapshot(s), 2026-09-20 .. 2026-10-26; newest has 75 live IDs
No baseline is 60+ days old yet (earliest is 36d). First survival number readable on 2026-11-19.
```

Diagnostics (window churn, NOT official): 28d=0/264. NEYOA fully empty this week (all 4 from 10-12 gone — death or flap; flapping precedent says wait before calling it). Comfrt rotated creative AGAIN (all 25 created within ~2h of scan: Teddy Softness / Stay-In Season / Snak Hoodie / One More Look).
```
6 snapshot(s), 2026-09-20 .. 2026-10-26; newest has 75 live IDs
SURVIVAL (live 28+ days, baseline vs newest snapshot): 0/264 overall (0%)
  baseline 2026-09-20  n=103  alive=0    0%
  baseline 2026-09-21  n=81   alive=0    0%
  baseline 2026-09-28  n=80   alive=0    0%

BY HOOK (tagged at baseline only):
  direct_offer     n=44   0%
  curiosity_claim  n=18   0%
  (untagged)       n=12   0%

BY OFFER (tagged at baseline only):
  other_product    n=53   0%
  (untagged)       n=12   0%
  saas_subscription n=9    0%
```

Scans: keyword 50 (est 6277) / comfrt 25 (est 6443) / goodell 0 / neyoa 0 / lucas 0. Snapshot: 75 unique IDs (prev 79, delta -4).
