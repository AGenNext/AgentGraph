# Private Context

Private context is the internal state that belongs to a principal or profile and should not be collapsed into public schema or external protocol claims.

## What It Includes

- work context
- family context
- personal context
- device context
- location context
- time context
- active task state
- recent interactions
- unresolved recovery state
- disclosure policy

## Rule

```text
Public protocols can identify and transport claims.
Only the platform can decide what stays private and what is shared across profiles.
```

## Storage Pattern

- store raw context in ledger-style records
- project only the necessary slices into schemafull operational views
- keep sensitive context behind policy and field permissions
- link context to principal, profile, time, and purpose

## Platform Mapping

| Concept | Primitive |
|---|---|
| private state | `ap:ContextFrame` |
| disclosure rules | `ap:PolicyCheck` |
| sensitive material | field permissions |
| profile overlays | `ap:AgentProfile` |
| cross-profile sharing | controlled context layer |
