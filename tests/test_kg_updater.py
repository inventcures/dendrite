def test_should_update_journal(tmp_claude_home):
    import kg_updater

    journal_path = str(tmp_claude_home / "journal" / "2026" / "01" / "2026-01-15.md")
    assert kg_updater.should_update(journal_path) is True


def test_should_update_rejects_schema(tmp_claude_home):
    import kg_updater

    schema_path = str(tmp_claude_home / "journal" / "SCHEMA.md")
    assert kg_updater.should_update(schema_path) is False


def test_should_update_rejects_non_md(tmp_claude_home):
    import kg_updater

    assert kg_updater.should_update("/some/path/file.py") is False


def test_should_update_rejects_unrelated_path(tmp_claude_home):
    import kg_updater

    assert kg_updater.should_update("/tmp/random/file.md") is False
