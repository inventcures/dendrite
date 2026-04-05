---
name: discover
description: "Surface hidden connections, contradictions, and gaps across the wiki and knowledge graph. Usage: /discover"
---

## Behavior

1. Read `~/.claude/journal/knowledge-graph.json` for the full entity graph.
2. Read `~/.claude/wiki/index.md` for the current wiki state.
3. Perform these analyses:

**Cross-cluster bridges**: Find entities that appear in multiple KG clusters or have connections spanning different topic pages. These are hidden links between seemingly unrelated domains.

**Contradictions**: Scan wiki entity pages for claims that conflict with each other. Look for the same entity described differently in different sources (e.g., "GPT-5.2 refuses to hallucinate" vs "GPT-5.2 hallucinated a brain MRI").

**Gaps**: Find KG nodes with high connection counts but no wiki page. Find wiki pages with thin Source Logs (only 1 source). Find topics where Open Questions have been sitting unanswered.

**Emerging themes**: Look for tags or entities that appear across 3+ unrelated journal entries — these may deserve a new topic page.

**Surprising co-occurrences**: Find entity pairs that co-occur but haven't been explicitly connected in any wiki page's Connections table.

4. Present findings as a structured report:
   ```
   ## Discoveries

   ### Cross-Cluster Bridges
   - [entity] connects [cluster A] to [cluster B] via [relationship]

   ### Contradictions
   - [page A] says X, but [page B] says Y

   ### Gaps to Fill
   - [entity] has N connections but no wiki page
   - [topic page] has only 1 source — needs enrichment

   ### Emerging Themes
   - [theme] appears across N entries — consider creating a topic page

   ### Surprising Connections
   - [entity A] and [entity B] co-occur but aren't linked in the wiki
   ```

5. Offer to act on any discovery: create missing pages, create synthesis pages for contradictions, create topic pages for emerging themes.

## Tools

Read, Grep, Glob, Bash
