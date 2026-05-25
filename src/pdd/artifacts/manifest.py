from __future__ import annotations

import time
from pathlib import Path
from typing import Iterable


def build_manifest(out_dir: Path, documents: Iterable[str]) -> dict[str, object]:
    return {
        "schema": "pdd.manifest.v1",
        "generated_at": int(time.time()),
        "docs_root": str(out_dir),
        "documents": sorted(documents),
    }
