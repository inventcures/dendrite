import importlib
import os
import shutil
import sys
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
HOOKS_DIR = Path(__file__).parent.parent / "hooks"


@pytest.fixture(autouse=True)
def _setup_imports():
    """Make hooks importable despite hyphens in filenames."""
    sys.path.insert(0, str(HOOKS_DIR))
    # Create importable aliases for hyphenated filenames
    import importlib.util
    for name, filename in [
        ("build_knowledge_graph", "build-knowledge-graph.py"),
        ("kg_updater", "kg-updater.py"),
    ]:
        if name not in sys.modules:
            spec = importlib.util.spec_from_file_location(name, HOOKS_DIR / filename)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                sys.modules[name] = mod
                spec.loader.exec_module(mod)
    yield


@pytest.fixture
def tmp_claude_home(tmp_path):
    """Create a temporary CLAUDE_HOME with test fixtures."""
    home = tmp_path / ".claude"
    shutil.copytree(FIXTURES_DIR / "journal", home / "journal")
    shutil.copytree(FIXTURES_DIR / "ideas", home / "ideas")
    os.environ["CLAUDE_HOME"] = str(home)

    # Reload modules to pick up new CLAUDE_HOME
    for mod_name in ("build_knowledge_graph", "kg_updater"):
        if mod_name in sys.modules:
            del sys.modules[mod_name]

    import importlib.util
    for name, filename in [
        ("build_knowledge_graph", "build-knowledge-graph.py"),
        ("kg_updater", "kg-updater.py"),
    ]:
        spec = importlib.util.spec_from_file_location(name, HOOKS_DIR / filename)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            spec.loader.exec_module(mod)

    yield home
    os.environ.pop("CLAUDE_HOME", None)
