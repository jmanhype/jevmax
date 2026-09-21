# BUILD: Jevmax Studio Product Portfolio

Mode: full (self-contained)

## 1. Purpose and scope

Build a deterministic commercial product layer for Jevmax Studio. The layer
routes a client through five products, verifies that each product package has
real artifacts and measured evidence, blocks unsupported claims and premium
generation by default, and leaves live ad deployment to explicit client
approval.

In scope:

- five product packages
- client routing index
- public-safe go-to-market kit
- Comedy Test Sprint premise/tournament pipeline
- deterministic portfolio validator
- manifest artifact verification
- measured cost and QA evidence
- claim discipline
- paid-generation policy

Out of scope:

- new paid media generation
- live ad deployment
- replacement of existing intelligence or rendering scripts
- guaranteed performance claims

## 2. Glossary

- **Client**: brand founder or marketing operator receiving a product.
- **StudioDirector**: operator responsible for routing and standards.
- **Reviewer**: deterministic validator or human verifying evidence.
- **ProductPackage**: reusable commercial product directory.
- **Artifact**: concrete repository output cited by a manifest.
- **ProductEvidence**: measured cost, QA, verification date, and limitations.
- **PortfolioRoute**: deterministic mapping from client question to product.
- **DogfoodVerified**: internal package status granted only after validation.

## 3. Domain model

Source of truth: `design/domain.modelith.yaml`.

Entities:

- `Client`: supplies goal, product context, and paid-action approval.
- `PortfolioRoute`: maps client questions to ordered products.
- `ProductPackage`: owns template, manifest, evidence, and summary files.
- `Artifact`: path-valued evidence resolved by the validator.
- `ProductEvidence`: measured cost and QA record.

Primary invariants:

- `approval-before-paid-action`
- `complete-product-chain`
- `route-starts-from-client-question`
- `package-required-files`
- `package-manifest-valid`
- `artifacts-exist`
- `package-dogfood-verified`
- `artifact-has-role`
- `evidence-has-cost`
- `evidence-has-qa`
- `no-unsupported-performance-claim`
- `default-paid-generation-policy`

## 4. Architecture

Source of truth: `design/workspace.dsl` and `design/ARCHITECTURE.md`.

Containers:

- `studio.index`: client routing map and policy.
- `studio.packages`: five Markdown/JSON product packages.
- `studio.gtm`: public-safe case study, sales kit, outreach playbook, tracker schema, and evidence manifest.
- `studio.comedy`: premise generation, deterministic filtering, recorded Jev tournaments, mutation, board preparation, and bounded V6 render evidence.
- `studio.validator`: deterministic Python validator.
- `studio.artifacts`: existing repository outputs.

Allowed dependencies:

```text
studio.validator -> studio.packages
studio.validator -> studio.gtm
studio.validator -> studio.comedy
studio.validator -> studio.artifacts
studio.index -> studio.packages
studio.packages -> studio.artifacts
studio.gtm -> studio.artifacts
studio.comedy -> studio.artifacts
studio.comedy -> external.typesafe
studio.comedy -> external.pixverse
```

External Meta, TypeSafe, and PixVerse systems are evidence provenance only.
The portfolio validator does not call them.

Migration implementation plan: N/A - no legacy/target transition.

Neighbor stand-ins and test environment: N/A - not a pack child.

## 5. Behavior

Source machine: `design/machines/ProductPackage.machine.json`.

The product package starts in Draft. A verify event enters the transient
`validating` state and invokes the offline validator. If all package checks
pass, the package becomes DogfoodVerified. Validation failure, validator error,
or timeout returns it to Draft. A verified package can later retire.

Named-unit and failure contract:
`design/machines/ProductPackage.matrix.md`.

## 6. Traceability matrix

| invariant id | enforced by | component | interface contract | test |
|---|---|---|---|---|
| `approval-before-paid-action` | manifest policy and launch approval template | ProductPackage | package policy fields | launch approval checklist |
| `complete-product-chain` | route order and next product checks | PortfolioRoute | manifest route fields | validator route test |
| `route-starts-from-client-question` | index and manifest question checks | PortfolioRoute | client question field | index route test |
| `package-required-files` | required-file check | ProductPackage | package files | validator file test |
| `package-manifest-valid` | schema and key check | ProductPackage | manifest JSON | validator manifest test |
| `artifacts-exist` | path resolver | Artifact | artifact path field | validator path test |
| `package-dogfood-verified` | status and evidence check | ProductPackage | status field | validator status test |
| `artifact-has-role` | non-empty role check | Artifact | role field | validator role test |
| `evidence-has-cost` | measured cost fields | ProductEvidence | manifest cost object | validator evidence test |
| `evidence-has-qa` | QA fields and limitations | ProductEvidence | manifest QA object | validator evidence test |
| `no-unsupported-performance-claim` | claim scan | ProductPackage | portfolio prose | validator claim test |
| `default-paid-generation-policy` | manifest and index policy checks | ProductPackage | policy object | validator policy test |
| `comedy-premise-quota` | exact premise count | ComedySprint | premise CSV | comedy validator |
| `comedy-persona-coverage` | six-by-20 persona matrix | ComedySprint | persona column | comedy validator |
| `comedy-premise-unique` | normalized ID/text uniqueness | ComedyPremise | premise rows | comedy validator |
| `comedy-premise-product-link` | product tension and text link | ComedyPremise | product tension field | comedy validator |
| `comedy-premise-text-bounded` | 25–240 character bound | ComedyPremise | premise text | comedy validator |
| `deterministic-filter-first` | filter ordering evidence | ComedySprint | filter report | comedy validator |
| `mutation-before-final` | all survivor mutation links | ComedyPremise | mutation CSV | comedy validator |
| `comedy-finalist-quota` | second-round output count | ComedySprint | round-two report | comedy validator |
| `free-image-board-only` | board model and credits | ComedySprint | board manifest | comedy production validator |
| `v6-two-video-cap` | video count | ComedySprint | render manifest | comedy production validator |
| `no-premium-comedy-video` | V6 model allowlist | ComedySprint | render manifest | comedy production validator |
| `tournament-evidence-recorded` | candidate/output/path reconciliation | TournamentRound | round report | comedy validator |
| `tournament-usage-recorded` | token usage fields | TournamentRound | round report | comedy validator |
| `tournament-rationale-recorded` | rationale category per candidate | TournamentRound | scores CSV | comedy validator |

## 7. Test specification

The transition oracle is:

`design/machines/ProductPackage.oracle.md`

`design/machines/ComedySprint.oracle.md`

Conformance tests must parse the oracle table and assert every stable row.
The practical repository gate is:

```bash
python3 studio/validate_portfolio.py
python3 studio/validate_gtm.py
python3 studio/comedy/validate_run.py <comedy-run> --full
python3 benchmark.py --min-pass-rate 0.99
```

Required validator properties:

- exactly five products
- four required files per product
- valid manifest schema
- correct product id, order, status, and next route
- every artifact path exists
- measured cost basis exists
- QA result exists
- live ad changes are false
- premium generation is false
- unsupported claim assertions fail
- index documents both verification commands
- comedy run has 120 premises, six personas, deterministic filter evidence, two recorded tournaments, 24 survivors, and eight finalists
- comedy production has eight free boards, at most two V6 videos, zero premium models, and at least one technical QA pass
- public-safe go-to-market documents reconcile measured source facts
- comedy premise, tournament, board, video, QA, and policy evidence reconcile

## 8. State migration

No persisted instances yet. Package state is derived from files and validation
output; it is not stored in a database.

## 9. Build plan

**M0 - walking skeleton validator**

Implement one-package shape and artifact-path validation, then run it against a
temporary fixture with one passing and one failing package. Instantiate the
NFR mechanisms: deterministic output, fail-closed behavior, no external calls,
and explicit validator errors.

DoD: cover oracle rows `PROD-a89c26` and `PROD-6c7114`, all required file and
artifact properties, and the local validator command.

**M1 - five product packages**

Create the Category Signal Audit, Brand Identity System, Creative Test Sprint,
Paid Launch Kit, and Growth Loop directories with template, manifest, evidence,
and portfolio summary.

DoD: all five product routes validate, every manifest artifact resolves, every
product records cost and QA evidence, and no package contains an unsupported
performance assertion.

**M2 - routing index and policy**

Implement the client-facing routing index and central generation policy.

DoD: every concrete client situation routes to the correct product, every
product appears in the index, and premium generation requires explicit
approval.

**M3 - complete portfolio gate**

Run portfolio validation and the existing offline regression together.

DoD: `python3 studio/validate_portfolio.py` passes, `python3 benchmark.py
--min-pass-rate 0.99` passes 36/36, all product manifests resolve, and the
goal audit records the evidence.

**M4 - public-safe go-to-market kit**

Create the flagship case study, Category Signal Sprint sales kit, founder
outreach playbook, pilot tracker schema, and evidence manifest.

DoD: `python3 studio/validate_gtm.py` passes, all measured facts reconcile to
saved sources, no private account identifier appears, all links resolve, and
unsupported performance claims are excluded.

**M6 - Comedy Test Sprint pipeline**

Generate 120 premises from six personas, filter deterministically, run the first
Jev tournament to 24 survivors, mutate all survivors, run the second Jev
tournament to eight finalists, create eight free GPT Image 2.5 Sunburst boards,
and render at most two V6 720p no-audio videos.

DoD: `python3 studio/comedy/comedy_sprint.py selftest` passes, the real run's
selection validator passes, the full comedy validator passes, at least one V6
video passes technical QA, and no premium video route appears.

## 10. Language realization notes

Target language: Python 3 standard library.

The machine is realized as a deterministic validator and explicit package
status field rather than a long-running stateful service. Validation reads the
current filesystem, emits one report, and exits.

## Toolchain

Toolchain pins:

- Python 3.14.3 current repository runtime
- standard library `json`, `pathlib`, `argparse`, `re`
- Machinery 0.3.x design gates
- no new runtime dependency

## 11. Hard-TDD protocol

1. Run `modelith lint design/domain.modelith.yaml`.
2. Run `machinery oracle design/machines`.
3. Run `machinery check design --gate gc,g2,g3,gx`.
4. Add validator tests before changing validator behavior.
5. Run `python3 studio/validate_portfolio.py`.
6. Run `python3 benchmark.py --min-pass-rate 0.99`.
7. Do not modify tests to hide a missing artifact or unsupported claim.

## 12. Open questions and residual risks

- Current GPT Image 2.5 pricing is promotional and can change.
- V6 40-credit pricing can change.
- The Ad Library sample is bounded and newest-first.
- Survival evidence is not valid until the baseline is 60 days old.
- No live paid test has measured advertising performance.
- Platform AI-disclosure requirements vary by client and jurisdiction.
- TypeSafe or PixVerse network failure blocks the live tournament/render stages; local selftests must not be presented as live Jev evidence.

### What the gates do not verify

Not covered by any deterministic check or proof, by construction: whether the
interrogation extracted the RIGHT invariants (a shallow domain model gates
clean); guard and action semantics in code (the named-unit contracts carry
them into tests; a wrong implementation of a correctly-named guard is caught
by tests, not proofs); races between concurrent machine instances, and message
loss, duplication, or reordering between machines (the models are
single-instance; the event-contract table and idempotency contracts govern
those seams, and the tests exercise them); whether migration transformations
preserve real production data (Gm proves decision coverage, not the
implementation or a database run); coupling through shared database tables or
bus topics (invisible to import analysis; the event-contract table governs
it); and security, capacity, and observability beyond what the Phase 2 NFR
record captures.
