from __future__ import annotations

from pdd.inventory.models import Inventory, SourceFile


def selected_sources(inventory: Inventory) -> list[SourceFile]:
    files = [f for f in inventory.files if not f.binary_asset and not f.generated]
    return sorted(files, key=lambda f: (f.kind != "documentation", f.path))


def by_kind(inventory: Inventory) -> dict[str, list[SourceFile]]:
    groups: dict[str, list[SourceFile]] = {}
    for source in selected_sources(inventory):
        groups.setdefault(source.kind, []).append(source)
    return groups
