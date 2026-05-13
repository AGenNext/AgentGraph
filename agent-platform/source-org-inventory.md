# Source Organization Inventory

This records the external repo families mapped into the platform.

## didoneworld

- `didoneworld/Agent-DID`: DID-backed agent identity, blueprints, lifecycle, ownership, permissions.
- `didoneworld/verifiable-credential`: credential issuance, verification, revocation.
- `didoneworld/idwallet`: wallet and credential presentation.
- `didoneworld/platform`: product/integration layer.
- `didoneworld/website`: public website.

## openagx

- `openagx/Agent-Auth`: AuthZEN-style PEP/PDP authorization SDK.
- `openagx/Autonomous-Governance-Protocol`: zero-trust governance, ReBAC, ABAC, drift detection, HITL.
- `openagx/agent-access-protocol`: access protocol placeholder.
- `openagx/Agentic-IGA`: identity governance and administration.
- `openagx/midpoint`: IDM/IGA reference fork.
- `openagx/Cai-Agent`: cybersecurity AI capability.
- `openagx/platform`: platform repo.
- `openagx/website`: website repo.

## AGenNext

- `AGenNext/AgentGraph`: Schema.org implementation platform with databases, graphs, AI agents, and visualization.

## Rule

```text
Use identity and credential repos as external trust inputs.
Use governance repos as policy and lifecycle inputs.
Use Schema.org implementation repos as semantic projection inputs.
```
