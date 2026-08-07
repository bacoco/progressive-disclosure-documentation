# Artifact Contract

PDD consumers should read artifacts from `.pdd/`.

Known consumers and guards:

- [PDG](https://github.com/bacoco/progressive-disclosure-guard) enforces when
  PDD artifacts are required; it must not duplicate this engine.
- [PDD-IAR](https://github.com/bacoco/progressive-disclosure-iar) reads this
  artifact contract to investigate source evidence.

Required artifacts:

- `inventory.json`: scanned source evidence.
- `source-map.json`: generated docs mapped to source evidence.
- `manifest.json`: generation metadata and document list.
- `disclosure.json`: ordered disclosure layers and answering contract.
- `review/coverage.json`: coverage receipt.
- `review/grounding.json`: grounding receipt.
- `review/regression.json`: regression receipt.

Generated Markdown documents carry an Open Knowledge Format (OKF) YAML frontmatter (`type`,
`title`, `description`, `resource`, `tags`, `timestamp`) and cross-links; the `resource` field
points back to the grounding source. This is a convenience for OKF-aware consumers — it does not
change the rule below: consumers must not assume generated Markdown alone is the source of truth.
The `.pdd/` receipts remain the authority on provenance and review.

## Inventory Metadata

Each source entry includes disclosure metadata for consumers:

- `source_type`: normalized source class such as `documentation`,
  `implementation`, or `configuration`.
- `authority`: whether the artifact is `primary`, `derived`, `asset`, or
  `supporting` evidence.
- `freshness`: `current` or `stale`.
- `version`: the first 12 characters of the source hash for compact trace
  display.

## Source Map Sections

`source-map.json` keeps the legacy `documents` mapping and also includes a
`sections` mapping. Section mappings let consumers progressively disclose the
specific evidence behind each generated surface before using it in an answer.

## Answering Contract

`disclosure.json` marks generated docs as non-authoritative. Answering consumers
must verify against `inventory.json`, `source-map.json`,
`review/grounding.json`, `overrides.jsonl`, and `stale-removals.jsonl` before
presenting generated documentation as evidence-backed.
