def test_to_mermaid(tmp_claude_home):
    import build_knowledge_graph as pkg

    entries = pkg.parse_all_journals()
    graph = pkg.build_graph(entries, model=None, version=None)
    mermaid = pkg.to_mermaid(graph)

    assert mermaid.startswith("graph LR")
    assert "subgraph" in mermaid


def test_to_dot(tmp_claude_home):
    import build_knowledge_graph as pkg

    entries = pkg.parse_all_journals()
    graph = pkg.build_graph(entries, model=None, version=None)
    dot = pkg.to_dot(graph)

    assert dot.startswith("graph KG {")
    assert "layout=neato" in dot


def test_write_summary(tmp_claude_home):
    import build_knowledge_graph as pkg

    entries = pkg.parse_all_journals()
    graph = pkg.build_graph(entries, model=None, version=None)
    summary = pkg.write_summary(graph)

    assert "# Knowledge Graph Summary" in summary
    assert "Top Entities by Mentions" in summary
    assert "Entity Types Distribution" in summary
