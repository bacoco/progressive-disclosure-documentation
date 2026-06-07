# PDD - Progressive Disclosure Documentation

PDD is a documentation engine for creating, converting, updating, reviewing,
indexing, and serving progressive documentation artifacts.

PDD is not a chatbot. A chatbot can consume PDD artifacts, but the engine must
work on its own.

## Relationship To PDG

PDG is the agent guardrail. PDD is the documentation engine.

Use PDG to decide when durable documentation work must go through PDD. Use PDD
to produce the actual source inventory, documentation, review receipts, stale
removals, human override records, and searchable index.

## Relationship To Chatbots

A PDD chatbot should consume `.pdd/` artifacts instead of rebuilding its own
documentation pipeline:

```text
PDG frames the work -> PDD produces artifacts -> PDD Chat consumes artifacts
```

## Quickstart

```bash
python -m pip install -e ".[test]"
python -m pytest
pdd inventory --repo . --out .pdd/inventory.json
pdd generate --inventory .pdd/inventory.json --out docs/pdd
pdd review --docs docs/pdd --inventory .pdd/inventory.json --out .pdd/review
pdd index --docs docs/pdd --out .pdd/index.sqlite
```

## Lifecycle

- `inventory`: scan a repository and classify source files.
- `generate`: create PDD documentation from an inventory.
- `convert`: convert existing docs into PDD-shaped documentation.
- `update`: regenerate only the PDD surfaces from current evidence.
- `review`: produce coverage, grounding, and regression receipts.
- `index`: build a local SQLite FTS index for consumers such as chat apps.

## Artifacts

PDD writes machine-readable artifacts under `.pdd/`:

```text
.pdd/
  inventory.json
  source-map.json
  manifest.json
  disclosure.json
  overrides.jsonl
  stale-removals.jsonl
  review/
    coverage.json
    grounding.json
    regression.json
  index.sqlite
```

Generated documentation is a disclosure surface, not the source of truth. Consumers
that answer questions must verify generated claims against `inventory.json`,
`source-map.json`, review receipts, overrides, stale removals, and the original
sources.

## Non-Goals

- No required chatbot.
- No project-specific branding.
- No project-specific question banks in core.
- No silent overwrite of human overrides.
