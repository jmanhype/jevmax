# Jevmax remaining work handoff

Date: 2026-09-21

This handoff records what is complete in this working tree and the exact work
that remains before the Comedy Test Sprint goal can be marked complete.

## Completed and locally verified

### Product portfolio

- Five product packages:
  - Category Signal Audit
  - Brand Identity System
  - Creative Test Sprint
  - Paid Launch Kit
  - Growth Loop
- Each package contains:
  - reusable template
  - valid manifest
  - measured evidence
  - portfolio summary
- Client routing index is implemented at `studio/INDEX.md`.
- Portfolio validator passes at `studio/validate_portfolio.py`.

### Go-to-market layer

- Public-safe flagship case study
- Category Signal Sprint sales kit
- Founder outreach playbook
- Pilot tracker schema
- Measured-fact evidence manifest
- Public-safety/source validator passes at `studio/validate_gtm.py`

### Machinery design governance

- Domain model
- Architecture contract
  - 6 boundaries
  - 10 allow rules
  - 13 transitive pairs
  - 7 deny rules
  - 2 no-path assertions
- Two state machines:
  - ProductPackage
  - ComedySprint
- Generated transition oracles
- Build plan with six DoD-bearing milestones
- Full Machinery check has 0 blocking findings

### Comedy Test Sprint implementation

The executable pipeline now supports:

1. 120 premise generation
2. six comedic personas, 20 premises each
3. deterministic product/safety/claim filters
4. recorded Jev tournament format
5. 24-survivor selection
6. persona-specific mutation
7. second tournament
8. eight-finalist selection
9. eight free GPT Image 2.5 board prompts
10. at most two V6 720p no-audio video prompts
11. production evidence normalization
12. technical/human QA evidence structure
13. full run validation

Offline structure selftest passes:

```text
120 premises
→ filters
→ 24 survivors
→ mutation
→ 8 finalists
→ 8 boards
→ 2 V6 prompts
→ full production-policy validation
```

The live AirPods run has already generated and filtered 120 premises.

## Immediate blocker

The current Codex execution sandbox has no usable DNS or outbound network
entitlement. The host resolver uses Tailscale MagicDNS at `100.100.100.100`,
but the sandbox reports:

```text
scutil --dns → No DNS configuration available
100.100.100.100:53 → Operation not permitted
```

Both `api.typesafe.ai` and unrelated hosts fail DNS resolution from this
shell. The blocker is the execution sandbox, not the pipeline, host Internet,
TypeSafe, or PixVerse.

The live Jev failure is recorded in:

`studio/comedy/runs/airpods-wired-2026-09-21/network-status.json`

Current recorded state:

- attempts: 5
- live scores: false
- mock scores used: false
- filtered premise input preserved

## Remaining execution sequence

Run from a normal macOS Terminal with normal host DNS:

```bash
cd /Users/batmanosama/jevmax
sh studio/comedy/resume-live-selection.sh
```

That command:

1. preserves the existing 120-premise corpus
2. runs live Jev round one to 24 survivors
3. mutates all 24 survivors
4. runs live Jev round two to eight finalists
5. generates eight board prompts
6. creates the PixVerse board queue command file
7. validates the selection artifacts

It intentionally submits no PixVerse generation.

After live selection succeeds:

1. Run the board queue command file.
2. Verify all eight GPT Image 2.5 Sunburst boards completed at zero credits.
3. Run:

   ```bash
   python3 studio/comedy/prepare_videos.py \
     --run studio/comedy/runs/airpods-wired-2026-09-21 \
     --count 2
   ```

4. Generate the V6 video queue command file.
5. Submit no more than two V6 720p no-audio videos.
6. Run PixVerse technical QA.
7. Normalize board/render/QA evidence:

   ```bash
   python3 studio/comedy/finalize_production.py \
     --run studio/comedy/runs/airpods-wired-2026-09-21 \
     --board-result <board-queue-result.json> \
     --render-result <video-queue-result.json> \
     --qa-result <qa-report.json> \
     --human-review
   ```

8. Validate the full run:

   ```bash
   python3 studio/comedy/validate_run.py \
     studio/comedy/runs/airpods-wired-2026-09-21 \
     --full
   ```

9. Re-run:

   ```bash
   python3 studio/comedy/comedy_sprint.py selftest
   python3 studio/validate_portfolio.py
   python3 studio/validate_gtm.py
   machinery check design
   python3 benchmark.py --min-pass-rate 0.99
   ```

10. Audit the client-facing report for:

    - real round-one scores and rationales
    - 24 real survivors
    - mutation links
    - round-two scores and rationales
    - exactly eight finalists
    - measured TypeSafe token usage
    - eight free board receipts
    - at most two V6 task receipts
    - no MiniMax or Seedance task
    - at least one technical QA pass
    - no unsupported performance claim

## Commercial next steps after the technical goal

1. Commit and push this working tree.
2. Add 10 real qualified prospects to the pilot tracker.
3. Send five first-touch outreach messages.
4. Book three discovery calls.
5. Sell the first Category Signal Audit.
6. Convert one audit into a Category Signal Sprint.
7. Capture a written client approval before any live campaign action.

## Do not claim yet

- no ROAS
- no conversion lift
- no production performance lift
- no whole-library coverage
- no blind-holdout result
- no 60-day survival rate before 2026-11-19
