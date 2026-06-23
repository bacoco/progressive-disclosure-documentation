# Changelog

## Unreleased

- Generated documentation now carries Open Knowledge Format (OKF) YAML frontmatter
  (`type`, `title`, `description`, `resource`, `tags`, `timestamp`) and cross-links between pages.
  `generate_docs` accepts an optional `generated_at` date for deterministic output. No new
  dependencies (frontmatter is emitted as plain text).

## 0.1.0

- Initial PDD repository scaffold.
- Added inventory, generation, review, and index commands.
- Added artifact contract for `.pdd/` consumers.
