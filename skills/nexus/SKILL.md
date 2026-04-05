---
name: nexus
description: "Find bridge entities connecting otherwise separate knowledge clusters. Usage: /nexus or /nexus \"cluster1\" \"cluster2\""
---

## Behavior

1. Read `~/.claude/journal/knowledge-graph.json` for the full graph with clusters.
2. Read `~/.claude/wiki/index.md` for topic pages (each topic roughly maps to a cluster).

3. **Default (no args)**: Analyze all clusters and find bridge entities:
   - For each entity, count how many distinct clusters it has connections into
   - Entities connected to 2+ clusters are **nexus points**
   - Rank by cross-cluster connection count

4. **With args** (`/nexus "medical AI" "cancer investment"`): Find specific bridges between two named clusters/topics:
   - Identify entities in both clusters
   - Find shortest paths between cluster hubs through the KG
   - Highlight entities that sit at the intersection

5. Present findings:
   ```
   ## Nexus Points

   ### AI Safety ↔ Cancer Investment
   Bridge: **AI** — appears in MIRAGE cluster (AI enables hallucination) AND cancer cluster (AI accelerates clinical trials)
   Implication: The same AI that hallucinates medical diagnoses is being deployed to accelerate cancer drug discovery. Safety concern?

   ### Cancer Investment ↔ Twitter API
   Bridge: None found — these clusters are disconnected.

   ### Strength Rankings
   1. AI (connects 2 clusters, 5 cross-links)
   2. Stanford (connects MIRAGE + could connect to cancer research)
   ```

6. For each nexus point, suggest: "Create a synthesis page exploring this bridge?"

## Tools

Read, Bash, Grep
