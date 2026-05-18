# Agent-Graph Repo Guide

## Project Context

**Repository:** /Users/apple/Agent-Graph
**Purpose:** Backend graph source of truth for the AGenNext stack, including the optional shared schema package, SurrealDB graph assets, backend APIs, validation harnesses, and the packaged Python SDK.

## Current Focus

Keep the repository source of truth in git, and keep the generated SurrealDB assets, live database behavior, and tests aligned.
Treat this repo as a composable schema package: services may adopt it, extend it, or bring their own schema, but nothing should be forced into a bundled dependency graph.

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
| `surreal/validation/graph-validation.surql` | SurrealDB-native validation blocks |
| `surreal/knowledge-graph.surql` | Repository knowledge graph seed |
| `REPO_LAYOUT.md` | Repo boundary contract for graph/runtime/identity/auth/protocols |
| `tests/test_database.py` | Static asset validation |
| `tests/test_surrealdb_integration.py` | Disposable SurrealDB integration validation |
| `scripts/surrealkit-lint.sh` | SurrealKit lint wrapper |
| `scripts/surrealkit-apply.sh` | SurrealKit apply wrapper |

## Mandatory Preread

Before working on runtime, database, schema, identity, governance, or protocol-layer code, load:

- `surreal/README.md`
- `surreal/AGENT.md`
- `REPO_LAYOUT.md`

These files are the local source of truth for the SurrealDB runtime model and must be followed for changes in:

- SurrealDB schema or graph relations
- Schema.org vocabulary or path generation
- runtime functions or events
- knowledge graph seeding
- identity, governance, or protocol behavior
- backend/runtime boundary changes

## Working Rules

- Keep generated SurrealQL assets deterministic and checked into git.
- Re-run the relevant generator before committing changes to `surreal/schema/schemaorg-vocabulary.surql` or `surreal/schema/schemaorg-paths.surql`.
- Prefer disposable testcontainers validation for live database checks.
- Use `RELATE` for graph edges and record links for direct node references.
- Treat `route` as the relation-name chain and `path` as the exact record chain.
- Do not introduce new runtime or schema files without a clear reason.
- Child repo schemas may extend the shared base schema, but every schema must remain Agent-Graph-compatible.
- Everything must remain composable; do not introduce forced bundling between services.
- Hosted services such as WaltID, external LLMs, cloud storage, and similar integrations should be wired through `Agent-Environment` and environment variables rather than hardcoded into `Agent-Runtime`.
- The base schema is core IP; child repos and external vendors may extend it for their own use cases, but those extensions should remain Agent-Graph-compatible and only be absorbed into the core when they fit the platform's own repo and IP strategy.
- The shared schema package is optional at the service level: a service may adopt `Agent-Graph`, extend it, or use its own schema entirely, so long as anything it uses remains compatible with the shared contract when integration is desired.
- Treat `core/`, `a2a/`, `agents/`, and `agentnext/` as migration targets outside the long-term Agent-Graph package boundary; do not grow new features there unless the work is explicitly part of the extraction plan.
- For every code change, first use an existing source reference from the current GitHub repo if one exists; if not, validate against the current code path and update the implementation or tests accordingly.

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

- The integration harness now validates Schema.org relation tables, path materialization, and the repository knowledge graph through SurrealDB-native validation blocks in a disposable container.
- Keep repo documentation aligned with the current SurrealDB-native layout.

*Last updated: 2026-05-17*
