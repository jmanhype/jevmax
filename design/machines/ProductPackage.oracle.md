# Generated transition oracle: `productpackage`

Generated from `ProductPackage.machine.json` by `machinery oracle`. DO NOT EDIT BY HAND.
<!-- machinery-version: v0.3.11 -->
Single source of truth for the hard-TDD transition tests: one transition row is one
test case. Key tests on the STABLE id, not the row number; row numbers renumber when
the design changes, stable ids do not.

## State entry / exit actions

| state | kind | entry | exit |
|---|---|---|---|
| Draft | atomic | - | - |
| validating | atomic | - | - |
| DogfoodVerified | atomic | - | - |
| Retired | final | - | - |

## Transitions

| test id | stable id | source | trigger | guard | target | actions |
|---|---|---|---|---|---|---|
| T-PROD-01 | PROD-a89c26 | Draft | on:verify | - | validating | clearLastError |
| T-PROD-02 | PROD-92141d | validating | after:validationTimeout | - | Draft | recordValidatorError |
| T-PROD-03 | PROD-6c7114 | validating | onDone:validatePortfolioPackage | allPackageChecksPass | DogfoodVerified | recordVerifiedEvidence |
| T-PROD-04 | PROD-6e36c7 | validating | onDone:validatePortfolioPackage | - | Draft | recordValidationFailure |
| T-PROD-05 | PROD-2da7f6 | validating | onError:validatePortfolioPackage | - | Draft | recordValidatorError |
| T-PROD-06 | PROD-27b7dd | DogfoodVerified | on:verify | - | (internal) | recordAlreadyVerified |
| T-PROD-07 | PROD-93248e | DogfoodVerified | on:retire | - | Retired | recordRetirement |

Total transitions (test cases): 7
