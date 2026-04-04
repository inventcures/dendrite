def test_build_graph_tags_only(tmp_claude_home):
    import build_knowledge_graph as pkg

    entries = pkg.parse_all_journals()
    graph = pkg.build_graph(entries, model=None, version=None)

    assert graph["graph"]["entity_count"] > 0
    assert graph["graph"]["edge_count"] > 0
    assert graph["graph"]["gliner_available"] is False

    node_ids = {n["id"] for n in graph["nodes"]}
    assert "rust" in node_ids
    assert "postgresql" in node_ids


def test_graph_has_co_occurrence_edges(tmp_claude_home):
    import build_knowledge_graph as pkg

    entries = pkg.parse_all_journals()
    graph = pkg.build_graph(entries, model=None, version=None)

    edge_pairs = set()
    for l in graph["links"]:
        edge_pairs.add((l["source"], l["target"]))
    assert ("borrow-checker", "rust") in edge_pairs or ("rust", "borrow-checker") in edge_pairs


def test_merge_into_graph(tmp_claude_home):
    import build_knowledge_graph as pkg

    entries = pkg.parse_all_journals()
    graph = pkg.build_graph(entries, model=None, version=None)
    original_count = graph["graph"]["entity_count"]

    filepath = tmp_claude_home / "journal" / "2026" / "01" / "2026-01-15.md"
    file_entries = pkg.parse_journal_file(filepath)
    merged = pkg.merge_into_graph(graph, file_entries, None, None, str(filepath))

    assert merged["graph"]["entity_count"] <= original_count
