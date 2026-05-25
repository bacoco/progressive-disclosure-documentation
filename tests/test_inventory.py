from pathlib import Path

from pdd.inventory.scanner import scan_repo


def test_scan_minimal_repo_finds_docs_and_code():
    inventory = scan_repo(Path("examples/minimal-repo"))
    paths = {item.path for item in inventory.files}
    assert "README.md" in paths
    assert "src/example.py" in paths
    assert inventory.unknowns == []


def test_inventory_serializes_roundtrip():
    inventory = scan_repo(Path("examples/minimal-repo"))
    data = inventory.to_dict()
    assert data["schema"] == "pdd.inventory.v1"
    assert len(data["files"]) >= 2
