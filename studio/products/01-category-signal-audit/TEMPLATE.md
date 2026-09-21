# Category Signal Audit — Client Production Template

## Client

- Client:
- Category:
- Search terms:
- Competitor pages:
- Countries:
- Ad account ID:
- Audit date:

## 1. Scope

This audit answers four questions:

1. What are competitors running now?
2. Which hooks and offers appear in the bounded sample?
3. What is broken or risky in the client ad account?
4. What should be tested first?

## 2. Inputs

- [ ] Bounded Ad Library scan saved as JSON
- [ ] Ad IDs and delivery start dates captured
- [ ] Read-only ad-account snapshot
- [ ] Existing tagged baseline, if any
- [ ] Landing page or product page
- [ ] Client exclusions or compliance rules

## 3. Bounded sample policy

Record the exact query set and limits:

| Parameter | Value |
|---|---|
| Search terms |  |
| Countries |  |
| Ad status | ACTIVE |
| Ad type | ALL |
| Limit per query |  |
| Queries run |  |

State prominently:

> This is a bounded sample, not a whole-library census.

## 4. Market output

- Unique ads:
- Tagged ads:
- Top advertisers:
- Hook mix:
- Offer mix:
- Delivery-start distribution:
- New IDs versus prior snapshot:
- IDs overlapping prior snapshot:

## 5. Account audit

For each finding, record:

| Finding | Evidence | Priority | Action | Spend at risk |
|---|---|---|---|---|
|  |  | now / soon / note |  |  |

Check at minimum:

- active campaigns with no recent spend
- campaign delivery state
- pixel or dataset activity
- linked Instagram accounts
- lead-gen ToS
- page configuration

## 6. Survival baseline

- Snapshot date:
- Unique IDs:
- Snapshot path:
- Minimum survival age:
- First valid survival read date:

Do not report survival until the baseline is at least 60 days old and the
sampling route is comparable.

## 7. Recommended next tests

1.
2.
3.

For each recommendation:

- evidence:
- risk:
- first test unit:
- pass criterion:

## 8. QA gates

- [ ] Every market number comes from a saved JSON artifact
- [ ] Every account finding cites a field from a read-only snapshot
- [ ] Bounded-sample limitation is stated
- [ ] No whole-library claim is made
- [ ] No performance lift is claimed
- [ ] The next product route is explicit

## 9. Delivery checklist

- [ ] Market signal section
- [ ] Account audit section
- [ ] Survival baseline section
- [ ] Three recommendations
- [ ] Raw JSON retained
- [ ] Tagged CSV retained, if tagging was approved
- [ ] Snapshot retained
- [ ] Audit report retained
