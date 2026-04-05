# Wiki Schema

This document defines the conventions for maintaining the dendrite wiki.
The wiki is an LLM-generated and LLM-maintained knowledge layer.
Humans read and guide; the LLM owns the content.

## Principles

1. **Sources are immutable** — never modify files in `~/.claude/sources/raw/`
2. **Wiki pages are living documents** — update them as new information arrives
3. **Every claim traces to a source** — use `[source: YYYY-MM-DD journal]` or `[source: tweet-<id>]`
4. **Contradictions are explicit** — when sources disagree, document both views
5. **Staleness is tracked** — frontmatter `last_updated` enables lint checks

## Page Types

### Entity Pages (`wiki/entities/<slug>.md`)
- One page per KG node that crosses significance threshold (>= 2 mentions OR manually requested)
- Frontmatter: type, entity_type, aliases, first_seen, last_updated, sources, tags, stale
- Sections: Summary, Key Facts, Connections, Timeline, Source Log, Open Questions

### Topic Pages (`wiki/topics/<slug>.md`)
- Synthesize across multiple entities and sources around a theme
- Created when a KG cluster has 3+ entities or user requests synthesis
- Frontmatter: type, entities (list), last_updated, sources, tags, stale
- Sections: Overview, Key Findings, Timeline, Entities Involved, Sources, Open Questions

### Synthesis Pages (`wiki/synthesis/<slug>.md`)
- Cross-cutting analysis spanning multiple topics
- Created during lint (contradictions found) or on user request
- Sections: Thesis, Evidence For, Evidence Against, Sources, Conclusion, Last Reviewed

## Frontmatter Format

```yaml
---
title: <display name>
type: entity | topic | synthesis
slug: <url-safe identifier>
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
sources: [list of source references]
tags: [list of tags]
stale: false
---
```

## index.md Format

```
# Wiki Index

Last rebuilt: YYYY-MM-DD HH:MM
Pages: N | Entities: N | Topics: N | Synthesis: N

## Entities
- [Entity Name](entities/slug.md) — one-line summary (N sources, updated YYYY-MM-DD)

## Topics
- [Topic Name](topics/slug.md) — one-line summary (N sources, updated YYYY-MM-DD)

## Synthesis
- [Title](synthesis/slug.md) — one-line summary (last reviewed YYYY-MM-DD)
```

## log.md Format

```
# Wiki Activity Log

### YYYY-MM-DD HH:MM — <operation type>
- Action: <what happened>
- Pages affected: [list]
- Sources processed: [list]
```

## Update Rules

1. On **ingest**: read source, extract entities/facts, create or update entity pages, update topic pages if relevant, append to log.md, rebuild index.md
2. On **journal write**: if new entry mentions entities with wiki pages, those pages become potentially stale
3. On **lint**: check all pages for staleness (>7 days since source with newer data), orphans (no sources), contradictions, missing pages
4. On **query**: search wiki pages first (pre-synthesized), fall back to raw journal/source grep
