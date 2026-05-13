# Audit

Audit is the durable record of what happened, who did it, when it happened, and why.

## Audit Requirements

- principal or subject
- profile in use
- requested action
- resource or target
- policy decision
- trust state
- intervention state
- commit result
- timestamps
- evidence and rationale

## Rule

```text
If a decision can affect safety, authority, disclosure, money, or recovery, it must be auditable.
```

## Platform Mapping

| Concept | Primitive |
|---|---| 
| audit entry | `ledger_entry` |
| execution trace | `ap:ProcessingState` |
| rationale | `ap:ReasoningTrace` |
| evidence link | relation edges |
| outcome | `ap:Outcome` |

## Storage Pattern

- keep immutable audit history in the ledger
- project summaries into operational views
- never rely on only the latest row for accountability
