# The Jevmaxxing playbook, built — two pipelines and a shared brain

A working system for running marketing like a systematic trader: **watch the
market, judge what survives, produce against it, audit your own spend, repeat.**
Not a deck — everything below runs today, as plain Python + a few CLI tools,
with every cost measured instead of asserted.

Two pipelines share one judgment engine:

```
PIPELINE A (intelligence)          PIPELINE B (creative production)
watch what survives in your        mass-produce disciplined ad
category  ────────────────┐        variants against those patterns
                          ▼
              ┌─────────────────────────┐
              │   JEV (TypeSafe S1 API) │   ← the shared brain
              │   state + questions →   │
              │   structured judgment   │
              └───────────┬─────────────┘
                          │
        PIPELINE A' (audit): which of MY decisions leak money
```

---

## 0. The shared brain — "Jev"

[TypeSafe System One](https://typesafe.ai) (`jev-latest`): you POST a `state`
(any JSON) plus any number of independent `questions`; it returns structured
answers (including calibrated probabilities) per question. A ~90-line stdlib
client (`typesafe.py`) wraps it: retries on 429/529, batches concurrent
requests, and **prints measured input/output tokens on every run**. Discipline:
no workflow ships until its real token cost per unit of work is known.

Costs measured: ~20 tokens/ad tagged (Ad Library scan) · ~30 tokens/search
query sorted · ~1,100 tokens for a full account audit ranking.

---

## 1. Pipeline A — market intelligence ("what works")

### 1a. Ad Library scan + tagging — `ad_library_scan.py`
Pulls live ads from the Meta Ad Library (via the `ads_library_search` MCP tool,
read-only, free), then asks Jev per ad: which hooks does it use (pain question?
proof stats? founder story? curiosity claim? direct offer?). Output: raw JSON →
tagged CSV with `days_running` per ad.

**The core insight:** runtime is a free profitability signal. Nobody keeps a
losing ad live for 90 days.

### 1b. Longitudinal survival — `survival.py`
The Ad Library is newest-first, ~2 days deep, **no pagination** — you cannot
see history directly. Fix: snapshot the set of live ad IDs every scan day; the
report then asks *what % of a 60-day-old baseline is still alive today?*
Survivors = the category's actual money printers. Snapshots are cheap (no LLM
calls); a Monday cron does scans + snapshot + report automatically.

- `python3 survival.py snapshot scan_*.json` — merge one day's IDs
- `python3 survival.py report --tags ad_library_mcp_tagged.csv --min-age 60`
- First baseline 2026-09-20 (74 ads) → first real numbers ~60 days later

### 1c. Search-term triage — `sort_search_terms.py`
Google Ads search-terms CSV in → one Jev buyer-intent verdict per query out →
`decisions.csv` split into KEEP / WATCH / NEGATIVE, plus `negatives.csv` ready
to paste back into Google Ads. Scales: ~30 tokens/query, projected cost for
50k queries printed before you commit.

### 1d. Account audit — `audit.py`
Points at any ad account: deterministic checks (active campaigns with no 28-day
spend + budget exposure math, pixel never fired, Instagram not linked, lead-gen
ToS missing), then Jev ranks findings now/soon/note into `audit_report.md`.
First real run found a 2022 $5/day zombie boost still spending — paused same day.

---

## 2. Pipeline B — creative production (7 layers)

```
1. IDEA     Lost Future GPT      style families (S01–S50: era+medium+genre)
                                 → concepts (TITLE + TAGLINE) → shot prompts
2. STORY    pick ad-worthy beats, hook first
3. GRAMMAR  Eyecandy             name the technique per shot (fisheye, object POV…)
4. SPEC     jevmax-creative-v2   JSON; character block VERBATIM-FROZEN;
                                 variable scene/wardrobe/pose/camera; any field
                                 may hold a list — `*_options` = alternatives
5. GATE     score_briefs.py      rank concepts BEFORE spending render credits
6. RENDER   flatten.py           one painter-paragraph per variant + manifest
7. MOTION   pixverse.py → CLI    seed still → approved → image-to-video kits
```

**The two rules that make layer 4/6 work:**

- A plain list is **compositional** — all items appear together in one prompt
  ("blue sky, a few wispy clouds, ocean horizon…"). A field named
  `*_options` is **alternatives** — the renderer cartesian-expands them (2
  times-of-day × 2 tops × 2 POVs = 8 variants from ONE spec, capped at 50).
- The character block never mutates between generations. Identity flows
  through a **seed still**: render once, approve it, and every variant
  references that image. Guardrails are structural, not vibes:
  `fictional_model_only`, `no_real_person_likeness`, `disclose_as_ai`
  (enforced at the ad layer via Meta's `self_ai_disclosure=OPT_IN`, never
  inside the image).

**Rendering (layer 7)** runs on the PixVerse CLI — an agent-grade CLI: OAuth
device-flow login, **prompts accept file paths** (so layer 6's output pipes
straight in, no pasting), `--json` output, deterministic exit codes, `--count
N --seed S` batches, and multi-reference modes for character consistency
(V6: up to 10 images). Each spec expands to kits containing the seed-image
command, the image-to-video command, and a TTS hook-line slot.

---

## 3. Measured economics (2026-09)

| Unit | Cost |
|---|---|
| Tag 1 Ad Library ad (Jev) | ~20 tokens |
| Triage 1 search term (Jev) | ~30 tokens |
| Seed still, 1080p (Nano Banana 2 via PixVerse) | 25 credits |
| 5s 720p 9:16 video (V6 image-to-video) | 50 credits |
| Full 9-variant creative batch | 475 credits ≈ 4% of a 12k Pro balance |

Failed renders are **not billed**. Retries are cheap; measure, don't guess.

---

## 4. Gotchas learned the hard way (the valuable section)

1. **The Ad Library shows ~2 days of history.** Any "trend" claim without
   longitudinal snapshots is fiction. Snapshot IDs daily; diff weekly.
2. **AI video audio is a dice roll.** V6 generates sound *natively and
   unscripted* — some takes come out with improvised (unintelligible) speech,
   some with just wind. Controls: `--no-audio` forces silence; `--seed N`
   makes video+audio reproducible; scripted speech = TTS (`create voice`) +
   lip-sync, only on keepers.
3. **Models read camera language loosely.** "Overhead flat-lay" came back as
   a high close-up. If framing matters, say it twice, concretely.
4. **Negations are weakly honored.** `constraints.avoid` never enters the
   painter prompt — it guides the translator. Describe what you WANT.
5. **Composition vs alternatives must be explicit in the schema**, or the
   cartesian expansion manufactures nonsense (all-objects-at-once prompts).
6. **Two wallets.** PixVerse app/CLI (subscription credits) and the platform
   API (pay-as-you-go) are separate balances; the API key validates fine at
   0 credits and blocks silently. Pick the wallet on purpose.
7. **Prompt-as-file-path + JSON output + exit codes** is what makes an AI
   pipeline agent-operable. Any tool that requires copy-paste into a web UI
   is a pipeline break.

---

## 5. Repo layout (stdlib Python 3, no dependencies)

```
jevmax/
├── typesafe.py            # shared Jev client (ask / ask_batch, prints tokens)
├── ad_library_scan.py     # A: scan + tag ads
├── survival.py            # A: snapshots + survival report (selftest included)
├── sort_search_terms.py   # A: query triage → negatives
├── audit.py               # A: account audit → ranked report
├── render_videos.py       # B: batch video producer (fail-tolerant, logs CSV)
├── creative/
│   ├── pipeline.md        # the 7-layer engine doc + status
│   ├── lost_future_example.md  # captured output grammar + schema mapping
│   ├── persona-*.json     # v2 specs (base + wildcard variants)
│   ├── renders/           # approved identity seeds
│   └── pixverse/          # kits, prompts, videos, render_log.csv
└── snapshots/             # daily Ad Library ID sets (survival baselines)
```

**Positioning:** not an execution autopilot — the *intelligence and judgment
layer*. The moat is survival data that accrues daily plus judgment-grade
decisions with the math shown, not another "generate videos for me" wrapper.
