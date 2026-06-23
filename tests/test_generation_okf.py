from pathlib import Path

from pdd.generation.renderer import generate_docs
from pdd.generation.templates import okf_frontmatter
from pdd.inventory.scanner import scan_repo


def test_generated_pages_carry_okf_frontmatter(tmp_path):
    inventory = scan_repo(Path("examples/minimal-repo"))
    out = tmp_path / "docs"
    generate_docs(inventory, out, generated_at="2026-06-23")
    for name in ("INDEX.md", "sources.md", "architecture.md"):
        text = (out / name).read_text(encoding="utf-8")
        assert text.startswith("---\n")                       # OKF frontmatter leads the file
        head = text.split("---", 2)[1]
        assert "type:" in head and "title:" in head
        assert "timestamp: 2026-06-23" in head                # injected date -> deterministic output


def test_index_links_to_sibling_concepts(tmp_path):
    inventory = scan_repo(Path("examples/minimal-repo"))
    out = tmp_path / "docs"
    generate_docs(inventory, out, generated_at="2026-06-23")
    index = (out / "INDEX.md").read_text(encoding="utf-8")
    assert "(sources.md)" in index and "(architecture.md)" in index   # OKF cross-links


def test_okf_frontmatter_quotes_special_values():
    block = okf_frontmatter(doc_type="Concept", title='A: b "c"', timestamp="2026-06-23")
    assert block.startswith("---") and block.rstrip().endswith("---")
    assert 'title: "A: b \\"c\\""' in block                   # colon + quotes escaped, YAML-safe
    assert "type: Concept" in block and "timestamp: 2026-06-23" in block
