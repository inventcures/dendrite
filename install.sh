#!/usr/bin/env bash
set -euo pipefail

CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing dendrite to $CLAUDE_HOME ..."

mkdir -p "$CLAUDE_HOME/journal"
mkdir -p "$CLAUDE_HOME/ideas"/{inbox,developing,parked,done}
mkdir -p "$CLAUDE_HOME/personal"
mkdir -p "$CLAUDE_HOME/hooks"
mkdir -p "$CLAUDE_HOME/wiki/entities"
mkdir -p "$CLAUDE_HOME/wiki/topics"
mkdir -p "$CLAUDE_HOME/wiki/synthesis"
mkdir -p "$CLAUDE_HOME/sources/raw"

for template in journal/SCHEMA.md ideas/PIPELINE.md personal/bio.md personal/writing-style.md wiki/WIKI_SCHEMA.md sources/tweets-inbox.md; do
  base=$(basename "$template")
  dir=$(dirname "$template")
  if [ "$base" = "tweets-inbox.md" ]; then
    dest="$CLAUDE_HOME/sources/tweets.md"
  else
    dest="$CLAUDE_HOME/$template"
  fi
  mkdir -p "$(dirname "$dest")"
  if [ ! -f "$dest" ]; then
    cp "$REPO_DIR/templates/$template" "$dest"
    echo "  Created $(basename "$dest")"
  else
    echo "  Skipped $(basename "$dest") (already exists)"
  fi
done

for skill_dir in "$REPO_DIR"/skills/*/; do
  skill_name=$(basename "$skill_dir")
  mkdir -p "$CLAUDE_HOME/skills/$skill_name"
  cp "$skill_dir"SKILL.md "$CLAUDE_HOME/skills/$skill_name/SKILL.md"
  echo "  Installed skill: /$skill_name"
done

cp "$REPO_DIR/hooks/build-knowledge-graph.py" "$CLAUDE_HOME/hooks/"
cp "$REPO_DIR/hooks/kg-updater.py" "$CLAUDE_HOME/hooks/"
chmod +x "$CLAUDE_HOME/hooks/build-knowledge-graph.py"
chmod +x "$CLAUDE_HOME/hooks/kg-updater.py"
echo "  Installed hooks"

if [ ! -f "$CLAUDE_HOME/dendrite.config.json" ]; then
  cp "$REPO_DIR/dendrite.config.json" "$CLAUDE_HOME/"
  echo "  Created dendrite.config.json"
fi

python3 "$REPO_DIR/scripts/merge-settings.py" "$CLAUDE_HOME/settings.json"
echo "  Registered PostToolUse hook in settings.json"

echo ""
echo "Done! dendrite installed to $CLAUDE_HOME"
echo ""
echo "Available commands:"
echo "  /journal  — capture learnings, decisions, patterns, mistakes"
echo "  /idea     — quick-capture an idea"
echo "  /ideas    — manage ideas pipeline"
echo "  /recall   — search past learnings (wiki-first)"
echo "  /kg       — build/query/visualize knowledge graph"
echo "  /wiki     — build/query/edit the wiki knowledge layer"
echo "  /ingest   — batch-ingest tweets or articles"
echo "  /lint     — health-check the wiki"
echo "  /blog-review    — review blog drafts"
echo "  /review-linkedin — review LinkedIn posts"
echo "  /intro    — generate context-aware introductions"
echo ""
echo "Optional: pip install gliner2  # for NER-powered entity extraction"
