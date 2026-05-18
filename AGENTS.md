# Agent-Graph Repo Guide

## Project Context

**Repository:** /Users/apple/Agent-Graph
**Purpose:** SurrealDB-native agent/runtime platform with Schema.org graph assets, runtime schema, and validation harnesses.

## Current Focus

Keep the repository source of truth in git, and keep the generated SurrealDB assets, live database behavior, and tests aligned.

## Key Files

| Path | Purpose |
|------|---------|
| `server.py` | Runtime server and SurrealDB bootstrapping |
| `main.py` | Application entrypoint |
| `surreal/README.md` | SurrealDB asset and workflow guide |
| `surreal/AGENT.md` | SurrealDB runtime constraints |
| `surreal/runtime-schema.surql` | Core runtime schema |
| `surreal/schema/schema-meta.surql` | Schema term definitions and relation tables |
| `surreal/schema/schemaorg-vocabulary.surql` | Generated Schema.org vocabulary |
| `surreal/schema/schemaorg-paths.surql` | Generated multi-step relation paths |
| `surreal/knowledge-graph.surql` | Repository knowledge graph seed |
| `tests/test_database.py` | Static asset validation |
| `tests/test_surrealdb_integration.py` | Disposable SurrealDB integration validation |
| `scripts/surrealkit-lint.sh` | SurrealKit lint wrapper |
| `scripts/surrealkit-apply.sh` | SurrealKit apply wrapper |

## Mandatory Preread

Before working on runtime, database, schema, identity, governance, or protocol-layer code, load:

- `surreal/README.md`
- `surreal/AGENT.md`

These files are the local source of truth for the SurrealDB runtime model and must be followed for changes in:

- SurrealDB schema or graph relations
- Schema.org vocabulary or path generation
- runtime functions or events
- knowledge graph seeding
- identity, governance, or protocol behavior

## Working Rules

- Keep generated SurrealQL assets deterministic and checked into git.
- Re-run the relevant generator before committing changes to `surreal/schema/schemaorg-vocabulary.surql` or `surreal/schema/schemaorg-paths.surql`.
- Prefer disposable testcontainers validation for live database checks.
- Use `RELATE` for graph edges and record links for direct node references.
- Treat `route` as the relation-name chain and `path` as the exact record chain.
- Do not introduce new runtime or schema files without a clear reason.

## Validation

Recommended checks for SurrealDB work:

```bash
python3 -m pytest -q tests/test_database.py tests/test_surrealdb_integration.py
python3 -m pytest -q
```

If SurrealKit is used, validate the wrapper scripts first:

```bash
./scripts/surrealkit-lint.sh
./scripts/surrealkit-apply.sh
```

## Notes

- The integration harness currently validates Schema.org relation tables and path materialization in a disposable SurrealDB container.
- Knowledge graph validation is a separate concern and may require its own targeted test if the schema changes.
- Keep repo documentation aligned with the current SurrealDB-native layout.

*Last updated: 2026-05-17*
