def test_normalize_entity_key(tmp_claude_home):
    import build_knowledge_graph as pkg

    assert pkg.normalize_entity_key("AlphaGenome") == "alphagenome"
    assert pkg.normalize_entity_key("Deep Learning") == "deep-learning"
    assert pkg.normalize_entity_key("  Rust  ") == "rust"
    assert pkg.normalize_entity_key("N+1 queries") == "n1-queries"


def test_extract_entities_tags_only(tmp_claude_home):
    import build_knowledge_graph as pkg

    filepath = tmp_claude_home / "journal" / "2026" / "01" / "2026-01-15.md"
    entries = pkg.parse_journal_file(filepath)
    entities = pkg.extract_entities_tags_only(entries[0])
    keys = [e.text for e in entities]
    assert "rust" in keys
    assert "memory-safety" in keys
    assert "borrow-checker" in keys
