# Jevmax Studio internal dogfood portfolio report

Date: 2026-09-20

## Conclusion

Jevmax Studio now has a complete five-product internal dogfood portfolio. Each
product has a reusable template, machine-readable manifest, measured cost and
QA evidence, portfolio-facing summary, and concrete repository artifacts. The
portfolio validator passes, the offline regression passes 36/36, all manifest
artifacts resolve, and the client routing index selects the correct next
product.

## Product portfolio

| Route | Product | Dogfood evidence | Current default cost basis | Normal next |
|---:|---|---|---|---|
| 1 | Category Signal Audit | 50-ad bounded scan, 21 tagged, 103-ID snapshot, three account findings | 0 render credits; 1,005 input / 114 output audit tokens | Brand Identity System |
| 2 | Brand Identity System | Ava seed, frozen contracts, Lost Future prompt, Eyecandy grammar, zero-cost GPT 2.5 image tests | 0 credits for current image tests | Creative Test Sprint |
| 3 | Creative Test Sprint | Eight existing V6 variants plus current LF001 V6 QA | 40 credits per V6 720p no-audio video; 320 projected for eight | Paid Launch Kit |
| 4 | Paid Launch Kit | V6 hero, thumbnail frame, copy variants, disclosure and measurement gates | 0 new-generation credits for package assembly | Growth Loop |
| 5 | Growth Loop | 103-ID survival snapshot, weekly read-only scan cadence, monthly review | 0 render credits for recurring snapshots | Creative Test Sprint |

## Routing result

`studio/INDEX.md` routes five concrete client situations:

1. unknown competitive signal → Category Signal Audit
2. inconsistent identity → Brand Identity System
3. controlled variants needed → Creative Test Sprint
4. winner ready for launch → Paid Launch Kit
5. ongoing optimization → Growth Loop

## Commercial launch kit

The public-safe go-to-market layer is under `studio/gtm/`:

- flagship internal dogfood case study
- Category Signal Sprint sales kit
- founder outreach playbook
- pilot tracker schema
- measured-fact evidence manifest

Verification:

```text
python3 studio/validate_gtm.py
status: PASS
documents: 6
public_safety: PASS
source_reconciliation: PASS
links: PASS
```

## Deterministic verification

Portfolio gate:

```text
python3 studio/validate_portfolio.py
status: PASS
products: 5
required_files_each: 4
all_manifest_artifacts_exist: true
claim_discipline: PASS
```

Offline regression:

```text
python3 benchmark.py --min-pass-rate 0.99
36 / 36 passed
aggregate pass rate: 100%
overall: PASS
```

Unified selftest:

```text
python3 jevmax.py selftest
status: PASS
commands: 10
live_ad_changes: false
api_calls: false
```

Go-to-market gate:

```text
python3 studio/validate_gtm.py
status: PASS
public_safety: PASS
source_reconciliation: PASS
```

## Machinery design gate

The portfolio is backed by a Machinery design under `design/`:

- Modelith lint: 0 errors, 0 warnings
- Gc-carrier: 12/12 invariants carried
- G2 architecture: 4 boundaries, 5 mitigated dependencies, 0 blocking findings
- G3 state machine: 7 machine transitions, 7 matrix rows, 1 fresh oracle
- Gx traceability: no blocking findings
- Gb build plan: 4 milestones with DoD coverage

Full command:

```bash
machinery check design
```

Latest result: **0 blocking findings**.

## Paivot execution record

Paivot epic `JEV-2fkt` was created and executed through six stories:

1. `JEV-v3gp` Category Signal Audit package
2. `JEV-xwe6` Brand Identity System package
3. `JEV-aopd` Creative Test Sprint package
4. `JEV-s1pc` Growth Loop package
5. `JEV-sugs` Paid Launch Kit package
6. `JEV-sx6v` Portfolio validator and routing index

All six stories passed delivery verification 9/9, were accepted, and closed.
The parent epic is closed and accepted. The execution loop was cancelled after
`epic_complete`.

## Generation policy compliance

This portfolio assembly used:

- new image generations: **0**
- new video generations: **0**
- paid external API calls: **0**
- live ad changes: **0**

The production policy pre-approves:

- free GPT Image 2.5 image boards
- V6 720p five-second no-audio videos at 40 credits

MiniMax H3, Seedance, and other premium routes require explicit approval.

## Honest limitations

1. The market scan is bounded, not a whole-library census.
2. Survival is not readable until the baseline is 60 days old.
3. Current GPT Image 2.5 zero-credit pricing is promotional.
4. V6 pricing can change.
5. No live paid test has measured ROAS or conversion lift.
6. Platform AI-disclosure requirements must be checked per client and
   jurisdiction before launch.
