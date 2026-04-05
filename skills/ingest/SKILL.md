---
name: ingest
description: "Ingest sources into the knowledge system. Usage: /ingest tweets, /ingest article <url>"
---

## Behavior

1. Route based on first argument.

2. **`tweets`** — Batch-process the Twitter link inbox:
   - Read `~/.claude/sources/tweets.md`. If it doesn't exist, create it from the template with header and instructions.
   - Find all unchecked links: lines matching `- [ ] https://x.com/` or `- [ ] https://twitter.com/`.
   - For each unprocessed link (sequentially, wait 1 second between fetches):
     a. Transform URL: replace `x.com` or `twitter.com` with `api.fxtwitter.com`.
     b. Fetch via WebFetch. Extract full tweet text, author, date, media, engagement stats.
     c. **On success:**
        - Write raw source to `~/.claude/sources/raw/tweet-<status_id>.md` with YAML frontmatter (type: tweet, source_url, author, date, fetched timestamp, immutable: true) and full tweet text body. This file is IMMUTABLE — never modify after creation.
        - Create a journal entry in today's journal file (same format as /journal — `### HH:MM | [learning] Title` with Context, Insight, Evidence, Tags).
        - If `~/.claude/wiki/entities/` exists, extract entities from tweet content and update/create wiki entity pages for significant entities.
        - Mark the checkbox in tweets.md: change `- [ ]` to `- [x]` and append `<!-- ingested YYYY-MM-DD -->`.
     d. **On failure (404, timeout, etc.):**
        - Mark: change `- [ ]` to `- [!]` and append `<!-- fetch failed YYYY-MM-DD: <reason> -->`.
        - Continue to next link.
   - After all links processed: rebuild `~/.claude/wiki/index.md` if wiki exists, append batch summary to `~/.claude/wiki/log.md`.
   - Report: "Ingested N tweets, created M new wiki pages, updated K existing pages, L failures."

3. **`article <url>`** — Ingest a single web article:
   - Fetch the URL via WebFetch. Extract title, author, date, and body text.
   - Generate a slug from the title: `article-YYYY-MM-DD-slugified-title.md`.
   - Write raw source to `~/.claude/sources/raw/<slug>.md` with frontmatter (type: article, source_url, title, author, date, fetched, immutable: true).
   - Create a journal entry summarizing the article.
   - Update wiki entity pages for extracted entities.
   - Update wiki index and log.

4. **Rules:**
   - Never modify files in `~/.claude/sources/raw/` after initial creation — sources are immutable.
   - Always create the raw source file BEFORE updating wiki pages (source of truth first).
   - For tweet ingestion, wait 1 second between fetches to be polite to the fxtwitter Cloudflare Worker.
   - Store the original `x.com` URL as the Evidence link in journal entries, not the fxtwitter URL.

## Tools

Read, Write, Edit, Glob, Bash, WebFetch
