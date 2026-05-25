from __future__ import annotations

from pathlib import Path


DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".txt", ".html", ".htm"}
CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java"}
CONFIG_EXTENSIONS = {".json", ".yaml", ".yml", ".toml"}
BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf"}


def classify(path: Path) -> tuple[str, str, bool, bool, bool]:
    suffix = path.suffix.lower()
    parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    generated = any(part in {"dist", "build", ".next", "coverage"} for part in parts)
    stale = any(token in name for token in ("old", "deprecated", "archive"))
    binary = suffix in BINARY_EXTENSIONS
    if suffix in DOC_EXTENSIONS:
        return "documentation", "high", generated, stale, binary
    if suffix in CODE_EXTENSIONS:
        return "code", "high", generated, stale, binary
    if suffix in CONFIG_EXTENSIONS:
        return "configuration", "medium", generated, stale, binary
    if binary:
        return "asset", "low", generated, stale, binary
    return "source", "medium", generated, stale, binary


def is_supported(path: Path) -> bool:
    return path.suffix.lower() in DOC_EXTENSIONS | CODE_EXTENSIONS | CONFIG_EXTENSIONS | BINARY_EXTENSIONS
