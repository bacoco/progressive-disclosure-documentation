from __future__ import annotations

from pathlib import Path

from pdd.inventory.models import Inventory


def coverage_receipt(docs_dir: str | Path, inventory: Inventory) -> dict[str, object]:
    docs = list(Path(docs_dir).glob("*.md"))
    covered = len(docs) > 0 and len(inventory.files) > 0
    return {
        "schema": "pdd.coverage.v1",
        "status": "pass" if covered else "warn",
        "documents": sorted(path.name for path in docs),
        "source_count": len(inventory.files),
        "unknowns": inventory.unknowns,
    }
