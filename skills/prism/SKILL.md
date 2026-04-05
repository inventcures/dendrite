---
name: prism
description: "Reframe an entity or topic from multiple disciplinary angles. Usage: /prism \"stanford\" or /prism \"AI safety\""
---

## Behavior

1. Accept an entity or topic name as argument.
2. Read the wiki page for this entity/topic (if exists).
3. Read all journal entries and sources mentioning it.
4. Read KG connections for this entity.

5. Generate **3-5 distinct lenses** through which to view this entity/topic. Each lens reframes the subject from a different disciplinary or stakeholder perspective:

   Example for "AI Safety":
   ```
   ## Prism: AI Safety

   ### Lens 1: Clinical — The Patient Perspective
   AI hallucination means a patient could receive a false diagnosis (STEMI, melanoma)
   from a model that never actually saw their scan. Life-or-death stakes.

   ### Lens 2: Epistemological — What Counts as "Seeing"?
   MIRAGE reveals that 74-77% of vision benchmarks don't test vision. This isn't
   just a model problem — it's a measurement problem. How do we know what AI knows?

   ### Lens 3: Economic — The Productivity Trap
   Newport's "brain fry": AI makes workers less capable over time, but companies
   mandate its use. A tragedy of the commons for cognitive capital.

   ### Lens 4: Regulatory — Who's Responsible?
   Australia banned social media for under-16s. Should medical AI face similar
   gating? Who's liable when a hallucinated diagnosis causes harm?

   ### Lens 5: Personal — Your Own Practice
   You're building an LLM-maintained wiki right now. Are you offloading thinking
   or augmenting it? Where's your line?
   ```

6. Each lens should be 2-3 sentences, provocative, and grounded in actual sources from the wiki/journal.
7. Offer: "Want me to create a synthesis page exploring any of these angles?"

## Tools

Read, Grep, Glob
