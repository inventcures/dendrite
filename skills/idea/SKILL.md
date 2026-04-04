---
name: idea
description: Quick-capture an idea to the inbox. Usage: /idea "Build a Claude Code plugin for automated code archaeology"
---

## Behavior

1. Parse the user's input for the idea title and any description.
2. Generate a slug: `YYYY-MM-DD-slugified-title.md` (lowercase, hyphens, no special chars).
3. Read `~/.claude/ideas/PIPELINE.md` for the template.
4. Create the file in `~/.claude/ideas/inbox/` using the template.
5. Pre-fill: Created date (today), Status=inbox, Category (infer from context or ask), Effort (infer or ask).
6. Fill in the "What" section from the user's description. Leave "Why" and "Notes" for the user to expand.
7. Confirm the capture with the full file path.

## Tools

Write, Read, Glob
