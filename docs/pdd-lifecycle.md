# PDD Lifecycle

1. Scan a repository with `pdd inventory`.
2. Generate or convert documentation.
3. Review coverage, grounding, and regression.
4. Index the generated documentation.
5. Let chat or portal consumers use the artifacts.

Updates must preserve human overrides and report stale removals.

Consumers should treat the lifecycle as progressive disclosure: orient on the
generated docs, verify against source maps and review receipts, then inspect
source evidence before answering.
