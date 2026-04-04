#!/usr/bin/env python3
"""
KG Updater — PostToolUse hook
Triggers incremental KG update when journal/idea files are written or edited.
Non-blocking: spawns background process, returns {} immediately.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

CLAUDE_HOME = Path(os.getenv("CLAUDE_HOME", Path.home() / ".claude"))
JOURNAL_DIR = str(CLAUDE_HOME / "journal")
IDEAS_DIR = str(CLAUDE_HOME / "ideas")
SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPT = str(SCRIPT_DIR / "build-knowledge-graph.py")
LOG_FILE = str(SCRIPT_DIR / "kg-updater.log")
DEBOUNCE_DIR = SCRIPT_DIR / ".kg-debounce"

EXCLUDE_FILES = {
    "SCHEMA.md", "index.md", "PIPELINE.md",
    "knowledge-graph-summary.md", "knowledge-graph.json",
    ".gitkeep",
}

MATCH_TOOLS = {"Write", "Edit"}


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        print("{}")
        return

    tool_name = hook_input.get("tool_name", "")
    if tool_name not in MATCH_TOOLS:
        print("{}")
        return

    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if not should_update(file_path):
        print("{}")
        return

    if is_debounced(file_path):
        print("{}")
        return

    spawn_update(file_path)
    print("{}")


def should_update(file_path: str) -> bool:
    if not file_path or not file_path.endswith(".md"):
        return False
    basename = os.path.basename(file_path)
    if basename in EXCLUDE_FILES:
        return False
    return file_path.startswith(JOURNAL_DIR) or file_path.startswith(IDEAS_DIR)


def is_debounced(file_path: str, window: int = 5) -> bool:
    DEBOUNCE_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = file_path.replace("/", "_")
    marker = DEBOUNCE_DIR / safe_name
    if marker.exists():
        age = time.time() - marker.stat().st_mtime
        if age < window:
            return True
    marker.touch()
    return False


def spawn_update(file_path: str):
    try:
        log_fd = open(LOG_FILE, "a")
        subprocess.Popen(
            [sys.executable, SCRIPT, "incremental", "--file", file_path],
            stdout=subprocess.DEVNULL,
            stderr=log_fd,
            start_new_session=True,
        )
    except Exception:
        pass


if __name__ == "__main__":
    main()
