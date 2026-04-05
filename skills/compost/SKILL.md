---
name: compost
description: "Prune weak entities, archive stale pages, compact the knowledge graph. Weekly maintenance. Usage: /compost"
---

## Behavior

Like composting in a garden — decompose weak material to enrich the soil for stronger growth.

1. Read `~/.claude/journal/knowledge-graph.json` for the full graph.
2. Read `~/.claude/wiki/index.md` for wiki state.
3. Glob all wiki pages and read their frontmatter.

4. **Prune weak entities**: Find KG nodes with only 1 mention and no wiki page. These are noise — list them and offer to exclude from future KG builds (add to an ignore list in config).

5. **Archive stale pages**: Find wiki pages marked `stale: true` for more than 7 days (configurable via `wiki_stale_days`). Offer to either refresh them (re-synthesize from sources) or archive them (move to `~/.claude/wiki/_archive/`).

6. **Merge near-duplicates**: Use fuzzy matching on entity IDs to find near-duplicates (e.g., "gpt-5" and "gpt-52", "ai-safety" and "ai safety"). Propose merges.

7. **Compact the KG**: Remove orphaned edges (edges where one node was pruned). Recalculate cluster assignments. Rebuild graph JSON.

8. **Clean debounce markers**: Remove old files from `~/.claude/hooks/.kg-debounce/`.

9. **Report**:
   ```
   ## Compost Report — YYYY-MM-DD

   Weak entities identified: N (1-mention, no wiki page)
   - [list top 10 candidates for pruning]

   Stale pages (> 7 days): N
   - [list with last_updated dates]

   Near-duplicates found: N pairs
   - [entity A] ≈ [entity B]

   Orphaned edges removed: N
   KG compacted: N entities (was M), K connections (was L)
   Debounce cache cleared: N files
   ```

10. Ask for confirmation before executing destructive actions (pruning, archiving).
11. Append compost report to `~/.claude/wiki/log.md`.

## Tools

Read, Write, Edit, Glob, Grep, Bash
