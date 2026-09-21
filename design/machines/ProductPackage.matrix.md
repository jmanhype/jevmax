# ProductPackage machine contract and failure catalog

Component: `studio.packages`. Machine: `ProductPackage.machine.json`.

Placement: package files in `studio/products/**`. Concurrency: one author per
package directory; validation is read-only and may run concurrently with
authors in other directories but not while the package's own files are being
written.

States trace to the `PackageStatus` enum. `validating` is an operational overlay
for the offline validator invoke and does not grant client-ready status.

## Named-unit contract

| name | kind | signature | pre/post | maps to |
|---|---|---|---|---|
| `validatePortfolioPackage` | actor | `(input{slug,routeOrder}) -> report{checks,artifacts,cost,qa,policy,claims}` | pre: package exists. post: deterministic report; no repository mutation | `studio.validator -> studio.packages` and `studio.validator -> studio.artifacts` |
| `allPackageChecksPass` | guard | `(report) -> bool` | true iff required files, manifest, artifacts, evidence, route, policy, and claim checks pass | `package-required-files`, `package-manifest-valid`, `artifacts-exist`, `package-dogfood-verified` |
| `clearLastError` | action | `(ctx) -> ctx` | clears the prior failed check before a new validation run | fresh validation attempt |
| `recordVerifiedEvidence` | action | `(ctx,report) -> ctx` | records verification date, measured cost, QA status, and limitations | `ProductEvidence` |
| `recordValidationFailure` | action | `(ctx,report) -> ctx` | stores the failed check and remains Draft | fail-closed package gate |
| `recordValidatorError` | action | `(ctx,error) -> ctx` | stores validator runtime error and remains Draft | fail-closed package gate |
| `recordAlreadyVerified` | action | `(ctx) -> ctx` | records an idempotent verify attempt without downgrading status | stable verified package |
| `recordRetirement` | action | `(ctx) -> ctx` | marks package retired and removes it from the active route | `retire` action |

## Failure catalog

| failure | detection | transition | recovery | residual risk |
|---|---|---|---|---|
| Missing required file | validator report false | `validating -> Draft` | author missing file and rerun `verify` | none after gate passes |
| Invalid manifest JSON | validator throws or returns false | `validating -> Draft` | repair manifest and rerun | none |
| Missing artifact path | artifact check false | `validating -> Draft` | repair path or create artifact | none |
| Missing cost or QA evidence | evidence check false | `validating -> Draft` | record measured evidence | none |
| Wrong route | manifest route check false | `validating -> Draft` | repair `route_order`/`next_product` | none |
| Unsupported claim | claim scan finds non-negated banned claim | `validating -> Draft` | rewrite or explicitly negate limitation | none |
| Validator crash | invoke onError | `validating -> Draft` | fix validator and rerun | package remains non-client-ready |
| Validator timeout | after validationTimeout | `validating -> Draft` | inspect local files and rerun | package remains non-client-ready |

## Transition matrix

| # | source | event | guard | target | actions |
|---:|---|---|---|---|---|
| 1 | Draft | on:verify | - | validating | clearLastError |
| 2 | validating | invoke onDone | allPackageChecksPass | DogfoodVerified | recordVerifiedEvidence |
| 3 | validating | invoke onDone | - | Draft | recordValidationFailure |
| 4 | validating | invoke onError | - | Draft | recordValidatorError |
| 5 | validating | after validationTimeout | - | Draft | recordValidatorError |
| 6 | DogfoodVerified | on:retire | - | Retired | recordRetirement |
| 7 | DogfoodVerified | on:verify | - | (internal) | recordAlreadyVerified |

## Invariant enforcement

| invariant | enforcement point |
|---|---|
| `approval-before-paid-action` | package policy and launch approval checklist |
| `complete-product-chain` | manifest `route_order` and `next_product` checks |
| `route-starts-from-client-question` | `studio/INDEX.md` route map and manifest `client_question` |
| `package-required-files` | required file check |
| `package-manifest-valid` | manifest schema and key check |
| `artifacts-exist` | artifact path resolver |
| `package-dogfood-verified` | package status and evidence check |
| `artifact-has-role` | non-empty artifact role check |
| `evidence-has-cost` | measured cost fields |
| `evidence-has-qa` | QA status and limitations fields |
| `no-unsupported-performance-claim` | claim-discipline scan |
| `default-paid-generation-policy` | manifest policy and studio index policy gate |
