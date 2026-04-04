---
name: intro
description: Generate a context-aware self-introduction. Usage: /intro "for a GitHub bio" or /intro "for a conference talk"
---

## Behavior

1. Read `~/.claude/personal/bio.md` for raw facts. If it doesn't exist or contains only empty template placeholders, tell the user to fill in their bio first at `~/.claude/personal/bio.md`.
2. Parse the context argument (conference, GitHub, LinkedIn, email, Slack, etc.).
3. Generate an introduction tailored to:
   - **Length**: GitHub bio = 1 sentence; conference = 1 paragraph; LinkedIn = 3 paragraphs; email signature = 2 lines
   - **Tone**: Technical for GitHub; professional for LinkedIn; engaging for conference
   - **Emphasis**: Select relevant expertise/projects for the context
4. Output the introduction as ready-to-copy text.
5. Offer variations if the user wants alternatives.

## Tools

Read
