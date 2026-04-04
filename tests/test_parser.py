def test_find_journal_files(tmp_claude_home):
    import build_knowledge_graph as pkg

    files = pkg.find_journal_files()
    names = [f.name for f in files]
    assert "2026-01-15.md" in names
    assert "2026-01-16.md" in names
    assert "2026-01-17.md" in names
    assert "SCHEMA.md" not in names


def test_parse_journal_file(tmp_claude_home):
    import build_knowledge_graph as pkg

    filepath = tmp_claude_home / "journal" / "2026" / "01" / "2026-01-15.md"
    entries = pkg.parse_journal_file(filepath)
    assert len(entries) == 4
    assert entries[0].category == "learning"
    assert "rust" in entries[0].tags
    assert entries[0].date == "2026-01-15"
    assert entries[0].time == "10:30"


def test_parse_journal_skips_auto_extracted(tmp_claude_home):
    import build_knowledge_graph as pkg

    filepath = tmp_claude_home / "journal" / "2026" / "01" / "2026-01-15.md"
    entries = pkg.parse_journal_file(filepath)
    for entry in entries:
        assert "auto-generated" not in entry.body.lower()


def test_parse_idea_file(tmp_claude_home):
    import build_knowledge_graph as pkg

    filepath = tmp_claude_home / "ideas" / "inbox" / "2026-01-15-faster-ci-pipeline.md"
    entries = pkg.parse_idea_file(filepath)
    assert len(entries) == 1
    assert entries[0].category == "idea"
    assert entries[0].date == "2026-01-15"
    assert "ci-cd" in entries[0].tags


def test_parse_all_journals(tmp_claude_home):
    import build_knowledge_graph as pkg

    entries = pkg.parse_all_journals()
    assert len(entries) >= 7
