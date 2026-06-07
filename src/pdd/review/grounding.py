from __future__ import annotations

import json
from pathlib import Path


def grounding_receipt(docs_dir: str | Path, source_map_path: str | Path) -> dict[str, object]:
    source_map = Path(source_map_path)
    docs = [path.name for path in Path(docs_dir).glob("*.md")]
    mapping: dict[str, object] = {}
    if source_map.exists():
        try:
            payload = json.loads(source_map.read_text(encoding="utf-8"))
            raw_mapping = payload.get("documents", {})
            if isinstance(raw_mapping, dict):
                mapping = raw_mapping
        except (OSError, json.JSONDecodeError):
            mapping = {}

    missing_mappings = sorted(doc for doc in docs if doc not in mapping)
    empty_mappings = sorted(
        doc
        for doc in docs
        if doc in mapping and isinstance(mapping[doc], list) and not mapping[doc]
    )
    ok = source_map.exists() and bool(docs) and not missing_mappings and not empty_mappings
    return {
        "schema": "pdd.grounding.v1",
        "status": "pass" if ok else "fail",
        "source_map": str(source_map),
        "documents": sorted(docs),
        "mapped_documents": sorted(mapping),
        "missing_mappings": missing_mappings,
        "empty_mappings": empty_mappings,
        "requires_human_review": not ok,
    }
