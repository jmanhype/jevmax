# Architecture: Jevmax Studio Product Portfolio

The portfolio is a thin commercial and verification layer over the existing
Jevmax repository. It does not replace the intelligence scripts, creative
schema, Meta MCP connector, TypeSafe client, or PixVerse runner. It makes their
outputs sellable by giving each commercial product a reusable template, a
manifest of real artifacts, measured evidence, QA status, and a deterministic
route to the next product.

## Architecture Contract

```yaml
contract_version: 2
boundaries:
  - id: studio.validator
    kind: container
    element: validator
    code: ["studio/validate_portfolio.py", "studio/validate_gtm.py"]
  - id: studio.packages
    kind: container
    element: packages
    code: ["studio/products/**"]
  - id: studio.comedy
    kind: container
    element: comedy
    code: ["studio/comedy/**"]
  - id: studio.gtm
    kind: container
    element: gtm
    code: ["studio/gtm/**"]
  - id: studio.index
    kind: container
    element: index
    code: ["studio/INDEX.md"]
  - id: studio.artifacts
    kind: container
    element: artifacts
    code: ["runs/**", "creative/**", "projects/**", "snapshots/**"]
externals:
  - id: external.meta
    element: meta
    imports: []
  - id: external.typesafe
    element: typesafe
    imports: []
  - id: external.pixverse
    element: pixverse
    imports: []
dependency_rules:
  allow:
    - studio.validator -> studio.packages
    - studio.validator -> studio.comedy
    - studio.validator -> studio.gtm
    - studio.validator -> studio.artifacts
    - studio.index -> studio.packages
    - studio.packages -> studio.artifacts
    - studio.comedy -> studio.artifacts
    - studio.comedy -> external.typesafe
    - studio.comedy -> external.pixverse
    - studio.gtm -> studio.artifacts
  deny:
    - "studio.validator -> external.meta"
    - "studio.validator -> external.typesafe"
    - "studio.validator -> external.pixverse"
    - "studio.packages -> external.meta"
    - "studio.packages -> external.typesafe"
    - "studio.packages -> external.pixverse"
    - "studio.comedy -> external.meta"
  assert:
    - no_path: studio.packages -> studio.validator
    - no_path: studio.artifacts -> studio.packages
  notes:
    - "External systems are evidence provenance in the package layer; the Comedy Test Sprint pipeline may call TypeSafe and PixVerse explicitly, but validators remain offline and deterministic."
```

## Interface contracts

| edge | shape | errors | idempotency |
|---|---|---|---|
| `studio.validator -> studio.packages` | read `TEMPLATE.md`, `MANIFEST.json`, `EVIDENCE.md`, `PORTFOLIO.md` | invalid JSON, missing key, wrong route, bad status | deterministic over unchanged files |
| `studio.validator -> studio.comedy` | read premise, tournament, board, render, cost, QA, and report artifacts | missing premise, malformed tournament, over-quota render, premium route, failed QA | deterministic over unchanged files |
| `studio.validator -> studio.gtm` | read public-safe Markdown, measured-fact JSON, and source-artifact paths | private identifier, unsupported claim, source mismatch, missing path | deterministic over unchanged files |
| `studio.validator -> studio.artifacts` | resolve every manifest artifact path | missing file | deterministic over unchanged files |
| `studio.index -> studio.packages` | route table links to product summaries | broken route | deterministic |
| `studio.packages -> studio.artifacts` | manifest cites artifact roles and paths | missing artifact, ambiguous role | manifest revision replaces prior citation |
| `studio.comedy -> external.typesafe` | batched premise judgment questions returning scores, fit, clarity, and rationale categories | HTTP 429/529, malformed answer, timeout | recorded request and token usage keyed by sprint/round |
| `studio.comedy -> external.pixverse` | free GPT Image 2.5 boards and at most two V6 720p no-audio video tasks | moderation rejection, task failure, download failure, pricing change | task IDs and local paths recorded; no blind retry |

## Dependency mitigation posture

| dependency | failure modes | mitigation | residual | bound |
|---|---|---|---|---|
| `external.meta` | unavailable, auth expired, bounded sample | package records prior live evidence and provenance; no validation-time call | latest live scan may be stale | no API call during portfolio validation |
| `external.typesafe` | unavailable, token cost | concept gate evidence is recorded before packaging | new concepts cannot be gated offline | recorded token usage only |
| `external.pixverse` | pricing change, moderation rejection, output failure | measured cost/QA evidence recorded by task ID; premium routes blocked | current price can change | only existing V6 artifacts used for dogfood packages |
| `studio.comedy -> external.typesafe` | API unavailable, rate limit, malformed judgments | bounded retries, fail closed, preserve partial corpus without selecting finalists | sprint remains Draft | two tournament rounds; no video before round two |
| `studio.comedy -> external.pixverse` | image moderation, video failure, pricing change | free boards first; max two V6 tasks; fail closed and preserve task IDs | no finalist render that round | image boards 8; V6 videos <= 2 |
| `meta` | element alias for `external.meta` | same mitigation as `external.meta` | same residual | same bound |
| `typesafe` | element alias for `external.typesafe` | same mitigation as `external.typesafe` | same residual | same bound |
| `pixverse` | element alias for `external.pixverse` | same mitigation as `external.pixverse` | same residual | same bound |
| repository filesystem | missing artifact path | validator fails closed | none | all manifests must resolve |

## Persistence and placement

| component | machine placement | persistence | concurrency |
|---|---|---|---|
| `ProductPackage` | studio.packages | Markdown/JSON files under `studio/products` | single author per package directory |
| `Artifact` (no machine: a path-valued evidence record checked synchronously) | studio.artifacts | repository files and project outputs | read-only during validation |
| `ProductEvidence` (no machine: immutable evidence attached to a package revision) | studio.packages | `EVIDENCE.md` plus manifest cost/QA fields | single author per package |
| `ComedySprint` | studio.comedy | JSON/CSV/Markdown artifacts under `studio/comedy/runs/**` | one sprint directory at a time |
| `ComedyPremise` (no machine: immutable premise row plus optional mutation link) | studio.comedy | premise CSV/JSON rows | generated sequentially per persona |
| `TournamentRound` (no machine: immutable score/rationale record) | studio.comedy | round JSON plus scores CSV | no concurrent writes to one sprint |
| `PortfolioRoute` (no machine: static route table validated as data) | studio.index | `INDEX.md` plus manifest route fields | single author |
| `GoToMarketAssets` (no machine: static public-safe evidence documents) | studio.gtm | Markdown and JSON under `studio/gtm` | single author |
| `Client` (no machine: external commercial actor; approvals are recorded evidence) | outside the portfolio system | client records are outside this design | explicit client approval input |

## NFR record

- Reliability: portfolio validation is offline and deterministic.
- Cost: validation performs no paid generation and no external API call.
- Safety: live ad changes and premium generation are policy-blocked absent explicit approval.
- Claim integrity: unsupported performance and whole-library claims fail validation.
