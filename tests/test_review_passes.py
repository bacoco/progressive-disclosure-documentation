from pathlib import Path

from pdd.generation.renderer import generate_docs
from pdd.inventory.scanner import scan_repo
from pdd.review import coverage_receipt, grounding_receipt, regression_receipt


def test_review_receipts_pass_for_generated_docs(tmp_path):
    inventory = scan_repo(Path("examples/minimal-repo"))
    docs = tmp_path / "docs"
    generate_docs(inventory, docs)
    source_map = tmp_path / ".pdd" / "source-map.json"
    assert coverage_receipt(docs, inventory)["status"] == "pass"
    assert grounding_receipt(docs, source_map)["status"] == "pass"
    assert regression_receipt(docs)["status"] == "pass"
