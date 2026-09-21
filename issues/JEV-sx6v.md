---
id: JEV-sx6v
title: "Studio portfolio validator and routing index"
status: closed
priority: 3
type: task
labels: [studio, dogfood, delivered]
parent: JEV-2fkt
created_at: 2026-09-21T06:03:13Z
created_by: batmanosama
updated_at: 2026-09-21T06:45:22Z
content_hash: "sha256:6f4aed6c1d9d3b6e4295bd7aa4ffbc24d6d3d83f352ef2b5a05caa248b77e757"
assignee: dev-JEV-sx6v
closed_at: 2026-09-21T06:45:22Z
close_reason: "Accepted: Independently verified INDEX.md routes all five situations with correct next products, validate_portfolio.py checks five packages/required files/schema/route chain/artifact existence/cost/QA/policy/claim discipline with typed functions and no stubs, premium and live-write policies are encoded, portfolio validator PASSes, and offline regression passes 36/36."
---

## Description
Create the portfolio-wide routing index and deterministic validator.

Acceptance criteria:
- INDEX.md routes a client to the correct product.
- validate_portfolio.py checks all five product packages.
- Every artifact referenced by every manifest exists.
- Premium generation policy is encoded.
- Offline regression remains 36/36.

## Acceptance Criteria


## Design


## Notes
## Implementation Evidence

### Files
- `studio/INDEX.md`
- `studio/validate_portfolio.py`
- `studio/PRODUCT_CONTRACT.md`
- `studio/README.md`

### CI/Test Results

PASS.

Commands run:

1. `python3 studio/validate_portfolio.py`
2. `python3 benchmark.py --min-pass-rate 0.99`
3. `pvg story deliver JEV-sx6v`
4. `pvg story verify-delivery JEV-sx6v`

Summary: Portfolio validator checks five products, required files, manifest schema, route chain, artifact existence, QA/cost fields, generation policy, claim discipline, and both verification commands. Offline regression is run separately in the final goal gate and must pass 36/36.

Commit SHA: 35758c3c0276b1068aafe41ab04ed3b8972fac64 (base HEAD; portfolio files intentionally remain uncommitted).

### AC Verification

- [x] INDEX.md routes a client to the correct product.
- [x] validate_portfolio.py checks all five product packages.
- [x] Every artifact referenced by every manifest exists.
- [x] Premium generation policy is encoded.
- [x] Offline regression remains 36/36.


## nd_contract
status: delivered

### evidence
- Transitioned via pvg story deliver on 2026-09-21.

### proof
- [ ] Developer evidence block must remain authoritative above this contract.


## History
- 2026-09-21T06:05:22Z status: open -> in_progress
- 2026-09-21T06:05:22Z claimed by dev-JEV-sx6v
- 2026-09-21T06:38:02Z status: in_progress -> in_progress
- 2026-09-21T06:45:22Z status: in_progress -> closed

## Links
- Parent: [[JEV-2fkt]]

## Comments
