# Artifact Contract

PDD consumers should read artifacts from `.pdd/`.

Required artifacts:

- `inventory.json`: scanned source evidence.
- `source-map.json`: generated docs mapped to source evidence.
- `manifest.json`: generation metadata and document list.
- `review/coverage.json`: coverage receipt.
- `review/grounding.json`: grounding receipt.
- `review/regression.json`: regression receipt.

Consumers must not assume generated Markdown alone is the source of truth.
