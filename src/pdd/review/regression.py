from __future__ import annotations

from pathlib import Path


def regression_receipt(docs_dir: str | Path) -> dict[str, object]:
    docs_root = Path(docs_dir)
    required = ["INDEX.md", "sources.md"]
    missing = [name for name in required if not (docs_root / name).exists()]
    return {
        "schema": "pdd.regression.v1",
        "status": "pass" if not missing else "fail",
        "required_documents": required,
        "missing": missing,
    }
