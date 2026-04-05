---
name: sleep
description: "End-of-session consolidation — merge entities, promote tags, update staleness, compact the knowledge base. Usage: /sleep"
---

## Behavior

Run end-of-day (or end-of-session) consolidation, mimicking how the brain consolidates memories during sleep:

1. **Merge duplicates**: Scan KG nodes for entities that are likely the same thing with different names (e.g., "GPT-5" and "GPT-5.2", "AI safety" and "ai-safety"). Propose merges — update wiki pages to use canonical names.

2. **Promote tags to entities**: Find tag-only KG nodes with >= 3 mentions that don't have wiki pages. These have earned a page. Create entity pages for them.

3. **Update staleness**: For each wiki page, compare `last_updated` against the most recent journal/source entry that mentions any of its entities. Mark pages as `stale: true` if newer data exists.

4. **Strengthen connections**: Read today's journal entries. For each entity mentioned, update its wiki page's Connections table with any new co-occurring entities.

5. **Compact Source Logs**: For wiki pages with many source entries, summarize older entries while keeping recent ones detailed.

6. **Rebuild KG**: Run `python3 ~/.claude/hooks/build-knowledge-graph.py rebuild` to regenerate the graph with all current data.

7. **Rebuild wiki index**: Update `~/.claude/wiki/index.md` with current page counts and summaries.

8. **Generate sleep report**:
   ```
   ## Sleep Report — YYYY-MM-DD

   Merged: 2 entity pairs (GPT-5 + GPT-5.2 → GPT-5)
   Promoted: 3 tags to entity pages (cal-newport, deep-work, karpathy)
   Stale pages flagged: 2
   Connections strengthened: 5 pages updated
   KG rebuilt: N entities, M connections
   Index updated: N pages total
   ```

9. Append sleep report to `~/.claude/wiki/log.md`.

## Tools

Read, Write, Edit, Glob, Grep, Bash
