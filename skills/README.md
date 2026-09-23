# jevmax skills bundle

Vendored agent skills (agentskills.io format — one folder per skill, each with a
`SKILL.md`) so this repo is self-contained: the whole Jevmaxxing pipeline —
judgment, writing, validation, and generation routing — travels with the code.

Install them into any agent's skill directory with `install_skills.py` (repo root):

    python3 install_skills.py                 # -> ~/.zcode/skills
    python3 install_skills.py --agent claude  # -> ~/.claude/skills
    python3 install_skills.py --agent codex   # -> ~/.codex/skills (also ~/.agents/skills)
    python3 install_skills.py --target D:\any\skill\dir

## What's in here (40 skills)

| Collection | Skills | Source | License |
|---|---|---|---|
| short-drama pipeline | `short-drama`, `-novel-analyze`, `-develop`, `-write`, `-assets`, `-image-prompts`, `-storyboard`, `-video-prompts`, `-produce`, `-edit`, `-review` (11) | github.com/zenstory-ai/drama-skills (`skills/*` @ main) | MIT |
| screenwriting craft | `sw-*` (24) + `chekhov-dramaturgy`, `ozu-screenplay-style`, `succession-series-writing` (26) | github.com/jtydhr88/screenwriting-skills (`plugins/screenwriting/skills/*` @ main) | MIT (book quotes remain with owners — see NOTICE in source repo) |
| sgflix validation/bibles | `sgflix-poster-first-validate`, `sgflix-create-character-bible` (2) | gist.github.com/jmanhype/4f852148ec4fa205c1dae062c397c78f | by the jevmax author; no explicit license file in gist |
| typesafe-ai | `typesafe-ai` (1) | docs.typesafe.ai/agent-skill | TypeSafe docs |

Local modifications (documented, minimal):
- `sgflix-poster-first-validate/SKILL.md` — the gist original had no YAML
  frontmatter (agents skip such skills); name/description/version were added
  from the skill's own body text. Nothing else changed.
- sgflix filenames in the gist were flattened (`skill__subdir__file`); the
  folder structure here is the reconstruction.

## Environment notes for this machine

- Generation models referenced by the skills (`gpt-image-2`, Nano Banana Pro /
  `gemini-3-pro-image`, Kling video) are reachable through the Kling MCP server
  (`mcp__klingai__*` tools). The sgflix skills' hardcoded endpoints
  (localhost:8648 hermes API, Codex App Server :9100) are the original author's
  infrastructure and do not exist here — route generation through Kling MCP.
- Kling's `gpt-image2` has no 27:40 poster ratio; use 2:3 (closest) for posters.
- `short-drama-edit` rendering needs `ffmpeg`/`ffprobe` on PATH (not yet
  installed on this machine). Python 3.9+ is required by drama-skills; 3.14.7
  is installed.
- Skills are scanned at session start — after installing, start a new
  conversation for them to auto-trigger (or read the SKILL.md files directly).
