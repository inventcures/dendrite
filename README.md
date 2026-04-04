# dendrite

A CLI-first personal knowledge system for [Claude Code](https://claude.ai/code) — journal capture, ideas pipeline, knowledge graph with NER, and content review.

Named after the branching structures of neurons — because knowledge, like dendrites, grows by forming new connections.

## What it does

dendrite gives Claude Code 8 slash commands that turn it into a compounding knowledge companion:

| Command | Purpose |
|---------|---------|
| `/journal` | Capture learnings, decisions, patterns, and mistakes to a daily log |
| `/idea` | Quick-capture an idea to the inbox |
| `/ideas` | List and manage ideas through a kanban-style pipeline |
| `/recall` | Search past journal entries with graph-augmented results |
| `/kg` | Build, query, and visualize a knowledge graph from your entries |
| `/blog-review` | Review blog post drafts for clarity, structure, and voice |
| `/review-linkedin` | Review LinkedIn posts for engagement and formatting |
| `/intro` | Generate context-aware self-introductions |

## How the knowledge graph works

```
Journal entries (markdown)
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

Your journal entries, ideas, and personal data are **never** removed.

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

## Architecture

```
~/.claude/
  journal/           # Daily markdown files (YOUR data — never synced to this repo)
    SCHEMA.md        # Entry format template
    knowledge-graph.json
  ideas/             # Kanban pipeline (YOUR data)
    inbox/ developing/ parked/ done/
    PIPELINE.md
  personal/          # Bio and writing style (YOUR data)
  hooks/
    build-knowledge-graph.py   # KG builder (from dendrite)
    kg-updater.py              # Auto-rebuild hook (from dendrite)
  skills/
    journal/ idea/ ideas/ recall/ kg/
    blog-review/ review-linkedin/ intro/
```

**Key design principle:** dendrite installs *code* (skills, hooks). Your *data* (journal entries, ideas, personal info) stays completely private and is never part of this repo.

## Tweet ingestion

The `/journal` command auto-transforms Twitter/X URLs:

```
/journal https://x.com/someone/status/123456789
```

This rewrites the URL to `api.fxtwitter.com` for fetching (X blocks direct access), then journals the tweet content with the original URL as evidence.

## Requirements

- Claude Code
- Python 3.9+
- GLiNER2 (optional, for NER): `pip install gliner2`

## License

MIT
