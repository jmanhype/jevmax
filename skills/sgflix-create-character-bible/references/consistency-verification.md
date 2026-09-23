# Cross-Page Consistency Verification

When building multi-page character bibles, consistency is the most common point of user frustration.

## Rule
After generating any page after Page 1, you MUST explicitly compare it to Page 1 (and previous pages) for:

- Helmet / headgear style and visor treatment
- Suit design, patches, hardware, and connectors
- Body proportions and morphology
- Color palette and material appearance

Never state "this matches the previous page" without actually checking.

## Common Failure Mode
The model often drifts on helmet style (bubble vs standard) or suit details between pages. This triggers strong user correction.

## Recommended Fix
When drift is detected, immediately regenerate the page with an explicit line in the prompt:
"Must match previous pages exactly: [list the specific elements that drifted]"

This lesson was learned during a 1960s NASA astronaut bible creation session where helmet style inconsistency caused significant user frustration.