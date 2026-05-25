from __future__ import annotations

import sqlite3
from pathlib import Path


def search(index_path: str | Path, query: str, limit: int = 5) -> list[dict[str, object]]:
    conn = sqlite3.connect(index_path)
    conn.row_factory = sqlite3.Row
    try:
        try:
            rows = conn.execute(
                """
                SELECT d.path, snippet(docs_fts, 1, '[', ']', '...', 8) AS snippet
                FROM docs_fts f
                JOIN docs d ON d.id = f.rowid
                WHERE docs_fts MATCH ?
                LIMIT ?
                """,
                (query, limit),
            ).fetchall()
        except sqlite3.OperationalError:
            rows = []
        return [dict(row) for row in rows]
    finally:
        conn.close()
