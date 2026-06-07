from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class SourceFile:
    path: str
    sha256: str
    bytes: int
    kind: str
    relevance: str
    generated: bool = False
    stale: bool = False
    binary_asset: bool = False
    title: str = ""
    source_type: str = ""
    authority: str = "supporting"
    freshness: str = "current"
    version: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceFile":
        return cls(
            path=str(data["path"]),
            sha256=str(data["sha256"]),
            bytes=int(data.get("bytes", 0)),
            kind=str(data.get("kind", "source")),
            relevance=str(data.get("relevance", "medium")),
            generated=bool(data.get("generated", False)),
            stale=bool(data.get("stale", False)),
            binary_asset=bool(data.get("binary_asset", False)),
            title=str(data.get("title", "")),
            source_type=str(data.get("source_type", data.get("kind", "source"))),
            authority=str(data.get("authority", "supporting")),
            freshness=str(data.get("freshness", "current")),
            version=str(data.get("version", "")),
        )


@dataclass(frozen=True)
class Inventory:
    root: str
    files: list[SourceFile]
    unknowns: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "pdd.inventory.v1",
            "root": self.root,
            "files": [f.to_dict() for f in self.files],
            "unknowns": self.unknowns,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Inventory":
        return cls(
            root=str(data.get("root", "")),
            files=[SourceFile.from_dict(item) for item in data.get("files", [])],
            unknowns=[str(item) for item in data.get("unknowns", [])],
        )
