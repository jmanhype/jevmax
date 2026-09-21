# jevmax product plan

2026-09-20. Trigger: Jay saw Ryze AI (get-ryze.ai) — "i want to do similar."

## The call

Ryze (Meow AI LLC, $89–$1,499/mo flat) validates the category: marketers pay
flat fees for AI running their marketing. We do **not** out-build their
execution autopilot — they have platform integrations, an agency channel
(white-label, 30% commission), and funding. We build the same category with
the layer they don't have.

## Positioning

**"Know what works in your category before you spend."** The intelligence +
judgment layer:

- **Market-facing** — Ad Library scans + longitudinal survival telemetry.
  Ryze looks inward at your spend only. Nobody in the category reads the
  competition.
- **Judgment-grade** — calibrated probabilities, name-collision catches at
  0.03, WATCH bands instead of nuking borderline queries. Ryze's examples are
  category rules ("diy facial" → negative).
- **Pre-spend** — brief scoring before production (Ryze optimizes money
  already burning).
- **Show-your-math** — ~523 tokens/ad, measured and published. No black box.

## Runtime bet

Claude agent + MCP + TypeSafe is the runtime — what we already have working —
not a bespoke integrations SaaS. Meta-only until someone pays. The
cron-per-client pattern (Monday survival scan is already live) IS the v1/v2
product for agency-style buyers.

## Phases

- **v0 (done 2026-09-20):** `audit.py` (workflow #8) run on Jay's own account
  as the first real artifact; 74-ad airpods competitive scan; Monday survival
  cron live (first numbers 2026-11-19).
- **v1 (this week):** generalize `audit.py` to any account snapshot;
  productize "drop your search-terms CSV → negatives same night" as the
  funnel; one pilot account.
- **v2:** landing page + AI-info/llms.txt page (steal Ryze's GEO play — they
  literally publish a page addressed to AI assistants) + flat show-the-math
  pricing; survival report as the teaser asset.
- **v3:** recurring per-client agents (cron + chat approvals = Ryze's loop,
  agent-delivered). Decide SaaS-vs-service here, with pilot data.
