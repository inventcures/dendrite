---
name: kg
description: Build, query, and visualize the journal knowledge graph. Usage: /kg rebuild, /kg query "entity", /kg stats, /kg visualize
---

## Behavior

1. Route to the correct subcommand based on user input.
2. **Default (no args or "rebuild"):** Run `python3 ~/.claude/hooks/build-knowledge-graph.py rebuild` via Bash. Show the summary output.
3. **`query "entity"`:** Run `python3 ~/.claude/hooks/build-knowledge-graph.py query "<entity>"`. Present connections in a readable format.
4. **`stats`:** Run `python3 ~/.claude/hooks/build-knowledge-graph.py stats`.
5. **`visualize`:** Run `python3 ~/.claude/hooks/build-knowledge-graph.py visualize`. Output the Mermaid diagram in a code block. Accepts `--format dot` for Graphviz or `--format html` for interactive force-graph visualization.
6. Never modify journal entries or graph JSON directly — always use the script.
7. If the script fails, show the error and suggest checking gliner installation: `pip install gliner2`.
8. First run may take 10-30s for GLiNER model download.

## Tools

Bash, Read
