---
name: wiki
description: "Build, query, edit, and manage the wiki knowledge layer. Usage: /wiki build, /wiki query \"topic\", /wiki edit <slug>, /wiki status"
---

## Behavior

1. Route to subcommand based on user input.

2. **`build`** — Seed/rebuild wiki from existing KG + journal:
   - Read `~/.claude/wiki/WIKI_SCHEMA.md` for conventions.
   - Read `~/.claude/journal/knowledge-graph.json` for entities and connections.
   - For each KG node with mentions >= 2 (or `wiki_entity_threshold` from `~/.claude/dendrite.config.json`):
     - Read all source entries referenced in the node's `entries` array.
     - If entity page exists in `~/.claude/wiki/entities/<slug>.md`, update it. Otherwise create from template.
     - Populate: Summary (synthesize from sources), Key Facts, Connections (from KG edges), Timeline (from entry dates), Source Log.
   - Identify KG clusters with 3+ entities — create topic pages in `~/.claude/wiki/topics/`.
   - Rebuild `~/.claude/wiki/index.md` — catalog all pages with one-line summaries.
   - Append build event to `~/.claude/wiki/log.md`.
   - Report: "Seeded N entity pages, M topic pages from KG with X entities."

3. **`query "term"`** — Wiki-first search:
   - Grep `~/.claude/wiki/` for matching page titles, frontmatter tags, and content.
   - If found: present the pre-synthesized content from matching wiki pages.
   - If not found: fall back to journal grep + KG query (like /recall).
   - Offer to create a new wiki page if enough source material found.

4. **`edit <slug>`** — Re-synthesize a wiki page:
   - Read the existing page at `~/.claude/wiki/entities/<slug>.md` (or topics/, synthesis/).
   - Read all sources referenced in its Source Log section.
   - Also grep journal + sources/raw for any NEW mentions of this entity not yet in the page.
   - Re-synthesize Summary and Key Facts with all sources.
   - Update frontmatter: `last_updated` to today, `stale: false`.
   - Append edit event to `~/.claude/wiki/log.md`.

5. **`status`** — Show wiki dashboard:
   - Read `~/.claude/wiki/index.md` for page counts.
   - Glob wiki directories, count pages by type.
   - Count pages with `stale: true` in frontmatter.
   - Show: total pages, by type, stale count, last build time.

6. **`create entity|topic|synthesis "title"`** — Create a new wiki page:
   - Use the appropriate template from `~/.claude/wiki/WIKI_SCHEMA.md`.
   - Gather relevant sources by grepping journal + sources/raw for the title/topic.
   - Populate initial content from found sources.
   - Add to `~/.claude/wiki/index.md`, append to `~/.claude/wiki/log.md`.

7. After ANY write operation: always update `~/.claude/wiki/index.md` and append to `~/.claude/wiki/log.md`.

## Tools

Read, Write, Edit, Glob, Grep, Bash
