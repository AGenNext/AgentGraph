# Agent Platform Core Map

This directory captures the platform overlay for agent identity, authority, policy, trust, intervention, and protocol mapping.

## Layers

- `schema.org` and JSON-LD for the public semantic layer.
- SurrealDB for storage, graph, realtime, search, vector, time-series, auth, and transactions.
- `ap:*` for private context, authority, trust, intervention, recovery, and responsibility.
- External protocols such as DID, VC, OIDC, AuthZEN, A2A, and MCP as adapters around the control plane.

## Core Documents

- `protocol-registry.md`
- `source-org-inventory.md`
- `identity-access-policy.md`
- `schema-management.md`
- `time-series-strategy.md`
- `graph-modeling.md`
- `document-model-patterns.md`
- `realtime-data.md`
- `security-enforcement.md`

## Rule

```text
SurrealDB stores and enforces state.
ap:* defines meaning and governance.
Protocols move data or prove claims, but they do not replace the ontology.
```
