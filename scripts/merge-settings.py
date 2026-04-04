#!/usr/bin/env python3
"""Merge dendrite PostToolUse hook into Claude Code settings.json."""

import json
import sys
from pathlib import Path

HOOK_ENTRY = {
    "matcher": "Write|Edit",
    "hooks": [
        {
            "type": "command",
            "command": "python3 $HOME/.claude/hooks/kg-updater.py",
            "timeout": 2
        }
    ]
}


def main():
    if len(sys.argv) < 2:
        print("Usage: merge-settings.py <path-to-settings.json>", file=sys.stderr)
        sys.exit(1)

    settings_path = Path(sys.argv[1])

    if settings_path.exists():
        with open(settings_path) as f:
            settings = json.load(f)
    else:
        settings = {}

    hooks = settings.setdefault("hooks", {})
    post_tool_use = hooks.setdefault("PostToolUse", [])

    already_registered = any(
        any(
            "kg-updater" in h.get("command", "")
            for h in entry.get("hooks", [])
        )
        for entry in post_tool_use
    )

    if not already_registered:
        post_tool_use.append(HOOK_ENTRY)
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=2)


if __name__ == "__main__":
    main()
