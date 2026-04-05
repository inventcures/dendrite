# dendrite

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/inventcures/dendrite)

A CLI-first personal knowledge system for [Claude Code](https://claude.ai/code) — journal capture, ideas pipeline, knowledge graph with NER, and content review.

Named after the branching structures of neurons — because knowledge, like dendrites, grows by forming new connections.

## What it does

dendrite gives Claude Code 11 slash commands that turn it into a compounding knowledge companion:

| Command | Purpose |
|---------|---------|
| `/journal` | Capture learnings, decisions, patterns, and mistakes to a daily log |
| `/idea` | Quick-capture an idea to the inbox |
| `/ideas` | List and manage ideas through a kanban-style pipeline |
| `/recall` | Search across wiki, journal, KG, and raw sources (wiki-first) |
| `/kg` | Build, query, and visualize a knowledge graph from your entries |
| `/wiki` | Build, query, and edit the LLM-maintained wiki knowledge layer |
| `/ingest` | Batch-ingest tweets or articles into the knowledge system |
| `/lint` | Health-check the wiki for staleness, orphans, and contradictions |
| `/blog-review` | Review blog post drafts for clarity, structure, and voice |
| `/review-linkedin` | Review LinkedIn posts for engagement and formatting |
| `/intro` | Generate context-aware self-introductions |

## Architecture: Three Layers

Inspired by [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):

```
Raw Sources (tweets, articles, journal entries)
        |  /journal, /ingest
        v
  Wiki Layer (LLM-maintained entity/topic pages)
        |  /wiki build
        v
  Knowledge Graph (GLiNER2 NER + co-occurrence)
        |  /kg rebuild
        v
  knowledge-graph.json + interactive HTML visualization
```

The wiki is the key innovation: instead of re-deriving answers from scratch on every query, the LLM incrementally builds persistent, interlinked markdown pages. Knowledge compounds.

## How the knowledge graph works

```
Journal entries + raw sources (markdown)
        |
        v
  GLiNER2 NER extraction (or tag-only fallback)
        |
        v
  Co-occurrence graph (entities in same entry = connected)
        |
        v
  knowledge-graph.json + interactive HTML visualization
```

**Entity extraction tiers:**
- **Tier 0** (zero-install): Uses `#hashtag` tags as entities. Works with just Python 3.9+.
- **Tier 1** (`pip install gliner`): Automatic NER — extracts people, organizations, concepts, tools.
- **Tier 2** (`pip install gliner2`): Latest GLiNER2 architecture from Fastino. Best quality.

The knowledge graph auto-rebuilds in the background every time you use `/journal` or `/idea` via a PostToolUse hook.

## Install

### Option A: Clone and install

```bash
git clone https://github.com/inventcures/dendrite.git
cd dendrite
./install.sh

# Optional: for NER-powered entity extraction
pip install gliner2
```

### Option B: Manual

Copy `skills/` to `~/.claude/skills/`, `hooks/` to `~/.claude/hooks/`, and `templates/` contents to their respective `~/.claude/` locations.

## Uninstall

```bash
cd dendrite
./uninstall.sh
```

Your journal entries, ideas, wiki, sources, and personal data are **never** removed.

## Wiki Layer

The wiki is a collection of LLM-maintained markdown pages that compound knowledge over time:

```bash
/wiki build              # Seed wiki from existing KG + journal
/wiki query "topic"      # Search pre-synthesized wiki pages
/wiki edit stanford       # Re-synthesize an entity page from latest sources
/wiki status             # Show wiki health dashboard
/lint                    # Check for stale, orphaned, or missing pages
```

Wiki pages live in `~/.claude/wiki/entities/`, `topics/`, and `synthesis/`. The LLM writes and maintains them. You read and guide.

## Tweet Inbox

Batch-ingest tweets by adding links to `~/.claude/sources/tweets.md`:

```markdown
- [ ] https://x.com/karpathy/status/123456789
- [ ] https://x.com/someone/status/987654321
```

Then run `/ingest tweets`. Each tweet is fetched via fxtwitter, archived as an immutable raw source, journaled, and integrated into wiki entity pages.

You can also ingest articles: `/ingest article https://example.com/interesting-post`.

## Configuration

dendrite works out of the box with sensible defaults. To customize, create `~/.claude/dendrite.config.json`:

```json
{
  "entity_types": ["person", "organization", "tool/technology", "scientific_concept", "disease", "drug/molecule", "idea"],
  "gliner_model": "fastino/gliner2-base-v1",
  "gliner_threshold": 0.4,
  "auto_rebuild": true,
  "debounce_seconds": 5,
  "visualization_max_nodes": 50
}
```

### Domain presets

**Software engineering:**
```json
{ "entity_types": ["person", "organization", "technology", "programming_language", "framework", "pattern", "bug_type"] }
```

**Research:**
```json
{ "entity_types": ["person", "organization", "method", "dataset", "metric", "theory", "finding"] }
```

**Product management:**
```json
{ "entity_types": ["person", "organization", "product", "feature", "metric", "competitor", "market"] }
```

## Directory Structure

```
~/.claude/
  journal/           # Daily markdown files (YOUR data — never synced to this repo)
    SCHEMA.md        # Entry format template
    knowledge-graph.json
  ideas/             # Kanban pipeline (YOUR data)
    inbox/ developing/ parked/ done/
    PIPELINE.md
  personal/          # Bio and writing style (YOUR data)
  wiki/              # LLM-maintained knowledge pages (YOUR data)
    WIKI_SCHEMA.md   # Conventions doc
    index.md         # Content catalog
    log.md           # Activity log
    entities/        # One page per significant entity
    topics/          # Thematic synthesis
    synthesis/       # Cross-cutting analysis
  sources/           # Raw immutable source snapshots (YOUR data)
    tweets.md        # Twitter link inbox
    raw/             # Fetched tweet/article snapshots
  hooks/
    build-knowledge-graph.py   # KG builder (from dendrite)
    kg-updater.py              # Auto-rebuild hook (from dendrite)
  skills/
    journal/ idea/ ideas/ recall/ kg/
    wiki/ ingest/ lint/
    blog-review/ review-linkedin/ intro/
```

**Key design principle:** dendrite installs *code* (skills, hooks, templates). Your *data* (journal, ideas, wiki, sources, personal) stays completely private and is never part of this repo.

## Requirements

- Claude Code
- Python 3.9+
- GLiNER2 (optional, for NER): `pip install gliner2`

## License

MIT
