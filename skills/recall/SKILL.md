---
name: recall
description: Search past learnings from the journal and knowledge graph. Usage: /recall "typescript discriminated unions" or /recall "#react"
---

## Behavior

1. Accept a search query (topic, tag, or free text).
2. Grep `~/.claude/journal/` recursively for matching entries.
3. Parse matches into structured results (date, category, title, content snippet).
4. Present results sorted by most recent first.
5. If > 10 results, show top 10 with "N more found — refine your search".
6. If 0 results, suggest: check spelling, try related terms.
7. **Graph-augmented search:** If `~/.claude/journal/knowledge-graph.json` exists, also run `python3 ~/.claude/hooks/build-knowledge-graph.py query "<search_term>"` via Bash and present connected entities as a "Related entities from knowledge graph:" section after grep results.
8. **Index rebuild:** If `~/.claude/journal/index.md` is missing or older than 24 hours, rebuild it — scan all journal files, count entries by tag and category, list recent 7 days of activity.

## Tools

Grep, Read, Glob, Bash
