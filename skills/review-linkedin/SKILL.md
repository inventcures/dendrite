---
name: review-linkedin
description: Review a LinkedIn post for spelling, engagement, and formatting. Usage: /review-linkedin "paste your post here" or /review-linkedin path/to/post.md
---

## Behavior

1. Accept text input (pasted inline or a file path).
2. Check against these criteria:
   - **Spelling/grammar**: Flag all errors.
   - **Hook**: First 2 lines (visible before "...see more") — are they compelling enough to click?
   - **Formatting**: Line breaks for mobile readability.
   - **Length**: Optimal 1200-1500 characters. Flag if significantly too short or too long.
   - **Value density**: Every paragraph should deliver insight, not filler.
   - **CTA**: Does it end with an engagement prompt (question, ask)?
   - **Hashtags**: Relevant, 3-5 max, not excessive.
3. Output: the original with inline annotations highlighting issues, followed by a suggested revision.
4. Show character count and estimated read time.

## Tools

Read
