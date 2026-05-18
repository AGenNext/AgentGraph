# SurrealDB Runtime Layer

This directory is the canonical database layer for `Agent-Graph`.

The project is SurrealDB-native. Runtime structure, persistence rules, and
database-owned behavior should be defined here first, then consumed by the
application layer. Python should remain a thin transport and integration layer,
not the source of truth for runtime state rules.

## Core Objective

Build a best-in-class Schema.org-based multimodal graph neural runtime where
humans and agents share the same semantic language, with database and server
merged into one SurrealDB-native layer, and with schema design aligned to
natural human language to minimize conversion loss from intent to schema to
code. There is no compromise in security: all runtime design and
implementation must adhere to agent security, safety, governance, relevant
security frameworks, and best-in-class database management protocols.

## World Model

Humans are not outside the system.

Humans and agents are first-class participants in the same runtime world, with
identity, state, governance, and interaction modeled inside the system rather
than around it.

Time and location are primitives.

They must be represented as native elements of the runtime model and schema,
not treated as optional metadata or post-processing concerns. By default, time
and location should be present on every object unless there is a concrete
reason not to model them.

Time moves forward only.

The runtime should model time the way real-world events progress. Temporal
reversal or world-order overrides are not allowed unless explicitly authorized
by the user.

The world does not stop because one node has gone down.

The system must assume partial failure and continuity. Data continuity relies
on the database and distributed layer, and service recovery relies on
Kubernetes self-healing rather than global pause semantics. Kubernetes
self-healing is mandatory for the production world model. Production failure is
not an acceptable stopping condition; the world must keep moving.

If changes are reverted, they are reverted at a later time.

Reversion does not erase time. Any rollback, compensation, or corrective action
must be represented as a new event in forward time, not as deletion of prior
reality.

Immutable audit logs are mandatory.

Audit history must be append-only and generated at input, processing, and
output levels at every stage, including LLM streaming. Material events are not
silently rewritten or erased. Corrections, reversions, compensations, and
policy actions must be represented as new audit events in forward time. This
audit layer exists not only for governance and security, but also to debug and
improve LLM behavior over time.

## Goals

- Keep Schema.org vocabulary storage native to SurrealDB.
- Keep runtime persistence and mutation logic native to SurrealDB where possible.
- Preserve the imported Schema.org graph structure.
- Extend the model without creating a parallel Python-owned state system.
- Prefer standard SurrealDB features over custom application-side logic.

## Preread

Preread is mandatory before making runtime-layer changes.

Contributors must review:

- SurrealDB documentation
- official SurrealDB examples
- relevant SurrealDB tutorials
- Entra Agent Identity and Lifecycle Management requirements
- Governance Tool Kit requirements
- A2A protocol requirements and runtime implications

## Directory Ownership

### `schema/`

Canonical imported Schema.org assets.

- `schema/schemaorg-current-https.jsonld`
  Upstream Schema.org vocabulary dump.
- `schema/schema-meta.surql`
  SurrealDB metamodel for vocabulary storage.
- `schema/schemaorg-vocabulary.surql`
  Generated SurrealQL import of types, properties, values, and relations.
- `schema/schemaorg-summary.json`
  Generated term and edge counts for verification.

### `generate_schemaorg_surql.py`

Generator that converts the upstream JSON-LD dump into SurrealQL.

### `runtime-schema.surql`

Runtime tables, fields, indexes, and graph relations owned by the platform.

This is where to define:

- tables such as `agent`, `agent_version`, `entity`
- typed fields
- indexes
- runtime relation tables

### `runtime-functions.surql`

Reusable SurrealQL functions for runtime reads and mutations.

This is where to define:

- DB-native query helpers
- upsert helpers
- restore/version operations
- reusable mutation logic that should not be duplicated in Python

### `runtime-events.surql`

Database-native mutation side effects.

This is where to define:

- automatic version snapshots
- timestamp/default behavior
- other mutation-driven rules that belong inside the database transaction

### `knowledge-graph.surql`

Seeded semantic graph for the repository.

This file connects repository concepts into a durable SurrealDB graph using
the runtime tables and relation types defined above. It is the canonical
starting point for local graph bootstrap and repository-level semantic
navigation.

## Working Rules

1. Do not put core runtime rules in `server.py` if they can live in SurrealQL.
2. Do not duplicate versioning logic in Python and SurrealDB.
3. Keep Schema.org import assets distinct from runtime platform assets.
4. Preserve existing Surreal structure instead of inventing parallel models.
5. Prefer `DEFINE TABLE`, `DEFINE FIELD`, `DEFINE INDEX`, `DEFINE FUNCTION`,
   and `DEFINE EVENT` before adding custom application logic.
6. Use record links or graph relations intentionally. Avoid redundant
   representations unless there is a clear reason.
7. Keep runtime abstractions stable even if implementation moves deeper into
   SurrealDB.

## Preferred Architecture

- SurrealDB owns runtime state, graph structure, and DB-native behavior.
- Application code exposes HTTP and integrates external systems.
- Schema and runtime assets are applied from this directory, not rebuilt ad hoc
  in request handlers.

## Apply Order

When applying assets, use this order:

1. `schema/schema-meta.surql`
2. `schema/schemaorg-vocabulary.surql`
3. `runtime-schema.surql`
4. `runtime-functions.surql`
5. `runtime-events.surql`
6. `schema/schemaorg-paths.surql`
7. `knowledge-graph.surql`

Use the SurrealKit wrappers in `scripts/` to lint and apply the directory:

```bash
SURREALDB_URL=... SURREALDB_DATABASE=... SURREALDB_NAMESPACE=... SURREALDB_USER=... SURREALDB_PASS=... ./scripts/surrealkit-lint.sh
SURREALDB_URL=... SURREALDB_DATABASE=... SURREALDB_NAMESPACE=... SURREALDB_USER=... SURREALDB_PASS=... ./scripts/surrealkit-apply.sh
```

## Tooling Guidance

- Prefer SurrealQL for schema and runtime logic.
- Prefer SurrealKit for applying and managing database assets.
- Use SurrealML only when a real model/inference use case exists.
- Avoid JS/WASM extensions unless standard SurrealDB features are insufficient.

## What Does Not Belong Here

- HTTP route handling
- frontend state logic
- provider SDK orchestration
- channel integration glue
- unrelated application configuration

## Vocabulary Model

The imported Schema.org vocabulary is represented as:

- `schema_term`
  All schema terms in one table with a `term_kind`.
- relation tables
  `subclass_of`, `subproperty_of`, `domain_includes`, `range_includes`,
  `inverse_of`, `superseded_by`, `equivalent_to`, `exact_match`

## Contributor Checklist

Before adding new runtime behavior:

1. Decide whether it belongs in schema, function, or event files.
2. Confirm the behavior cannot be expressed cleanly with standard SurrealDB features.
3. Keep the runtime abstraction intact.
4. Avoid moving ownership back into Python without a concrete reason.
