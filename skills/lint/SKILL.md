---
name: lint
description: "Health-check the wiki for staleness, orphans, contradictions, and missing pages. Usage: /lint"
---

## Behavior

1. Read `~/.claude/wiki/WIKI_SCHEMA.md` for conventions and lint rules.

2. **Stale check:** Glob all wiki pages in entities/, topics/, synthesis/. Parse YAML frontmatter for `last_updated`. Compare against dates of sources that mention any of the page's entities. Flag pages where newer sources exist than `last_updated`. Set `stale: true` in frontmatter.

3. **Orphan check:** Find wiki pages whose `sources` list in frontmatter is empty or whose referenced source files no longer exist.

4. **Missing pages:** Read `~/.claude/journal/knowledge-graph.json`. Find nodes with mentions >= 2 (or `wiki_entity_threshold` from config) that lack a corresponding wiki entity page in `~/.claude/wiki/entities/`.

5. **Index sync:** Compare `~/.claude/wiki/index.md` entries against actual wiki files on disk. Report any pages in index but missing on disk, or on disk but missing from index.

6. **Broken refs:** For each wiki page, verify all `[source: ...]` references and Source Log entries point to existing files in journal/ or sources/raw/.

7. Present a dashboard:
   ```
   Wiki Health Check
   =================
   Pages: N (entities: N, topics: N, synthesis: N)
   Healthy: N | Stale: N | Orphaned: N
   Missing entity pages: N (entities with >= 2 mentions but no wiki page)
   Broken source refs: N
   Index: in sync | N entries out of sync
   ```

8. Offer to auto-fix: create missing entity pages, update stale pages, rebuild index.

9. Append lint results to `~/.claude/wiki/log.md`.

## Tools

Read, Glob, Grep, Bash, Edit
