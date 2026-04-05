#!/usr/bin/env python3
"""
Knowledge Graph Builder — extracts entities from journal entries using GLiNER,
builds a co-occurrence graph, and outputs queryable JSON + markdown summary.

Usage:
    python3 build-knowledge-graph.py rebuild
    python3 build-knowledge-graph.py query "entity name"
    python3 build-knowledge-graph.py stats
    python3 build-knowledge-graph.py visualize [--format mermaid|dot|html]
    python3 build-knowledge-graph.py incremental --file <path>
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import NamedTuple, Optional

CLAUDE_HOME = Path(os.getenv("CLAUDE_HOME", Path.home() / ".claude"))
JOURNAL_DIR = CLAUDE_HOME / "journal"
IDEAS_DIR = CLAUDE_HOME / "ideas"
SOURCES_RAW_DIR = CLAUDE_HOME / "sources" / "raw"
GRAPH_FILE = JOURNAL_DIR / "knowledge-graph.json"
SUMMARY_FILE = JOURNAL_DIR / "knowledge-graph-summary.md"
LOCK_FILE = JOURNAL_DIR / ".knowledge-graph.lock"


def _load_config():
    config_path = CLAUDE_HOME / "dendrite.config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}

_CONFIG = _load_config()

DEFAULT_MODEL = _CONFIG.get("gliner_model", "fastino/gliner2-base-v1")
GLINER_THRESHOLD = _CONFIG.get("gliner_threshold", 0.4)

ENTITY_TYPES = _CONFIG.get("entity_types", [
    "person",
    "organization",
    "tool/technology",
    "scientific_concept",
    "disease",
    "drug/molecule",
    "idea",
])

JOURNAL_EXCLUDE = {"SCHEMA.md", "index.md", "knowledge-graph-summary.md"}
IDEAS_EXCLUDE = {"PIPELINE.md", ".gitkeep"}
SOURCES_EXCLUDE = {"tweets.md"}

ENTRY_RE = re.compile(r"^###\s+(\d{2}:\d{2})\s+\|\s+(?:\[(\w+)\]\s+)?(.+)$")
TAG_RE = re.compile(r"#([\w-]+)")
AUTO_EXTRACTED_RE = re.compile(r"^##\s+Auto-Extracted", re.MULTILINE)
IDEA_TITLE_RE = re.compile(r"^#\s+Idea:\s*(.+)$", re.MULTILINE)
IDEA_DATE_RE = re.compile(r"\*\*Created\*\*:\s*(\d{4}-\d{2}-\d{2})")


class JournalEntry(NamedTuple):
    date: str
    time: str
    category: str
    title: str
    body: str
    tags: list
    source_file: str


class Entity(NamedTuple):
    text: str
    entity_type: str
    raw_text: str


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def find_journal_files():
    if not JOURNAL_DIR.exists():
        return []
    files = []
    for md in sorted(JOURNAL_DIR.rglob("*.md")):
        if md.name in JOURNAL_EXCLUDE or md.name == "knowledge-graph.json":
            continue
        if re.match(r"\d{4}-\d{2}-\d{2}\.md$", md.name):
            files.append(md)
    return files


def parse_journal_file(filepath: Path) -> list:
    text = filepath.read_text(encoding="utf-8")

    auto_match = AUTO_EXTRACTED_RE.search(text)
    if auto_match:
        text = text[:auto_match.start()]

    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", filepath.name)
    file_date = date_match.group(1) if date_match else "unknown"

    entries = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = ENTRY_RE.match(lines[i])
        if m:
            time_str, category, title = m.group(1), m.group(2) or "learning", m.group(3)
            body_lines = []
            i += 1
            while i < len(lines) and not ENTRY_RE.match(lines[i]) and not lines[i].startswith("## "):
                body_lines.append(lines[i])
                i += 1
            body = "\n".join(body_lines).strip()
            tags = TAG_RE.findall(body + " " + title)
            entries.append(JournalEntry(
                date=file_date,
                time=time_str,
                category=category.lower(),
                title=title.strip(),
                body=body,
                tags=tags,
                source_file=str(filepath),
            ))
        else:
            i += 1
    return entries


def parse_idea_file(filepath: Path) -> list:
    text = filepath.read_text(encoding="utf-8")

    title_match = IDEA_TITLE_RE.search(text)
    title = title_match.group(1).strip() if title_match else filepath.stem

    date_match = IDEA_DATE_RE.search(text)
    date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")

    body_parts = []
    for section in ("## What", "## Why", "## Notes"):
        idx = text.find(section)
        if idx == -1:
            continue
        start = idx + len(section)
        next_section = len(text)
        for other in ("## What", "## Why", "## Next Steps", "## Notes"):
            oidx = text.find(other, start)
            if oidx != -1 and oidx < next_section:
                next_section = oidx
        body_parts.append(text[start:next_section].strip())

    body = "\n".join(body_parts)
    tags = TAG_RE.findall(text)

    return [JournalEntry(
        date=date,
        time="00:00",
        category="idea",
        title=title,
        body=body,
        tags=tags,
        source_file=str(filepath),
    )]


def parse_source_file(filepath: Path) -> list:
    text = filepath.read_text(encoding="utf-8")

    title = filepath.stem
    date = datetime.now().strftime("%Y-%m-%d")

    body = text
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            frontmatter = text[3:end]
            body = text[end + 3:].strip()
            for line in frontmatter.split("\n"):
                if line.startswith("date:"):
                    date = line.split(":", 1)[1].strip().strip('"')
                elif line.startswith("author_name:"):
                    title = line.split(":", 1)[1].strip().strip('"') + " — " + title

    tags = TAG_RE.findall(body)

    return [JournalEntry(
        date=date,
        time="00:00",
        category="source",
        title=title,
        body=body,
        tags=tags,
        source_file=str(filepath),
    )]


def parse_single_file(filepath: Path) -> list:
    fp = str(filepath.resolve())
    if fp.startswith(str(JOURNAL_DIR)):
        return parse_journal_file(filepath)
    elif fp.startswith(str(IDEAS_DIR)):
        return parse_idea_file(filepath)
    elif fp.startswith(str(SOURCES_RAW_DIR)):
        return parse_source_file(filepath)
    return []


def parse_all_journals() -> list:
    all_entries = []
    for md_file in find_journal_files():
        all_entries.extend(parse_journal_file(md_file))
    if IDEAS_DIR.exists():
        for md_file in sorted(IDEAS_DIR.rglob("*.md")):
            if md_file.name in IDEAS_EXCLUDE:
                continue
            all_entries.extend(parse_idea_file(md_file))
    if SOURCES_RAW_DIR.exists():
        for md_file in sorted(SOURCES_RAW_DIR.rglob("*.md")):
            if md_file.name in SOURCES_EXCLUDE:
                continue
            all_entries.extend(parse_source_file(md_file))
    return all_entries


# ---------------------------------------------------------------------------
# Entity extraction
# ---------------------------------------------------------------------------

def try_load_gliner(model_name=DEFAULT_MODEL):
    # Try GLiNER2 (fastino) first, fall back to GLiNER v1
    try:
        from gliner2 import GLiNER2
        model = GLiNER2.from_pretrained(model_name)
        model._gliner_version = 2
        return model, model_name
    except Exception:
        pass
    try:
        from gliner import GLiNER
        model = GLiNER.from_pretrained(model_name)
        model._gliner_version = 1
        return model, model_name
    except Exception:
        return None, None


def normalize_entity_key(text: str) -> str:
    key = text.lower().strip()
    key = re.sub(r"[^a-z0-9\s-]", "", key)
    key = re.sub(r"\s+", "-", key)
    return key


def extract_entities_gliner(text: str, model) -> list:
    if not text.strip():
        return []

    version = getattr(model, "_gliner_version", 1)

    if version == 2:
        try:
            results = model.extract_entities(text, ENTITY_TYPES, threshold=GLINER_THRESHOLD)
        except Exception:
            return []
        entities = []
        for entity_type, mentions in results.get("entities", {}).items():
            for mention in mentions:
                key = normalize_entity_key(mention)
                if key and len(key) >= 2:
                    entities.append(Entity(text=key, entity_type=entity_type, raw_text=mention))
        return entities

    # GLiNER v1 path
    try:
        results = model.predict_entities(text, ENTITY_TYPES, threshold=GLINER_THRESHOLD)
    except Exception:
        return []

    seen = {}
    for r in results:
        key = normalize_entity_key(r["text"])
        if not key or len(key) < 2:
            continue
        if key in seen:
            if r["score"] > seen[key]["score"]:
                seen[key] = r
        else:
            seen[key] = r

    return [
        Entity(text=key, entity_type=r["label"], raw_text=r["text"])
        for key, r in seen.items()
    ]


def extract_entities_tags_only(entry: JournalEntry) -> list:
    entities = []
    for tag in entry.tags:
        key = normalize_entity_key(tag)
        if key and len(key) >= 2:
            entities.append(Entity(text=key, entity_type="tag", raw_text=tag))
    return entities


def extract_entities(entry: JournalEntry, model) -> list:
    combined_text = f"{entry.title}. {entry.body}"
    if model:
        gliner_entities = extract_entities_gliner(combined_text, model)
        tag_entities = extract_entities_tags_only(entry)
        merged = {e.text: e for e in gliner_entities}
        for te in tag_entities:
            if te.text not in merged:
                merged[te.text] = te
        return list(merged.values())
    return extract_entities_tags_only(entry)


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_graph(entries: list, model, version: str | None) -> dict:
    nodes = {}
    edges = {}

    for entry in entries:
        entities = extract_entities(entry, model)
        entry_ref = {
            "date": entry.date,
            "time": entry.time,
            "title": entry.title,
            "source_file": entry.source_file,
        }

        for ent in entities:
            if ent.text in nodes:
                node = nodes[ent.text]
                node["mentions"] += 1
                if entry.date < node["first_seen"]:
                    node["first_seen"] = entry.date
                if entry.date > node["last_seen"]:
                    node["last_seen"] = entry.date
                node["entries"].append(entry_ref)
                if ent.entity_type != "tag" and node["type"] == "tag":
                    node["type"] = ent.entity_type
                    node["label"] = ent.raw_text
            else:
                nodes[ent.text] = {
                    "id": ent.text,
                    "label": ent.raw_text,
                    "type": ent.entity_type,
                    "mentions": 1,
                    "first_seen": entry.date,
                    "last_seen": entry.date,
                    "entries": [entry_ref],
                }

        ent_keys = [e.text for e in entities]
        for i in range(len(ent_keys)):
            for j in range(i + 1, len(ent_keys)):
                a, b = sorted([ent_keys[i], ent_keys[j]])
                edge_key = (a, b)
                if edge_key in edges:
                    edges[edge_key]["weight"] += 1
                    edges[edge_key]["entries"].append(entry_ref)
                else:
                    edges[edge_key] = {
                        "source": a,
                        "target": b,
                        "weight": 1,
                        "entries": [entry_ref],
                    }

    return {
        "directed": False,
        "multigraph": False,
        "graph": {
            "built_at": datetime.now().isoformat(timespec="seconds"),
            "entry_count": len(entries),
            "entity_count": len(nodes),
            "edge_count": len(edges),
            "gliner_available": model is not None,
            "gliner_model": version or "none (tag-only fallback)",
        },
        "nodes": list(nodes.values()),
        "links": list(edges.values()),
    }


# ---------------------------------------------------------------------------
# Incremental merge
# ---------------------------------------------------------------------------

def acquire_lock(timeout: int = 30):
    import fcntl
    import time
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    fd = open(LOCK_FILE, "w")
    deadline = time.time() + timeout
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd
        except (BlockingIOError, OSError):
            if time.time() >= deadline:
                fd.close()
                return None
            time.sleep(0.5)


def release_lock(fd):
    import fcntl
    if fd:
        fcntl.flock(fd, fcntl.LOCK_UN)
        fd.close()


def merge_into_graph(existing: dict, new_entries: list, model, version, source_file: str) -> dict:
    nodes_by_id = {n["id"]: n for n in existing.get("nodes", [])}
    edges_by_key = {}
    for link in existing.get("links", []):
        key = (link["source"], link["target"])
        edges_by_key[key] = link

    for nid, node in list(nodes_by_id.items()):
        original_count = len(node.get("entries", []))
        node["entries"] = [
            e for e in node.get("entries", [])
            if e.get("source_file") != source_file
        ]
        removed = original_count - len(node["entries"])
        node["mentions"] = max(0, node.get("mentions", 0) - removed)
        if node["mentions"] <= 0:
            del nodes_by_id[nid]

    for key, edge in list(edges_by_key.items()):
        original_count = len(edge.get("entries", []))
        edge["entries"] = [
            e for e in edge.get("entries", [])
            if e.get("source_file") != source_file
        ]
        removed = original_count - len(edge["entries"])
        edge["weight"] = max(0, edge.get("weight", 0) - removed)
        if edge["weight"] <= 0:
            del edges_by_key[key]

    for entry in new_entries:
        entities = extract_entities(entry, model)
        entry_ref = {
            "date": entry.date,
            "time": entry.time,
            "title": entry.title,
            "source_file": entry.source_file,
        }

        for ent in entities:
            if ent.text in nodes_by_id:
                node = nodes_by_id[ent.text]
                node["mentions"] += 1
                if entry.date < node.get("first_seen", "9999"):
                    node["first_seen"] = entry.date
                if entry.date > node.get("last_seen", "0000"):
                    node["last_seen"] = entry.date
                node["entries"].append(entry_ref)
                if ent.entity_type != "tag" and node.get("type") == "tag":
                    node["type"] = ent.entity_type
                    node["label"] = ent.raw_text
            else:
                nodes_by_id[ent.text] = {
                    "id": ent.text,
                    "label": ent.raw_text,
                    "type": ent.entity_type,
                    "mentions": 1,
                    "first_seen": entry.date,
                    "last_seen": entry.date,
                    "entries": [entry_ref],
                }

        ent_keys = [e.text for e in entities]
        for i in range(len(ent_keys)):
            for j in range(i + 1, len(ent_keys)):
                a, b = sorted([ent_keys[i], ent_keys[j]])
                edge_key = (a, b)
                if edge_key in edges_by_key:
                    edges_by_key[edge_key]["weight"] += 1
                    edges_by_key[edge_key]["entries"].append(entry_ref)
                else:
                    edges_by_key[edge_key] = {
                        "source": a,
                        "target": b,
                        "weight": 1,
                        "entries": [entry_ref],
                    }

    return {
        "directed": False,
        "multigraph": False,
        "graph": {
            "built_at": datetime.now().isoformat(timespec="seconds"),
            "entry_count": existing.get("graph", {}).get("entry_count", 0),
            "entity_count": len(nodes_by_id),
            "edge_count": len(edges_by_key),
            "gliner_available": model is not None,
            "gliner_model": version or existing.get("graph", {}).get("gliner_model", "none"),
            "last_incremental": source_file,
        },
        "nodes": list(nodes_by_id.values()),
        "links": list(edges_by_key.values()),
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_graph(graph_data: dict):
    GRAPH_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(GRAPH_FILE, "w") as f:
        json.dump(graph_data, f, indent=2)


def write_summary(graph_data: dict) -> str:
    meta = graph_data["graph"]
    nodes = graph_data["nodes"]
    links = graph_data["links"]

    by_mentions = sorted(nodes, key=lambda n: n["mentions"], reverse=True)[:15]
    degree = defaultdict(int)
    neighbors = defaultdict(list)
    for link in links:
        degree[link["source"]] += link["weight"]
        degree[link["target"]] += link["weight"]
        neighbors[link["source"]].append(link["target"])
        neighbors[link["target"]].append(link["source"])

    by_degree = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:10]

    type_counts = defaultdict(int)
    for n in nodes:
        type_counts[n["type"]] += 1

    lines = [
        "# Knowledge Graph Summary",
        "",
        f"Built: {meta['built_at']} | Entries: {meta['entry_count']} | "
        f"Entities: {meta['entity_count']} | Connections: {meta['edge_count']}",
        f"Mode: {'GLiNER (' + meta['gliner_model'] + ')' if meta.get('gliner_available') else 'Tag-only fallback'}",
        "",
        "## Top Entities by Mentions",
        "| Entity | Type | Mentions |",
        "|--------|------|----------|",
    ]
    for n in by_mentions:
        lines.append(f"| {n['label']} | {n['type']} | {n['mentions']} |")

    lines += [
        "",
        "## Most Connected (Hub Entities)",
        "| Entity | Connections | Top Neighbors |",
        "|--------|-------------|---------------|",
    ]
    node_lookup = {n["id"]: n for n in nodes}
    for nid, deg in by_degree:
        label = node_lookup.get(nid, {}).get("label", nid)
        top_n = ", ".join(neighbors[nid][:5])
        lines.append(f"| {label} | {deg} | {top_n} |")

    lines += [
        "",
        "## Entity Types Distribution",
        "| Type | Count |",
        "|------|-------|",
    ]
    for t, c in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {t} | {c} |")

    lines += ["", "## Clusters"]
    visited = set()
    components = []
    adj = defaultdict(set)
    for link in links:
        adj[link["source"]].add(link["target"])
        adj[link["target"]].add(link["source"])

    for nid in [n["id"] for n in nodes]:
        if nid in visited:
            continue
        component = []
        stack = [nid]
        while stack:
            cur = stack.pop()
            if cur in visited:
                continue
            visited.add(cur)
            component.append(cur)
            for nb in adj[cur]:
                if nb not in visited:
                    stack.append(nb)
        if len(component) > 1:
            components.append(component)

    components.sort(key=len, reverse=True)
    for comp in components[:10]:
        rep = node_lookup.get(comp[0], {}).get("label", comp[0])
        members = ", ".join(comp[:15])
        if len(comp) > 15:
            members += f", ... (+{len(comp) - 15} more)"
        lines.append(f"### {rep}")
        lines.append(members)
        lines.append("")

    summary = "\n".join(lines)
    SUMMARY_FILE.write_text(summary, encoding="utf-8")
    return summary


# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------

def load_graph() -> dict | None:
    if not GRAPH_FILE.exists():
        return None
    with open(GRAPH_FILE) as f:
        return json.load(f)


def query_entity(name: str, graph_data: dict):
    query = normalize_entity_key(name)
    matches = []
    for node in graph_data["nodes"]:
        if query in node["id"] or query in node["label"].lower():
            matches.append(node)

    if not matches:
        print(f"No entity matching '{name}' found.")
        print(f"Available entities ({len(graph_data['nodes'])} total):")
        for n in sorted(graph_data["nodes"], key=lambda x: x["mentions"], reverse=True)[:20]:
            print(f"  - {n['label']} ({n['type']}, {n['mentions']} mentions)")
        return

    for node in matches:
        print(f"\n{'='*60}")
        print(f"Entity: {node['label']}")
        print(f"Type: {node['type']}")
        print(f"Mentions: {node['mentions']}")
        print(f"First seen: {node['first_seen']} | Last seen: {node['last_seen']}")

        connections = []
        for link in graph_data["links"]:
            if link["source"] == node["id"]:
                connections.append((link["target"], link["weight"]))
            elif link["target"] == node["id"]:
                connections.append((link["source"], link["weight"]))

        if connections:
            connections.sort(key=lambda x: x[1], reverse=True)
            print(f"\nConnections ({len(connections)}):")
            node_lookup = {n["id"]: n for n in graph_data["nodes"]}
            for cid, weight in connections:
                clabel = node_lookup.get(cid, {}).get("label", cid)
                ctype = node_lookup.get(cid, {}).get("type", "unknown")
                print(f"  - {clabel} ({ctype}, weight={weight})")

        if node.get("entries"):
            print(f"\nSource entries:")
            for e in node["entries"]:
                print(f"  - [{e['date']}] {e['title']}")


def query_stats(graph_data: dict):
    meta = graph_data["graph"]
    nodes = graph_data["nodes"]
    links = graph_data["links"]

    print(f"Knowledge Graph Statistics")
    print(f"{'='*40}")
    print(f"Built: {meta['built_at']}")
    print(f"Mode: {'GLiNER' if meta.get('gliner_available') else 'Tag-only fallback'}")
    print(f"Entries processed: {meta['entry_count']}")
    print(f"Entities: {meta['entity_count']}")
    print(f"Connections: {meta['edge_count']}")

    type_counts = defaultdict(int)
    for n in nodes:
        type_counts[n["type"]] += 1

    print(f"\nEntity Types:")
    for t, c in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {t}: {c}")

    degree = defaultdict(int)
    for link in links:
        degree[link["source"]] += link["weight"]
        degree[link["target"]] += link["weight"]

    top_hubs = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:10]
    node_lookup = {n["id"]: n for n in nodes}
    if top_hubs:
        print(f"\nTop Hubs:")
        for nid, deg in top_hubs:
            label = node_lookup.get(nid, {}).get("label", nid)
            print(f"  {label}: {deg} connections")


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def to_mermaid(graph_data: dict, max_nodes: int = 50) -> str:
    nodes = sorted(graph_data["nodes"], key=lambda n: n["mentions"], reverse=True)[:max_nodes]
    node_ids = {n["id"] for n in nodes}
    links = [l for l in graph_data["links"] if l["source"] in node_ids and l["target"] in node_ids]

    by_type = defaultdict(list)
    for n in nodes:
        by_type[n["type"]].append(n)

    lines = ["graph LR"]
    for etype, enodes in by_type.items():
        safe_type = etype.replace("/", "_").replace(" ", "_")
        lines.append(f"    subgraph {safe_type}")
        for n in enodes:
            safe_id = n["id"].replace("-", "_")
            lines.append(f'        {safe_id}["{n["label"]}"]')
        lines.append("    end")

    for link in links:
        src = link["source"].replace("-", "_")
        tgt = link["target"].replace("-", "_")
        if link["weight"] > 2:
            lines.append(f"    {src} ==> {tgt}")
        elif link["weight"] > 1:
            lines.append(f"    {src} --> {tgt}")
        else:
            lines.append(f"    {src} -.-> {tgt}")

    return "\n".join(lines)


def to_dot(graph_data: dict, max_nodes: int = 50) -> str:
    type_colors = {
        "person": "#4CAF50",
        "organization": "#2196F3",
        "tool/technology": "#FF9800",
        "scientific_concept": "#9C27B0",
        "disease": "#F44336",
        "drug/molecule": "#00BCD4",
        "idea": "#FFEB3B",
        "tag": "#9E9E9E",
    }

    nodes = sorted(graph_data["nodes"], key=lambda n: n["mentions"], reverse=True)[:max_nodes]
    node_ids = {n["id"] for n in nodes}
    links = [l for l in graph_data["links"] if l["source"] in node_ids and l["target"] in node_ids]

    lines = ["graph KG {", "    layout=neato;", "    overlap=false;", "    splines=true;", ""]
    for n in nodes:
        safe_id = n["id"].replace("-", "_")
        color = type_colors.get(n["type"], "#9E9E9E")
        lines.append(f'    {safe_id} [label="{n["label"]}" style=filled fillcolor="{color}" fontsize=10];')

    lines.append("")
    for link in links:
        src = link["source"].replace("-", "_")
        tgt = link["target"].replace("-", "_")
        penwidth = min(link["weight"] * 1.5, 6)
        lines.append(f"    {src} -- {tgt} [penwidth={penwidth}];")

    lines.append("}")
    return "\n".join(lines)


def to_html(graph_data: dict) -> str:
    template_path = Path(__file__).resolve().parent.parent / "visualization" / "dendrite.html"
    if not template_path.exists():
        return "HTML template not found. Expected at: " + str(template_path)
    template = template_path.read_text(encoding="utf-8")
    graph_json = json.dumps(graph_data, indent=2)
    return template.replace("/*__GRAPH_DATA__*/{}", graph_json)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_rebuild(args):
    entries = parse_all_journals()
    if not entries:
        print("No journal entries found.", file=sys.stderr)
        return 0

    model, version = (None, None)
    if not args.tags_only:
        print("Loading GLiNER model...", file=sys.stderr)
        model, version = try_load_gliner(args.model)
        if model:
            print(f"GLiNER loaded: {version}", file=sys.stderr)
        else:
            print("GLiNER not available, using tag-only fallback.", file=sys.stderr)

    graph_data = build_graph(entries, model, version)
    write_graph(graph_data)
    summary = write_summary(graph_data)
    print(summary)
    print(f"\nGraph written to {GRAPH_FILE}", file=sys.stderr)
    return 0


def cmd_query(args):
    graph_data = load_graph()
    if not graph_data:
        print("No knowledge graph found. Run `rebuild` first.")
        return 1
    query_entity(args.name, graph_data)
    return 0


def cmd_stats(args):
    graph_data = load_graph()
    if not graph_data:
        print("No knowledge graph found. Run `rebuild` first.")
        return 1
    query_stats(graph_data)
    return 0


def cmd_visualize(args):
    graph_data = load_graph()
    if not graph_data:
        print("No knowledge graph found. Run `rebuild` first.")
        return 1
    if args.format == "dot":
        print(to_dot(graph_data, max_nodes=args.max_nodes))
    elif args.format == "html":
        html = to_html(graph_data)
        out_path = JOURNAL_DIR / "dendrite.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"HTML visualization written to {out_path}", file=sys.stderr)
        print(html)
    else:
        print(to_mermaid(graph_data, max_nodes=args.max_nodes))
    return 0


def cmd_incremental(args):
    filepath = Path(args.file).resolve()
    if not filepath.exists():
        print(f"File not found: {filepath}", file=sys.stderr)
        return 1

    lock_fd = acquire_lock(timeout=30)
    if lock_fd is None:
        print("Could not acquire lock, skipping update.", file=sys.stderr)
        return 0

    try:
        entries = parse_single_file(filepath)
        if not entries:
            return 0

        model, version = (None, None)
        if not args.tags_only:
            model, version = try_load_gliner(args.model)

        if GRAPH_FILE.exists():
            with open(GRAPH_FILE) as f:
                existing = json.load(f)
            graph_data = merge_into_graph(existing, entries, model, version, str(filepath))
        else:
            graph_data = build_graph(entries, model, version)

        GRAPH_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(GRAPH_FILE, "w") as f:
            json.dump(graph_data, f, indent=2)

        write_summary(graph_data)
        print(f"Incremental update: {len(entries)} entries from {filepath.name}", file=sys.stderr)
        return 0
    finally:
        release_lock(lock_fd)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Knowledge Graph Builder")
    subparsers = parser.add_subparsers(dest="command")

    rebuild_p = subparsers.add_parser("rebuild", help="Full rebuild from all journals + ideas")
    rebuild_p.add_argument("--model", default=DEFAULT_MODEL, help="GLiNER model name")
    rebuild_p.add_argument("--tags-only", action="store_true", help="Skip GLiNER, use tags only")
    rebuild_p.add_argument("--config", type=Path, help="Path to dendrite.config.json")

    query_p = subparsers.add_parser("query", help="Query entity connections")
    query_p.add_argument("name", help="Entity name to search for")

    subparsers.add_parser("stats", help="Show graph statistics")

    viz_p = subparsers.add_parser("visualize", help="Output graph visualization")
    viz_p.add_argument("--format", choices=["mermaid", "dot", "html"], default="mermaid", help="Output format")
    viz_p.add_argument("--max-nodes", type=int, default=50, help="Maximum nodes to display")

    inc_p = subparsers.add_parser("incremental", help="Incremental update from a single file")
    inc_p.add_argument("--file", required=True, type=Path, help="Path to changed file")
    inc_p.add_argument("--model", default=DEFAULT_MODEL, help="GLiNER model name")
    inc_p.add_argument("--tags-only", action="store_true", help="Skip GLiNER, use tags only")
    inc_p.add_argument("--config", type=Path, help="Path to dendrite.config.json")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    handlers = {
        "rebuild": cmd_rebuild,
        "query": cmd_query,
        "stats": cmd_stats,
        "visualize": cmd_visualize,
        "incremental": cmd_incremental,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main() or 0)
