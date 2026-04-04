---
name: ideas
description: List and manage ideas across the pipeline. Usage: /ideas (list all), /ideas move "filename" to developing, /ideas archive "filename"
---

## Behavior

1. **Default (no args):** Glob all `.md` files (excluding PIPELINE.md and .gitkeep) in each ideas subdirectory (`~/.claude/ideas/inbox/`, `developing/`, `parked/`, `done/`). Present grouped by status with counts: `inbox(N) | developing(N) | parked(N) | done(N)`. Show title + created date + category for each idea.
2. **`move <filename> to <status>`:** Find the file across all ideas subdirs. Move it to the target folder using Bash `mv`. Update the `**Status**:` field inside the file to match the new folder. Confirm the move.
3. **`archive <filename>`:** Move to `done/` and update status to "done".
4. If a filename is ambiguous (partial match), list matches and ask user to clarify.

## Tools

Read, Edit, Glob, Bash
