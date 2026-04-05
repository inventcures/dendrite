# Changelog

## 0.2.0 (2026-04-05)

LLM Wiki pattern + Tweet Inbox (inspired by Karpathy's LLM Wiki gist).

- Wiki layer: /wiki build, /wiki query, /wiki edit, /wiki status, /wiki create
- Tweet inbox: batch ingestion via /ingest tweets with fxtwitter proxy
- Article ingestion: /ingest article <url>
- Wiki health checks: /lint (staleness, orphans, contradictions, missing pages)
- Enhanced /recall: wiki-first search across all layers
- Enhanced /journal: wiki staleness flagging on new entries
- Source layer: immutable raw sources in sources/raw/
- Wiki schema: WIKI_SCHEMA.md conventions doc, entity/topic/synthesis templates
- Activity tracking: index.md catalog + log.md chronological log
- KG builder: now parses raw source files alongside journal + ideas
- KG updater hook: now monitors sources/ directory, excludes wiki/ to prevent loops
- Config: wiki_entity_threshold, wiki_stale_days, tweet_fetch_delay_ms

## 0.1.0 (2026-04-04)

Initial open-source release.

- 8 slash commands: /journal, /idea, /ideas, /recall, /kg, /blog-review, /review-linkedin, /intro
- Knowledge graph builder with GLiNER2 NER extraction
- Co-occurrence graph with Mermaid, DOT, and HTML visualization
- PostToolUse auto-rebuild hook
- Tweet URL auto-transformation via fxtwitter
- Configurable entity types via dendrite.config.json
- install.sh / uninstall.sh for easy setup
