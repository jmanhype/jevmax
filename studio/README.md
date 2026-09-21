# Jevmax Studio internal portfolio

Jevmax Studio is an evidence-controlled AI advertising studio. This portfolio
contains the five commercial products, reusable templates, measured dogfood
evidence, and the routing index.

Start with `INDEX.md` to choose a product. Each product directory contains:

- reusable production template
- machine-readable manifest
- measured evidence
- portfolio summary
- optional dogfood sample

The completed internal dogfood evidence and verification summary is in
`PORTFOLIO_REPORT.md`.

The public-safe launch assets are under `gtm/` and are verified with:

```bash
python3 studio/validate_gtm.py
```

Verification command:

```bash
python3 studio/validate_portfolio.py
python3 benchmark.py --min-pass-rate 0.99
```
