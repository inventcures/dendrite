# Contributing to dendrite

## Adding a new entity type

Edit `dendrite.config.json` and add your type to the `entity_types` array. GLiNER supports zero-shot extraction for any entity type described in natural language.

## Adding a new skill

1. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`) and behavior instructions.
2. List the tools the skill needs.
3. Test by running `/<name>` in Claude Code.

## Running tests

```bash
cd tests
python3 -m pytest -v
```

GLiNER tests are skipped if GLiNER is not installed.

## Code style

- Python 3.9+ compatible (use `from __future__ import annotations`)
- No external dependencies in core scripts (GLiNER is optional)
- Skills are markdown — keep instructions clear and concise
