# Image Reference Usage for Character Bibles

ALWAYS use **Codex CLI with the `-i` flag** for ALL bible generation — not just product-heavy ones. Reference images lock character identity across all 8 pages.

## Correct Method

```bash
codex exec --skip-git-repo-check -m gpt-image-2 -i /absolute/path/to/reference.png -- "Full prompt text here"
```

## Rules
- **Model:** ALWAYS use `gpt-image-2` for character bibles (not gpt-image-1). User will correct you if wrong.
- **Reference:** ALWAYS pass `-i` with a reference image. This keeps costumes, vehicles, props, and aesthetic consistent across all 8 pages.
- **Prompt length:** gpt-image-2 uses ~75k tokens per page (vs ~3k for gpt-image-1). Budget accordingly.
- **Output:** Codex saves to `~/.codex/generated_images/<session_id>/ig_*.png`. Must `cp` to target path manually.

## Shell Escaping
Complex prompts with quotes/special chars WILL break shell escaping. Write prompts to temp files:

```bash
echo "Your full prompt here" > /tmp/page_prompt.txt
PROMPT=$(cat /tmp/page_prompt.txt)
codex exec --skip-git-repo-check -m gpt-image-2 -i "$REF_IMAGE" -- "$PROMPT"
```

## Batch Generation
For 8+ pages, write a shell script looping through prompt files. Each page ~5 min. Run in background with `notify_on_complete=true`. See `references/batch-generation.md` for template.

## When to Apply
- ALL character bibles (not just product-heavy)
- ALL pages in a bible (consistency requires reference on every generation)
- Any multi-character project (use lead character's page_01 as `-i` for supporting characters)

## Why This Matters
Without `-i`, each page drifts — different face, different costume details, different vehicle. The reference image is the CHARACTER_IDENTITY_LOCK in practice.