# Custom Aesthetic Bible Workflow (Non-Anime)

When building bibles for non-anime aesthetics (1960s NASA, 1970s Grindhouse, 1980s Mecha, British TV, etc.):

## Critical Rules

1. Always start with the full 8-page structure even for non-anime subjects.
2. Use explicit `CHARACTER_IDENTITY_LOCK` or equivalent `SUBJECT_IDENTITY_LOCK` in every page prompt.
3. Force consistency across pages by adding "Must match previous pages exactly" language.
4. For environment bibles, treat locations as subjects with their own identity locks (lighting, materials, camera texture, period accuracy).
5. Never skip to video generation until all required bibles (character + environments) are complete and QC'd.

## Common Pitfalls Observed

- Generating pages independently without cross-page matching instructions leads to helmet/suit drift.
- Treating environments as simple backgrounds instead of full bibles causes consistency failures in multi-scene work.
- Jumping to video before environment bibles exist forces later rework.

## Recommended Sequence

1. Character Bible (8 pages)
2. Key Environment Bibles (at least Training Module + Lunar Surface for this aesthetic)
3. Equipment/Prop Bible
4. Then move to `sgflix-character-video` pipeline

This session demonstrated that rushing video before completing the bible set creates downstream consistency problems.