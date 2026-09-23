# Corrected SGFLIX Production Workflow

**Date**: 2026-05-19
**Source**: Repeated user corrections during Vixen / Vegeta / NASA aesthetic sessions

## Core Lesson

User has repeatedly corrected the following pattern:

**Wrong Approach (what the agent kept doing):**
- Jumping straight to video generation
- Using single last-frame continuation
- Skipping character bible creation
- Using multi-image only when forced

**Correct Approach (proven on Vegeta and Yusuke runs):**

1. Always create the full 8-page character bible first
2. Use multi-reference (3–7 images from the bible)
3. Follow the structured handoff prompt / factory specs method

This was documented in `SGFLIX_FACTORY_SYSTEM_CORRECTED_SOP.md` and reinforced multiple times in session.

## User Signals That Trigger This Rule

- Frustration when agent skips bible creation
- Corrections about "last frame only" vs multi-reference
- Explicit requests to "use the full SGFLIX factory pipeline"
- References to "Vegeta 7-ref method" or "Yusuke factory test"

## Implementation Rule

Before any video generation task involving character consistency or aesthetic resurrection:

1. Check if a character bible exists for the subject
2. If not, create one using this skill
3. Then proceed to video generation using multiple references from the bible

This is now a hard requirement for all future aesthetic and character work.