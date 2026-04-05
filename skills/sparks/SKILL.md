---
name: sparks
description: "Quick rapid-fire insights from recent journal entries and wiki state. Usage: /sparks"
---

## Behavior

1. Read the most recent journal file(s) — today's and yesterday's entries from `~/.claude/journal/`.
2. Read `~/.claude/wiki/index.md` for wiki context.
3. Read `~/.claude/journal/knowledge-graph.json` for entity connections.

4. Generate 5-10 **one-liner insights**, each a single punchy sentence. Types of sparks:

   - **Connection spark**: "X and Y both appeared today but from completely different contexts — worth exploring?"
   - **Contradiction spark**: "Your journal says A, but earlier you noted B — which is right?"
   - **Pattern spark**: "This is the 3rd time you've journaled about [topic] this week."
   - **Gap spark**: "You captured [entity] but never asked: [obvious follow-up question]."
   - **Action spark**: "Based on today's entries, you might want to [concrete next step]."
   - **Serendipity spark**: "Interesting that [entity from cluster A] and [entity from cluster B] share [unexpected property]."

5. Format as a numbered list, each spark on one line. No headers, no sections — just rapid fire:
   ```
   1. Stanford appears in both MIRAGE (AI safety) and cancer investment — Fei-Fei Li's lab does both.
   2. You've journaled 3 AI safety entries but 0 action items — what are you going to DO with this?
   3. Cal Newport says "your writing should be your own" — ironic that an LLM journaled this for you.
   ...
   ```

6. Keep it provocative, not polite. Sparks should make the user think, not just nod.

## Tools

Read, Glob, Grep
