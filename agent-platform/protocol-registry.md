# Protocol Registry

Protocols are adapters around the platform primitives.

## Core Map

| Protocol | Layer | Platform mapping |
|---|---|---|
| JSON-LD | semantic data | `ledger_entry.payload`, `ap:*`, schema.org compatibility |
| schema.org | semantic vocabulary | public entities, actions, events, places, media |
| DID Core | identity | decentralized identifiers, verification methods, service endpoints |
| Verifiable Credentials | identity/evidence | issuer, holder, verifier, proof, status |
| Agent-DID | agent identity | DID-backed agent records, blueprints, lifecycle, permissions |
| OAuth2 / OIDC | authentication | provider binding, sessions, claims |
| JWT / JWKS | token verification | signed claims, key discovery |
| AuthZEN | authorization exchange | subject, action, resource, context, decision |
| A2A | agent communication | delegation, messages, tasks, artifacts |
| MCP | tool/context protocol | tools, resources, prompts, sampling |
| SurrealQL | database language | records, graph, vector, search, time, geo, transactions |
| Live Query / changefeed | realtime and replay | committed notifications and durable history |
| REST / GraphQL | integration APIs | controlled read/admin surfaces over hardened projections |
| MIME / URI | artifact addressing | multimodal artifacts, source refs, service refs |

## Boundaries

- Identity protocols prove claims about a subject.
- Authorization protocols decide whether a caller may act now.
- SurrealDB remains the state boundary.
- `ap:*` remains the meaning, authority, trust, intervention, and recovery layer.

## Rule

```text
A protocol can identify, carry, or verify data.
It cannot silently become authority.
```
