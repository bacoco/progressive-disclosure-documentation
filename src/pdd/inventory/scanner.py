from __future__ import annotations

import hashlib
from pathlib import Path

from .classifier import classify, is_supported
from .models import Inventory, SourceFile

EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".pdd",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}


def _skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    return any(part in EXCLUDED_DIRS for part in rel.parts) or not is_supported(path)


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _title(path: Path) -> str:
    if path.suffix.lower() in {".md", ".txt", ".rst"}:
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("# "):
                    return line[2:].strip()
        except OSError:
            return path.stem
    return path.stem.replace("-", " ").replace("_", " ").strip().title()


def _source_type(kind: str) -> str:
    if kind == "code":
        return "implementation"
    return kind


def _authority(kind: str, generated: bool, binary_asset: bool) -> str:
    if generated:
        return "derived"
    if binary_asset:
        return "asset"
    if kind in {"code", "configuration", "documentation"}:
        return "primary"
    return "supporting"


def scan_repo(root: str | Path) -> Inventory:
    root_path = Path(root).resolve()
    files: list[SourceFile] = []
    unknowns: list[str] = []
    for path in sorted(root_path.rglob("*")):
        if not path.is_file() or _skip(path, root_path):
            continue
        try:
            kind, relevance, generated, stale, binary = classify(path.relative_to(root_path))
            sha256 = _sha(path)
            files.append(
                SourceFile(
                    path=str(path.relative_to(root_path)),
                    sha256=sha256,
                    bytes=path.stat().st_size,
                    kind=kind,
                    relevance=relevance,
                    generated=generated,
                    stale=stale,
                    binary_asset=binary,
                    title=_title(path),
                    source_type=_source_type(kind),
                    authority=_authority(kind, generated, binary),
                    freshness="stale" if stale else "current",
                    version=sha256[:12],
                )
            )
        except OSError as exc:
            unknowns.append(f"{path}: {exc}")
    return Inventory(root=str(root_path), files=files, unknowns=unknowns)
