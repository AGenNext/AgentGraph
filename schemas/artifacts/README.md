# Artifact Schemas

This directory defines artifact schemas only.

Agent-Graph is used here as the schema layer for generated artifacts. It does not implement runtime generation, orchestration, execution, or business logic in this scope.

## Scope

Schema-only definitions for:

- artifact jobs
- artifact plans
- artifact versions
- artifact sections
- citations
- evaluations
- source dependencies
- artifact-specific payloads

## Non-Scope

This package does not currently implement:

- artifact generation workers
- LangGraph execution graphs
- model/provider orchestration
- UI rendering
- export engines
- billing
- tenant administration

## Relationship to Agent Knowledge

Agent Knowledge is the product/backend platform.

Agent-Graph provides reusable artifact schemas that Agent Knowledge can consume.

```text
Agent Knowledge
  → source memory
  → extraction
  → knowledge graph
  → artifact generation
  → evaluation

Agent-Graph
  → artifact schemas only
```

## Design Principle

Artifact schemas must preserve:

- source provenance
- source version dependencies
- citations
- evaluation status
- artifact versioning
- extensibility for future artifact types
