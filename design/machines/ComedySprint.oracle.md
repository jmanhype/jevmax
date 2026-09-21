# Generated transition oracle: `comedysprint`

Generated from `ComedySprint.machine.json` by `machinery oracle`. DO NOT EDIT BY HAND.
<!-- machinery-version: v0.3.11 -->
Single source of truth for the hard-TDD transition tests: one transition row is one
test case. Key tests on the STABLE id, not the row number; row numbers renumber when
the design changes, stable ids do not.

## State entry / exit actions

| state | kind | entry | exit |
|---|---|---|---|
| Draft | atomic | - | - |
| verifying | atomic | - | - |
| Verified | atomic | - | - |
| Retired | final | - | - |

## Transitions

| test id | stable id | source | trigger | guard | target | actions |
|---|---|---|---|---|---|---|
| T-COME-01 | COME-7e4189 | Draft | on:verify | - | verifying | clearLastError |
| T-COME-02 | COME-66184e | verifying | after:validationTimeout | - | Draft | recordValidatorError |
| T-COME-03 | COME-71dc51 | verifying | onDone:validateComedySprint | allComedySprintChecksPass | Verified | recordVerifiedSprint |
| T-COME-04 | COME-a56c75 | verifying | onDone:validateComedySprint | - | Draft | recordValidationFailure |
| T-COME-05 | COME-ef132a | verifying | onError:validateComedySprint | - | Draft | recordValidatorError |
| T-COME-06 | COME-9d3b04 | Verified | on:verify | - | (internal) | recordAlreadyVerified |
| T-COME-07 | COME-6faaf2 | Verified | on:retire | - | Retired | recordRetirement |

Total transitions (test cases): 7
