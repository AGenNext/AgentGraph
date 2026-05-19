# Intervention Gates

Intervention gates are the pause points in the platform.

They let the system stop before a risky write, disclosure, external action, or autonomous continuation.

## Gate Types

- pre_ingest
- pre_validate
- pre_save
- pre_project
- pre_execute
- pre_disclose
- post_commit
- live_review

## Rule

```text
Any sensitive or irreversible step can be interrupted.
The interruption can happen before the database write, after the write, or before any external effect.
```

## Gate Outcomes

- allow
- deny
- pause
- escalate
- redact
- sandbox

## Platform Mapping

| Concept | Primitive |
|---|---| 
| gate record | `ap:InterventionGate` |
| human decision | `ap:InterventionDecision` |
| approval | `ap:ApprovalDecision` |
| request | `ap:ApprovalRequest` |
| interruption trace | `ap:ProcessingState` |

## Operational Rule

```text
The gate is not a dead end.
It is a controlled handoff to policy, human review, or recovery.
```
