---
name: distill
description: "Compress a wiki page, topic, or theme into a tight briefing. Usage: /distill \"medical AI\" or /distill entities/stanford.md"
---

## Behavior

1. Accept a wiki page path, entity slug, topic name, or free-text theme.
2. Find the relevant wiki page(s) and/or journal entries.
3. Read all matching content.

4. Produce a **distilled briefing** in exactly this format:

   ```
   ## Distill: [Subject]

   **One sentence**: [The single most important thing to know]

   **Three facts**:
   1. [Fact with source attribution]
   2. [Fact with source attribution]
   3. [Fact with source attribution]

   **The tension**: [The core contradiction or unresolved question]

   **So what?**: [Why this matters to you specifically, based on your journal context]

   **Next move**: [One concrete action you could take]
   ```

5. The distillation should be ruthlessly concise — if it takes more than 30 seconds to read, it's too long.
6. Every claim must trace to a source.
7. "The tension" is the most important part — it should highlight what's unresolved or contradictory.

## Tools

Read, Grep, Glob
