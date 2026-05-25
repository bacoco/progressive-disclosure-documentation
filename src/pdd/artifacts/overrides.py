from __future__ import annotations

from pathlib import Path


def ensure_override_files(pdd_dir: str | Path) -> None:
    target = Path(pdd_dir)
    target.mkdir(parents=True, exist_ok=True)
    (target / "overrides.jsonl").touch(exist_ok=True)
    (target / "stale-removals.jsonl").touch(exist_ok=True)
