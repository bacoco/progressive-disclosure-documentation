from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_receipt(out_dir: str | Path, name: str, payload: dict[str, Any]) -> Path:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    path = target / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
