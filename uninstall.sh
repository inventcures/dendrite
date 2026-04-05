#!/usr/bin/env bash
set -euo pipefail

CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"

echo "Uninstalling dendrite from $CLAUDE_HOME ..."
echo "(Journal, ideas, and personal data are NEVER removed)"
echo ""

for skill in journal idea ideas recall kg wiki ingest lint blog-review review-linkedin intro; do
  if [ -d "$CLAUDE_HOME/skills/$skill" ]; then
    rm -rf "$CLAUDE_HOME/skills/$skill"
    echo "  Removed skill: /$skill"
  fi
done

for hook in build-knowledge-graph.py kg-updater.py; do
  if [ -f "$CLAUDE_HOME/hooks/$hook" ]; then
    rm "$CLAUDE_HOME/hooks/$hook"
    echo "  Removed hook: $hook"
  fi
done

if [ -f "$CLAUDE_HOME/dendrite.config.json" ]; then
  rm "$CLAUDE_HOME/dendrite.config.json"
  echo "  Removed dendrite.config.json"
fi

echo ""
echo "Done! Skills and hooks removed."
echo "Your data is safe: journal/, ideas/, personal/, wiki/, and sources/ were not touched."
