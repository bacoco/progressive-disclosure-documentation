# Artifact Contract

PDD consumers should read artifacts from `.pdd/`.

Required artifacts:

- `inventory.json`: scanned source evidence.
- `source-map.json`: generated docs mapped to source evidence.
- `manifest.json`: generation metadata and document list.
- `review/coverage.json`: coverage receipt.
- `review/grounding.json`: grounding receipt.
- `review/regression.json`: regression receipt.

Generated Markdown documents carry an Open Knowledge Format (OKF) YAML frontmatter (`type`,
`title`, `description`, `resource`, `tags`, `timestamp`) and cross-links; the `resource` field
points back to the grounding source. This is a convenience for OKF-aware consumers — it does not
change the rule below: consumers must not assume generated Markdown alone is the source of truth.
The `.pdd/` receipts remain the authority on provenance and review.
