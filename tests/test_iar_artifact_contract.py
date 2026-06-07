import json
from pathlib import Path

from pdd.generation.renderer import generate_docs
from pdd.inventory.scanner import scan_repo
from pdd.review import grounding_receipt


def test_inventory_records_disclosure_metadata(tmp_path):
    (tmp_path / "README.md").write_text("# Current Docs\n", encoding="utf-8")
    (tmp_path / "old-notes.md").write_text("# Old Notes\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "example.py").write_text("print('hello')\n", encoding="utf-8")

    inventory = scan_repo(tmp_path)
    by_path = {item.path: item.to_dict() for item in inventory.files}

    assert by_path["README.md"]["source_type"] == "documentation"
    assert by_path["README.md"]["authority"] == "primary"
    assert by_path["README.md"]["freshness"] == "current"
    assert by_path["README.md"]["version"] == by_path["README.md"]["sha256"][:12]
    assert by_path["old-notes.md"]["freshness"] == "stale"
    assert by_path["src/example.py"]["source_type"] == "implementation"


def test_generate_writes_progressive_disclosure_contract(tmp_path):
    inventory = scan_repo(Path("examples/minimal-repo"))
    docs = tmp_path / "docs"

    generate_docs(inventory, docs)

    pdd_dir = tmp_path / ".pdd"
    disclosure = json.loads((pdd_dir / "disclosure.json").read_text())
    source_map = json.loads((pdd_dir / "source-map.json").read_text())

    assert disclosure["schema"] == "pdd.disclosure.v1"
    assert [layer["name"] for layer in disclosure["layers"]] == [
        "inventory",
        "manifest",
        "source_map",
        "review",
        "index",
    ]
    assert disclosure["answering_contract"]["generated_docs_are_source_of_truth"] is False
    assert "source-map.json" in disclosure["answering_contract"]["must_verify_against"]
    assert (pdd_dir / "inventory.json").exists()
    assert source_map["sections"]["sources.md"][0]["sources"]


def test_grounding_receipt_reports_unmapped_generated_docs(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "INDEX.md").write_text("# Index\n", encoding="utf-8")
    (docs / "missing.md").write_text("# Missing\n", encoding="utf-8")
    source_map = tmp_path / ".pdd" / "source-map.json"
    source_map.parent.mkdir()
    source_map.write_text(
        json.dumps(
            {
                "schema": "pdd.source_map.v1",
                "documents": {"INDEX.md": ["README.md"]},
                "sections": {"INDEX.md": [{"section": "Index", "sources": ["README.md"]}]},
            }
        ),
        encoding="utf-8",
    )

    receipt = grounding_receipt(docs, source_map)

    assert receipt["status"] == "fail"
    assert receipt["missing_mappings"] == ["missing.md"]
    assert receipt["requires_human_review"] is True
