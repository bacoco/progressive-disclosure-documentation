# AGENTS.md

Instructions for agents working in this repository.

## Core Boundary

PDD is the documentation engine. Do not turn this repository into a chatbot
application. Chat applications must consume PDD artifacts through files or API
adapters.

## Required Constraints

- Preserve `.pdd/` artifact contracts unless a migration is documented.
- Keep generated docs source-grounded through inventory and source-map files.
- Do not add project-specific branding, pages, or question banks to `src/pdd`.
- Do not create a parallel documentation engine in examples or chat adapters.
- Keep new files focused and normally below 200 lines.

## Verification

Run:

```bash
python -m pip install -e ".[test]"
python -m pytest
pdd inventory --repo examples/minimal-repo --out /tmp/pdd/inventory.json
pdd generate --inventory /tmp/pdd/inventory.json --out /tmp/pdd/docs
pdd review --docs /tmp/pdd/docs --inventory /tmp/pdd/inventory.json --out /tmp/pdd/review
```
