---
name: journal
description: Capture a learning, decision, pattern, or mistake to the daily journal. Usage: /journal "I learned that discriminated unions are better than type guards for exhaustive checking"
---

## Behavior

1. **Tweet URL transformation**: If the input contains a tweet URL matching `https://x.com/<user>/status/<id>` or `https://twitter.com/<user>/status/<id>`, rewrite it to `https://api.fxtwitter.com/<user>/status/<id>` and fetch the content via WebFetch before journaling. Store the original `x.com` URL as the Evidence link.
2. Parse the user's input (or fetched tweet content) to determine category: **learning**, **decision**, **pattern**, or **mistake**. Default to "learning" if ambiguous.
3. Read `~/.claude/journal/SCHEMA.md` for the entry format.
4. Get the current time via Bash: `date +%H:%M`.
5. Determine today's file path: `~/.claude/journal/YYYY/MM/YYYY-MM-DD.md`.
6. If the daily file doesn't exist, create it with the header `# Journal: YYYY-MM-DD` and all section headers (## Learnings, ## Decisions, ## Patterns, ## Mistakes, ## Auto-Extracted).
7. Append a structured entry under the correct `##` section using the current time (HH:MM).
8. Fill in all fields for the entry type from the schema.
9. Ask the user for tags if not obvious from context. Use inline `#hashtag` format.
10. Confirm what was written with the file path.

## Tools

Read, Write, Edit, Glob, Bash, WebFetch
