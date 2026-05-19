# Trust Control

Trust is dynamic autonomy control.

It is not identity, and it is not a permanent label.

## Purpose

Trust answers how much this caller, profile, device, model, or capability may do right now.

## Inputs

- identity assurance
- session age and freshness
- prior policy violations
- incident history
- sponsor or owner approval
- device posture
- location and time signals
- data sensitivity
- capability provenance
- recent recovery state

## Outputs

- raise autonomy
- lower autonomy
- sandbox capability
- require intervention
- block action
- require re-authentication

## Rule

```text
Identity proves who.
Trust limits autonomy.
Policy decides the action.
```

## Platform Mapping

| Concept | Primitive |
|---|---|
| trust score | `ap:TrustControl` |
| current risk | `ap:RiskAssessment` |
| revocation | `ap:DecisionOverride` |
| emergency stop | `ap:EmergencyStop` |
| blocked state | `ap:LifecycleState` |
