from __future__ import annotations

from pathlib import Path


def grounding_receipt(docs_dir: str | Path, source_map_path: str | Path) -> dict[str, object]:
    source_map = Path(source_map_path)
    docs = [path.name for path in Path(docs_dir).glob("*.md")]
    ok = source_map.exists() and bool(docs)
    return {
        "schema": "pdd.grounding.v1",
        "status": "pass" if ok else "fail",
        "source_map": str(source_map),
        "documents": sorted(docs),
        "requires_human_review": not ok,
    }
