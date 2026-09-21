# Jevmax offline regression benchmark

- Mode: offline regression against recorded demo outputs
- Cases: 36 / 36 passed
- Aggregate pass rate: 100%
- Overall: PASS

| Workflow | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| Workflow #4 — buyer-intent search-term sorting | 25 | 25 | 100% |
| Workflow #6 — ad/page promise match | 1 | 1 | 100% |
| Workflow #5 — creative fatigue decision bands | 5 | 5 | 100% |
| Workflow #7 — lead quality scoring | 3 | 3 | 100% |
| Workflow #3 — brief scoring | 1 | 1 | 100% |
| Workflow #2 — survival boundary selftest | 1 | 1 | 100% |

## Measured recorded usage

| Run | Items | Tokens/item |
|---|---:|---:|
| search_terms_25 | 25 | 167 |
| briefs_3 | 3 | 507 |
| fatigue_5_flagged | 5 | 261 |
| page_match_1 | 1 | 858 |
| leads_3 | 3 | 412 |
| ad_tagging_12 | 12 | 523 |

## Limitations

- This is not a blind holdout; expected labels document the intended semantics of the demo fixtures.
- No TypeSafe API calls are made by benchmark.py.
- 30x, 90%, and whole-library claims are intentionally absent because they are not measured here.
