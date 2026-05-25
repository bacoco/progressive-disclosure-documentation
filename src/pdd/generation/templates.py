from __future__ import annotations

from pdd.inventory.models import Inventory, SourceFile


def index_page(inventory: Inventory, sources: list[SourceFile]) -> str:
    rows = "\n".join(f"- `{item.path}` ({item.kind}, {item.relevance})" for item in sources[:30])
    return "\n".join(
        [
            "# PDD Documentation",
            "",
            "This documentation was generated from a PDD source inventory.",
            "",
            "## Source Summary",
            "",
            f"- Repository root: `{inventory.root}`",
            f"- Source files: {len(inventory.files)}",
            f"- Unknowns: {len(inventory.unknowns)}",
            "",
            "## Primary Sources",
            "",
            rows or "- No eligible sources found.",
            "",
            "Next: read `sources.md` for the full source map.",
        ]
    )


def sources_page(sources: list[SourceFile]) -> str:
    lines = ["# Source Map", "", "Every generated claim must be traceable to these sources.", ""]
    for item in sources:
        lines.append(f"- `{item.path}`: {item.title or item.path} [{item.kind}]")
    return "\n".join(lines) + "\n"


def architecture_page(sources: list[SourceFile]) -> str:
    code = [item for item in sources if item.kind in {"code", "configuration"}]
    lines = ["# Architecture Notes", "", "PDD records only source-grounded architecture hints.", ""]
    if not code:
        lines.append("No code or configuration sources were found.")
    for item in code[:30]:
        lines.append(f"- `{item.path}` may describe implementation behavior.")
    return "\n".join(lines) + "\n"
