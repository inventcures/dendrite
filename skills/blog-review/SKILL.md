---
name: blog-review
description: Review a blog post draft for clarity, structure, and engagement. Usage: /blog-review path/to/draft.md
---

## Behavior

1. Read the draft file path provided by the user (or accept pasted text).
2. If `~/.claude/personal/writing-style.md` exists and has content beyond the template placeholders, read it for voice calibration.
3. Evaluate against these criteria, rating each as **Strong** / **Needs Work** / **Weak**:
   - **Structure**: Hook → body → conclusion flow
   - **Clarity**: Jargon density, sentence complexity, paragraph length
   - **Technical accuracy**: Claims backed by evidence
   - **Engagement**: Opening hook strength, call-to-action, takeaway clarity
   - **Voice consistency**: Does it match the user's documented writing style?
4. Output structured feedback with specific line-level suggestions.
5. Offer to produce a revised version if requested.

## Tools

Read, Write, Edit
