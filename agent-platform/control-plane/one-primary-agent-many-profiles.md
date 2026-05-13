# One Primary Agent, Many Profiles

The platform assumes one primary agent per person, with multiple profiles for different contexts.

## Profiles

- work
- family
- personal
- child-care
- community
- research
- operations

## Rule

```text
One person owns one primary agent.
Profiles specialize the same owner into separate contexts and authority scopes.
```

## What Profiles Share

- identity root
- some long-lived memory
- sponsor/owner binding
- recovery lineage
- audit lineage

## What Profiles Do Not Share By Default

- authority scopes
- disclosure rules
- private context slices
- tool permissions
- trust level
- irreversible state changes

## Platform Mapping

| Concept | Primitive |
|---|---|
| primary agent | `ap:Principal` |
| profile | `ap:AgentProfile` |
| profile overlay | `ap:ContextFrame` |
| shared memory | `ledger_entry` |
| scoped access | `ap:AuthorityScope` |
| profile decision | `ap:PolicyCheck` |
