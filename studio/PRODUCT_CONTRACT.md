# Jevmax Studio Product Contract

This directory is the internal dogfood portfolio for Jevmax Studio. Each
commercial product is represented by one package under `products/`. A package
is complete only when it can be reused for a new client, cites measured cost
and QA evidence, and exposes a portfolio-facing summary that a founder can
review without reading the implementation.

## Required package files

Every product directory must contain:

| File | Purpose | Acceptance requirement |
|---|---|---|
| `TEMPLATE.md` | Reusable client-facing production template | Contains client placeholders, scope, inputs, outputs, QA gates, and delivery checklist |
| `MANIFEST.json` | Machine-readable artifact and routing manifest | Valid JSON with required product, deliverable, evidence, routing, cost, and QA fields |
| `EVIDENCE.md` | Measured dogfood evidence | Cites real repository artifacts, measured credits or tokens, QA result, limitations, and verification date |
| `PORTFOLIO.md` | Concise commercial summary | Explains client outcome, inclusions, exclusions, price guidance, timeline, and next product |

A product may also include a `SAMPLE.md` when a concrete dogfood output is
useful for review.

## Go-to-market layer

The public-facing commercial assets live under `studio/gtm/` and are validated
separately with `python3 studio/validate_gtm.py`. They must reconcile every
measured fact to a saved source artifact, avoid private identifiers, and state
performance limitations rather than invent ad results.

## Product routes

1. **Category Signal Audit**
   - Answers: what is competing, what is the account doing wrong, and what should be tested first?
   - Normal next route: Brand Identity System or Creative Test Sprint.

2. **Brand Identity System**
   - Answers: who is the reusable fictional brand character and what visual grammar controls them?
   - Normal next route: Creative Test Sprint.

3. **Creative Test Sprint**
   - Answers: which controlled concepts and motion variants deserve paid testing?
   - Normal next route: Paid Launch Kit.

4. **Paid Launch Kit**
   - Answers: what exactly should be launched, measured, disclosed, and approved?
   - Normal next route: Growth Loop.

5. **Growth Loop**
   - Answers: what recurring scans, audits, refreshes, and reviews keep the system improving?
   - Normal next route: another Creative Test Sprint.

## Production and cost policy

- Free GPT Image 2.5 image boards are pre-approved while the current paid-member promotion is active.
- V6 720p five-second videos are pre-approved at the measured 40-credit no-audio rate.
- Seedance, MiniMax H3, and other paid or premium generation require explicit operator approval.
- Every render record must identify model, quality, duration, task ID, local output, cost, and QA outcome where available.
- No live ad change or paid deployment occurs without explicit client approval.

## Claim discipline

The portfolio must not claim whole-library coverage, guaranteed ROAS,
production performance lift, or a blind holdout result. Longitudinal survival
claims require snapshots at least 60 days apart. Competitive findings from the
bounded Meta Ad Library sample must say that the sample is bounded.
