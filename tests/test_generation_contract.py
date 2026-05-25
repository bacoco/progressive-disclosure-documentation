import json
from pathlib import Path

from pdd.generation.renderer import generate_docs
from pdd.inventory.scanner import scan_repo


def test_generate_writes_docs_and_artifacts(tmp_path):
    inventory = scan_repo(Path("examples/minimal-repo"))
    out = tmp_path / "docs"
    stats = generate_docs(inventory, out)
    assert "INDEX.md" in stats["documents"]
    assert (out / "INDEX.md").exists()
    assert (tmp_path / ".pdd" / "source-map.json").exists()
    manifest = json.loads((tmp_path / ".pdd" / "manifest.json").read_text())
    assert manifest["schema"] == "pdd.manifest.v1"
