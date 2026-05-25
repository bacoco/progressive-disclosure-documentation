from __future__ import annotations

import sqlite3
from pathlib import Path


def build_index(docs_dir: str | Path, out_path: str | Path) -> dict[str, object]:
    docs_root = Path(docs_dir)
    target = Path(out_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target)
    try:
        conn.executescript(
            """
            DROP TABLE IF EXISTS docs;
            DROP TABLE IF EXISTS docs_fts;
            CREATE TABLE docs(id INTEGER PRIMARY KEY, path TEXT NOT NULL, content TEXT NOT NULL);
            CREATE VIRTUAL TABLE docs_fts USING fts5(path, content, content='docs', content_rowid='id');
            """
        )
        count = 0
        for path in sorted(docs_root.glob("*.md")):
            content = path.read_text(encoding="utf-8", errors="replace")
            cur = conn.execute("INSERT INTO docs(path, content) VALUES (?, ?)", (path.name, content))
            conn.execute(
                "INSERT INTO docs_fts(rowid, path, content) VALUES (?, ?, ?)",
                (cur.lastrowid, path.name, content),
            )
            count += 1
        conn.commit()
        return {"schema": "pdd.index.v1", "path": str(target), "documents": count}
    finally:
        conn.close()
