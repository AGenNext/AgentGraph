# Surreal Runtime Agent Guide

This file is for anyone modifying the SurrealDB runtime layer in `Agent-Graph`.

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

They must be represented as native runtime and schema concerns from the start.
By default, time and location should be present on every object unless there is
a concrete reason not to model them.

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
must be modeled as a new event in forward time, not as deletion of what
happened before.

Immutable audit logs are mandatory.

Audit history must be append-only and generated at input, processing, and
output levels at every stage, including LLM streaming. Material events are not
silently rewritten or erased. Corrections, reversions, compensations, and
policy actions must be modeled as new audit events in forward time. This audit
layer exists not only for governance and security, but also to debug and
improve LLM behavior over time.

## Core Rule

The project is SurrealDB-native.

If a behavior can be expressed cleanly with standard SurrealDB features, it
should be implemented in SurrealQL before adding Python-side logic.

## Preread

Preread is mandatory before making runtime-layer changes.

Review:

- SurrealDB documentation
- official SurrealDB examples
- relevant SurrealDB tutorials
- Entra Agent Identity and Lifecycle Management requirements
- Governance Tool Kit requirements
- A2A protocol requirements and runtime implications

## What You Own Here

When working inside `surreal/`, prefer changing:

- `runtime-schema.surql`
- `runtime-functions.surql`
- `runtime-events.surql`
- `schema/` assets when the imported Schema.org layer itself must change

## What You Should Avoid

- Re-implementing DB rules in `server.py`
- Creating duplicate state rules in Python and SurrealDB
- Reshaping the imported Schema.org graph without a strong reason
- Adding custom extensions before exhausting standard SurrealDB features

## Decision Order

Use this order when deciding where logic belongs:

1. `DEFINE TABLE` / `DEFINE FIELD` / `DEFINE INDEX`
2. `DEFINE FUNCTION`
3. `DEFINE EVENT`
4. thin application orchestration in Python
5. advanced extensibility only if standard features are insufficient

## Runtime Boundaries

SurrealDB should own:

- runtime persistence
- graph relations
- version history mechanics
- DB-side defaults and mutation behavior
- reusable query and mutation functions

Python should own:

- HTTP transport
- auth and request handling
- external API and service integration
- UI-facing response shaping

## File Intent

- `runtime-schema.surql`: runtime structure
- `runtime-functions.surql`: reusable runtime operations
- `runtime-events.surql`: mutation side effects and history behavior
- `schema/schemaorg-paths.surql`: materialized direct and multi-step relation paths
- `knowledge-graph.surql`: seeded semantic graph for the repository
- `schema/schema-meta.surql`: Schema.org metamodel
- `schema/schemaorg-vocabulary.surql`: generated vocabulary graph

## Before You Add New Logic

Ask:

1. Can this be solved with plain SurrealQL?
2. Should this be schema, function, or event logic?
3. Would this duplicate behavior already owned by the database?
4. Does this preserve the current abstraction?

## Expected Outcome

The long-term target is a thin API layer over a SurrealDB-owned runtime model.
