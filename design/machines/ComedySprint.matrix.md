# ComedySprint machine contract and failure catalog

Component: `studio.comedy`. Machine: `ComedySprint.machine.json`.

Placement: generated files under `studio/comedy/runs/<sprint-id>`. Concurrency:
one writer per sprint directory; validation is read-only and offline.

States trace to the `ComedySprintStatus` enum. `verifying` is an operational
overlay and does not make a sprint client-ready.

## Named-unit contract

| name | kind | signature | pre/post | maps to |
|---|---|---|---|---|
| `validateComedySprint` | actor | `(input{sprintId}) -> report{premises,personas,filter,tournaments,boards,renders,qa,cost,claims}` | pre: sprint directory exists. post: deterministic report; no external call | `studio.validator -> studio.comedy` |
| `allComedySprintChecksPass` | guard | `(report) -> bool` | true only for 120 premises, six personas, deterministic filter evidence, two recorded tournaments, 24 survivors, eight finalists, eight free boards, at most two V6 videos, zero premium videos, required QA, measured usage, and clean claims | `approval-before-paid-action`, `complete-product-chain`, `route-starts-from-client-question`, `package-required-files`, `package-manifest-valid`, `artifacts-exist`, `package-dogfood-verified`, `artifact-has-role`, `evidence-has-cost`, `evidence-has-qa`, `no-unsupported-performance-claim`, `default-paid-generation-policy`, `comedy-premise-quota`, `comedy-persona-coverage`, `comedy-premise-unique`, `comedy-premise-product-link`, `comedy-premise-text-bounded`, `deterministic-filter-first`, `mutation-before-final`, `comedy-finalist-quota`, `free-image-board-only`, `v6-two-video-cap`, `no-premium-comedy-video`, `tournament-evidence-recorded`, `tournament-usage-recorded`, `tournament-rationale-recorded` |
| `clearLastError` | action | `(ctx) -> ctx` | clears prior failure before a fresh validation | fresh validation |
| `recordVerifiedSprint` | action | `(ctx,report) -> ctx` | records verified counts and evidence paths | `ComedySprint` |
| `recordValidationFailure` | action | `(ctx,report) -> ctx` | records first failed check and returns to Draft | fail-closed gate |
| `recordValidatorError` | action | `(ctx,error) -> ctx` | records local validator error and returns to Draft | fail-closed gate |
| `recordAlreadyVerified` | action | `(ctx) -> ctx` | records idempotent verification without downgrading | stable verified sprint |
| `recordRetirement` | action | `(ctx) -> ctx` | marks sprint retired | `retire` action |

## Failure catalog

| failure | detection | transition | recovery | residual risk |
|---|---|---|---|---|
| Premise count not 120 | premise report false | `verifying -> Draft` | regenerate missing persona/premise rows | none after gate passes |
| Persona coverage not six-by-20 | persona report false | `verifying -> Draft` | repair persona assignment | none |
| Deterministic filter evidence missing | filter report false | `verifying -> Draft` | run filter stage before tournament | none |
| First round does not output 24 | round-one count false | `verifying -> Draft` | rerun first tournament | TypeSafe usage already recorded |
| Mutation evidence missing | mutation report false | `verifying -> Draft` | mutate all 24 survivors | none |
| Second round does not output eight | round-two count false | `verifying -> Draft` | rerun second tournament | TypeSafe usage already recorded |
| Free board route missing or charged | board report false | `verifying -> Draft` | use current free GPT Image 2.5 route | promotion can change |
| More than two V6 videos | render report false | `verifying -> Draft` | operator review; no automatic retry | spend already occurred |
| Premium video model present | render policy false | `verifying -> Draft` | operator review | spend already occurred |
| No QA-passed V6 video | QA report false | `verifying -> Draft` | inspect technical/human QA; no automatic render | sprint remains Draft |
| Unsupported performance claim | claim scan false | `verifying -> Draft` | rewrite report limitation | none |
| Validator crash or timeout | invoke onError / after delay | `verifying -> Draft` | repair local validator and rerun | sprint remains Draft |

## Transition matrix

| # | source | event | guard | target | actions |
|---:|---|---|---|---|---|
| 1 | Draft | on:verify | - | verifying | clearLastError |
| 2 | verifying | invoke onDone | allComedySprintChecksPass | Verified | recordVerifiedSprint |
| 3 | verifying | invoke onDone | - | Draft | recordValidationFailure |
| 4 | verifying | invoke onError | - | Draft | recordValidatorError |
| 5 | verifying | after validationTimeout | - | Draft | recordValidatorError |
| 6 | Verified | on:verify | - | (internal) | recordAlreadyVerified |
| 7 | Verified | on:retire | - | Retired | recordRetirement |

## Invariant enforcement

| invariant | enforcement point |
|---|---|
| `approval-before-paid-action` | comedy pipeline policy gate |
| `complete-product-chain` | comedy sprint remains an extension of Creative Test Sprint |
| `route-starts-from-client-question` | sprint brief input |
| `package-required-files` | portfolio validator |
| `package-manifest-valid` | portfolio validator |
| `artifacts-exist` | comedy artifact path resolver |
| `package-dogfood-verified` | verified sprint evidence |
| `artifact-has-role` | comedy artifact role check |
| `evidence-has-cost` | tournament token plus render credit report |
| `evidence-has-qa` | technical/human QA evidence |
| `no-unsupported-performance-claim` | comedy claim scan |
| `default-paid-generation-policy` | board/video policy gate |
| `comedy-premise-quota` | exact premise count check |
| `comedy-persona-coverage` | six-by-20 persona matrix check |
| `comedy-premise-unique` | normalized premise uniqueness check |
| `comedy-premise-product-link` | product-tension field and text check |
| `comedy-premise-text-bounded` | premise length check |
| `deterministic-filter-first` | filter artifact ordering check |
| `mutation-before-final` | survivor mutation link check |
| `comedy-finalist-quota` | second-round output count check |
| `free-image-board-only` | board model and cost check |
| `v6-two-video-cap` | video task count check |
| `no-premium-comedy-video` | video model allowlist |
| `tournament-evidence-recorded` | tournament candidate/output/path check |
| `tournament-usage-recorded` | round token usage check |
| `tournament-rationale-recorded` | candidate rationale category check |
