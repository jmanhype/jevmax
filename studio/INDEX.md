# Jevmax Studio client routing index

Use this page to route a client to the first product they need. Do not start
with production if intelligence or identity is missing.

## Route map

| Client situation | Start here | Why | Normal next |
|---|---|---|---|
| “We do not know what competitors are running.” | [Category Signal Audit](products/01-category-signal-audit/PORTFOLIO.md) | Establish category signal and account blockers first | Brand Identity System or Creative Test Sprint |
| “Our AI creative looks different every time.” | [Brand Identity System](products/02-brand-identity-system/PORTFOLIO.md) | Lock a fictional identity, wardrobe, product handling, and visual grammar | Creative Test Sprint |
| “We need ad variants but cannot afford random renders.” | [Creative Test Sprint](products/03-creative-test-sprint/PORTFOLIO.md) | Gate concepts, then use controlled V6 tests | Paid Launch Kit |
| “We have a creative winner and want to launch.” | [Paid Launch Kit](products/04-paid-launch-kit/PORTFOLIO.md) | Package asset, copy, disclosure, measurement, and approval | Growth Loop |
| “We need ongoing optimization.” | [Growth Loop](products/05-growth-loop/PORTFOLIO.md) | Repeat scans, audits, snapshots, and creative refreshes | Creative Test Sprint |

## Decision rules

1. If the ad account has never been audited, start with **Category Signal Audit**.
2. If there is no reusable character/style system, route to **Brand Identity System** before a sprint.
3. If identity exists but no controlled variants exist, route to **Creative Test Sprint**.
4. If a test candidate has been selected, route to **Paid Launch Kit**.
5. If a launch has been approved and measured, route to **Growth Loop**.
6. If the client requests guaranteed performance or silent ad automation, do not accept that scope.

## Portfolio gates

Run:

```bash
python3 studio/validate_portfolio.py
python3 benchmark.py --min-pass-rate 0.99
```

The portfolio is valid only when:

- all five product packages are complete
- every manifest artifact exists
- route order is complete
- no package claims unsupported performance
- V6 is the default video route
- premium generation is blocked without explicit approval

## Commercial launch kit

The public-safe case study, Category Signal Sprint sales kit, outreach
playbook, and pilot tracking schema are in [go-to-market](gtm/README.md).

The completed dogfood result is recorded in
[PORTFOLIO_REPORT.md](PORTFOLIO_REPORT.md).

## Current production policy

- Free GPT Image 2.5 image boards: pre-approved during the current promotion.
- V6 720p five-second no-audio videos: pre-approved at 40 credits each.
- Seedance, MiniMax H3, and other premium generation: explicit approval required.
- Live Meta writes or paid deployment: explicit client approval required.
