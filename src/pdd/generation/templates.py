from __future__ import annotations

from datetime import date

from pdd.inventory.models import Inventory, SourceFile


def _yaml_quote(value: str) -> str:
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def okf_frontmatter(
    *,
    doc_type: str,
    title: str,
    timestamp: str,
    description: str = "",
    resource: str = "",
    tags: list[str] | None = None,
) -> str:
    """Render an Open Knowledge Format (OKF) YAML frontmatter block.

    OKF (Google, Apache-2.0) is a Markdown + YAML-frontmatter convention. Emitting it makes the
    generated documentation a portable, standard artifact that any OKF-aware consumer can read.
    Built as plain text on purpose: the engine keeps zero third-party dependencies.
    """
    lines = ["---", f"type: {doc_type}", f"title: {_yaml_quote(title)}"]
    if description:
        lines.append(f"description: {_yaml_quote(description)}")
    if resource:
        lines.append(f"resource: {_yaml_quote(resource)}")
    if tags:
        lines.append("tags: [" + ", ".join(tags) + "]")
    lines.append(f"timestamp: {timestamp}")
    lines.append("---")
    return "\n".join(lines)


def _today() -> str:
    return date.today().isoformat()


def index_page(
    inventory: Inventory, sources: list[SourceFile], generated_at: str | None = None
) -> str:
    rows = "\n".join(f"- `{item.path}` ({item.kind}, {item.relevance})" for item in sources[:30])
    front = okf_frontmatter(
        doc_type="Concept",
        title="PDD Documentation",
        description="Overview of the documentation generated from the source inventory.",
        resource=inventory.root,
        tags=["pdd", "index"],
        timestamp=generated_at or _today(),
    )
    body = "\n".join(
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
            "Next: read [the source map](sources.md) and [the architecture notes](architecture.md).",
        ]
    )
    return front + "\n" + body + "\n"


def sources_page(sources: list[SourceFile], generated_at: str | None = None) -> str:
    front = okf_frontmatter(
        doc_type="Reference",
        title="Source Map",
        description="Every generated claim must be traceable to these sources.",
        tags=["pdd", "sources"],
        timestamp=generated_at or _today(),
    )
    lines = [front, "", "# Source Map", "", "Every generated claim must be traceable to these sources.", ""]
    for item in sources:
        lines.append(f"- `{item.path}`: {item.title or item.path} [{item.kind}]")
    lines += ["", "See also: [the documentation index](INDEX.md)."]
    return "\n".join(lines) + "\n"


def architecture_page(sources: list[SourceFile], generated_at: str | None = None) -> str:
    front = okf_frontmatter(
        doc_type="Concept",
        title="Architecture Notes",
        description="Source-grounded architecture hints extracted from the inventory.",
        tags=["pdd", "architecture"],
        timestamp=generated_at or _today(),
    )
    code = [item for item in sources if item.kind in {"code", "configuration"}]
    lines = [front, "", "# Architecture Notes", "", "PDD records only source-grounded architecture hints.", ""]
    if not code:
        lines.append("No code or configuration sources were found.")
    for item in code[:30]:
        lines.append(f"- `{item.path}` may describe implementation behavior.")
    lines += ["", "See also: [the documentation index](INDEX.md)."]
    return "\n".join(lines) + "\n"
