---
name: recall
description: Search past learnings from the journal and knowledge graph. Usage: /recall "typescript discriminated unions" or /recall "#react"
---

## Behavior

1. Accept a search query (topic, tag, or free text).
2. **Wiki-first search:** If `~/.claude/wiki/` exists, grep wiki page titles, frontmatter tags, and content for matches. If a wiki page matches, present its pre-synthesized content first — this is the fastest, highest-quality result. Label this section "From wiki:".
3. Grep `~/.claude/journal/` recursively for matching raw entries. Present as "From journal:" section.
4. Parse matches into structured results (date, category, title, content snippet).
5. Present results sorted by most recent first.
6. If > 10 results, show top 10 with "N more found — refine your search".
7. If 0 results, suggest: check spelling, try related terms.
8. **Graph-augmented search:** If `~/.claude/journal/knowledge-graph.json` exists, also run `python3 ~/.claude/hooks/build-knowledge-graph.py query "<search_term>"` via Bash and present connected entities as a "Related entities from knowledge graph:" section.
9. **Raw sources search:** If `~/.claude/sources/raw/` exists, also grep ingested source files for matches. Present as "From sources:" section.
10. **Index rebuild:** If `~/.claude/journal/index.md` is missing or older than 24 hours, rebuild it — scan all journal files, count entries by tag and category, list recent 7 days of activity.

## Tools

Grep, Read, Glob, Bash
