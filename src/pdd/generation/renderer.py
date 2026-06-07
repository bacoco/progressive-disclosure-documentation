from __future__ import annotations

import json
from pathlib import Path

from pdd.artifacts.disclosure import build_disclosure_contract
from pdd.artifacts.manifest import build_manifest
from pdd.generation.planner import selected_sources
from pdd.generation.templates import architecture_page, index_page, sources_page
from pdd.inventory.models import Inventory


def generate_docs(inventory: Inventory, out_dir: str | Path) -> dict[str, object]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pdd_dir = out.parent / ".pdd"
    pdd_dir.mkdir(parents=True, exist_ok=True)

    sources = selected_sources(inventory)
    docs = {
        "INDEX.md": index_page(inventory, sources),
        "sources.md": sources_page(sources),
        "architecture.md": architecture_page(sources),
    }
    for name, content in docs.items():
        (out / name).write_text(content, encoding="utf-8")

    source_paths = [source.path for source in sources]
    source_map = {
        "schema": "pdd.source_map.v1",
        "documents": {name: source_paths for name in docs},
        "sections": {
            "INDEX.md": [
                {"section": "Source Summary", "sources": source_paths},
                {"section": "Primary Sources", "sources": source_paths[:30]},
            ],
            "sources.md": [{"section": "Source Map", "sources": source_paths}],
            "architecture.md": [
                {
                    "section": "Architecture Notes",
                    "sources": [
                        source.path
                        for source in sources
                        if source.kind in {"code", "configuration"}
                    ],
                }
            ],
        },
    }
    manifest = build_manifest(out, docs.keys())
    (pdd_dir / "inventory.json").write_text(json.dumps(inventory.to_dict(), indent=2), encoding="utf-8")
    (pdd_dir / "source-map.json").write_text(json.dumps(source_map, indent=2), encoding="utf-8")
    (pdd_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (pdd_dir / "disclosure.json").write_text(
        json.dumps(build_disclosure_contract(), indent=2),
        encoding="utf-8",
    )
    (pdd_dir / "overrides.jsonl").touch(exist_ok=True)
    (pdd_dir / "stale-removals.jsonl").touch(exist_ok=True)
    return {"documents": sorted(docs), "sources": len(sources), "pdd_dir": str(pdd_dir)}
