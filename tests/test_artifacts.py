from pathlib import Path

from pdd.generation.renderer import generate_docs
from pdd.index.retrieval import search
from pdd.index.sqlite_fts import build_index
from pdd.inventory.scanner import scan_repo


def test_index_can_search_generated_docs(tmp_path):
    inventory = scan_repo(Path("examples/minimal-repo"))
    docs = tmp_path / "docs"
    generate_docs(inventory, docs)
    index_path = tmp_path / "index.sqlite"
    stats = build_index(docs, index_path)
    assert stats["documents"] >= 1
    hits = search(index_path, "documentation")
    assert hits
