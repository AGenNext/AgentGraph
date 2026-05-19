# Recovery State

Recovery state records failed, interrupted, or partially completed work so the system can continue safely.

## What It Tracks

- failure cause
- interrupted step
- last known good state
- retry status
- human decision
- rollback scope
- remediation path
- restart cursor

## Rule

```text
Failure should become durable state.
Durable state lets the platform recover instead of guessing.
```

## Platform Mapping

| Concept | Primitive |
|---|---|
| retryable failure | `ap:RecoveryState` |
| incident | `ap:Incident` |
| resume cursor | `ap:ProcessingState` |
| rollback path | transaction / cancel |
| emergency stop | `ap:EmergencyStop` |

## Lifecycle

1. detect failure or interruption
2. record recovery state
3. prevent unsafe continuation
4. route to worker or human review
5. resume from the last safe checkpoint
