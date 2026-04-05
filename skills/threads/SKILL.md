---
name: threads
description: "Trace a specific theme across all sources chronologically. Usage: /threads \"ai safety\" or /threads \"cancer\""
---

## Behavior

1. Accept a theme/topic as argument.
2. Search across ALL layers chronologically:
   - Grep `~/.claude/wiki/` for matching pages (titles, tags, content)
   - Grep `~/.claude/journal/` for matching entries
   - Grep `~/.claude/sources/raw/` for matching raw sources
   - Query KG: `python3 ~/.claude/hooks/build-knowledge-graph.py query "<theme>"` via Bash

3. Assemble a **chronological thread** — every mention of this theme across all sources, ordered by date:
   ```
   ## Thread: "ai safety"

   ### 2026-04-04 05:29 — Journal
   Maor Shlomo investing in cancer research — AI mentioned as clinical trial accelerator
   → Tangential: AI as tool, not safety concern here

   ### 2026-04-04 08:38 — Journal
   MIRAGE paper: vision models hallucinate without images
   → Core: AI safety in medical imaging

   ### 2026-04-04 08:40 — Journal
   GPT-5.2 phantom MRI: confirmed MIRAGE effect live
   → Confirmation: hallucination is real and dangerous

   ### 2026-04-05 23:14 — Journal
   Cal Newport: AI "workslop" degrades cognitive fitness
   → New angle: AI safety for human cognition, not just model outputs

   ### Wiki pages touching this thread:
   - entities/ai-safety.md (3 sources)
   - topics/medical-ai-hallucination.md
   - topics/cognitive-fitness-revolution.md

   ### KG connections:
   ai-safety → hallucination, vision-models, mirage, stanford, medical-ai, ...
   ```

4. At the end, offer: "Want me to create a synthesis page for this thread?"

## Tools

Read, Grep, Glob, Bash
