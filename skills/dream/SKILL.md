---
name: dream
description: "Speculative pattern completion — hypothesize connections not yet in the data. Usage: /dream or /dream \"topic\""
---

## Behavior

Like REM sleep, `/dream` makes creative leaps — connecting dots that aren't explicitly connected in the data.

1. Read `~/.claude/journal/knowledge-graph.json` for the full entity graph.
2. Read `~/.claude/wiki/index.md` and 3-5 wiki pages for context.
3. Read the most recent journal entries for current interests.

4. **Default (no args)**: Generate 3-5 **speculative hypotheses** based on the knowledge base:

   For each hypothesis:
   - Start from two entities that are NOT directly connected in the KG
   - Hypothesize HOW they might be connected based on external knowledge
   - Rate confidence: wild speculation / plausible / likely
   - Suggest how to validate (a search, a paper to read, a person to ask)

   ```
   ## Dreams — YYYY-MM-DD

   ### 1. MIRAGE + Drug Repurposing (plausible)
   If vision models hallucinate medical diagnoses, could they also hallucinate
   drug efficacy results? The same text-pattern-matching that produces phantom
   MRI reads could generate phantom clinical trial outcomes. This would affect
   Maor Shlomo's drug repurposing thesis directly.
   → Validate: search for "AI hallucination clinical trials" or "LLM drug discovery bias"

   ### 2. Cal Newport + Karpathy's LLM Wiki (likely)
   Newport argues AI offloading degrades cognition. But Karpathy's wiki pattern
   offloads BOOKKEEPING, not THINKING. The human still curates and questions.
   Is there a principled distinction between "good offloading" (bookkeeping)
   and "bad offloading" (reasoning)?
   → Validate: does Newport's "brain fry" study distinguish task types?

   ### 3. Organoids + Digital Twins + MIRAGE (wild speculation)
   What if we applied the MIRAGE methodology to drug testing on organoids?
   Test whether AI models predicting organoid drug responses are actually
   "seeing" the organoid data or pattern-matching from text descriptions.
   → Validate: search for "AI organoid drug response prediction benchmarks"
   ```

5. **With topic** (`/dream "cancer"`): Focus speculative connections on that topic.

6. Offer: "Want me to journal any of these hypotheses? Or create a synthesis page?"

## Tools

Read, Grep, Glob, Bash
