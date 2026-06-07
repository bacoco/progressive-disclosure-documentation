# PDD Concepts

PDD separates documentation work into explicit layers.

- Inventory: what evidence exists.
- Generation: what durable docs are produced from evidence.
- Review: what proof exists that docs are complete and grounded.
- Index: what consumers can search.
- Chat: optional consumer, outside the core engine.

Generated Markdown is a disclosure layer. It helps humans and consumers orient
themselves, but it is not the source of truth. Question-answering consumers must
verify answers against the inventory, source map, review receipts, overrides,
stale-removal records, and original source evidence.

## PDD-IAR Consumers

An investigative retrieval consumer can use PDD artifacts without becoming part
of the PDD core engine:

1. Start with generated documentation for orientation.
2. Follow `source-map.json` to identify supporting evidence.
3. Inspect `inventory.json` for authority, freshness, and version metadata.
4. Check review receipts, overrides, and stale removals before answering.
5. Return an answerability state when evidence is missing or contradictory.
