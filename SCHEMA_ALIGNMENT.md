# Schema.org Platform Alignment

> How all AGenNext repos should follow Schema.org for interoperability

## ⚠️ COMMON BRANCH: `schema-org-implementation`

### ONE PLATFORM (6 COMPONENTS)

| Component | File | Purpose | Repo |
|-----------|------|---------|------|
| **ONE DB** | *_database.py | 22 domains | THIS REPO |
| **ONE SCHEMA** | base_entity.py | SoftwareApplication | THIS REPO |
| **ONE IDENTITY** | waltid_endpoints.py | DID + VC | THIS REPO |
| **ONE AUTH** | opa_sdk.py | OPA | THIS REPO |
| **ONE FGA** | a2a_sdk.py | A2A | THIS REPO |
| **ONE UI** | nextjs-website/ | Website | THIS REPO |

### ONE REPO FOR EACH THING

| Repo | Role | Keep There |
|------|------|----------|
| **AGenNext-Enterprise** | CORE (DB, Schema, ID, Auth, FGA, UI) | ✅ |
| **AGenNext-Protocols** | Protocols | ✅ |
| **AGenNext-SkillRegistry** | Skills | ✅ |
| **AGenNext-CodeReview** | Code Review Agent | ✅ |
| **agent-studio** | Studio UI | ✅ |
| **agent-kube** | K8s Deploy | ✅ |
| **agent-harness** | Runtime | ✅ |
| **agent-runner** | Execution | ✅ |

### TO CLEANUP (80 repos - DO NOT DELETE)

**DO NOT DELETE ANYTHING** - Document purpose only:

| Potential Role | Candidate Repos |
|----------------|------------------|
| **AGENT** | AgentGraph, AgentID, AutoGen, CrewAI, AgentCrew |
| **UI** | Agent-Chat-Ui, AgentChat, website, agent-studio |
| **DEPLOY** | agent-kube, code-deploy, agent-starter-pack |
| **RUNTIME** | agent-harness, agent-runner, Runner |
| **MCP** | mcp-registry, MCP-Agent |
| **FRAMEWORKS** | Agent-Frameworks, Microsoft-Agent-Framework |
| **TOOLS** | tools, feature-store, model-gateway |

## Problem

Current 88 repos don't use consistent data schemas. Each repo has its own models.

## Solution: Schema.org Alignment

All AGenNext repos should use Schema.org types for data interoperability.

### Core Types (in AGenNext-Enterprise)

| Schema.org Type | File | Purpose |
|--------------|------|--------|
| **SoftwareApplication** | base_entity.py | Agent definition |
| **Person** | person_organization.py | User/owner |
| **Organization** | person_organization.py | Team/company |
| **CreativeWork** | knowledge_graph.py | Knowledge base |
| **Action** | action_mapper.py | Skills/actions |
| **Thing** | base_entity.py | Base entity |

### Database Types (22 domains)

| Schema.org Type | Database |
|--------------|----------|
| Automotive | automotive_database.py |
| BankingAccount | banking_database.py |
| Healthcare | healthcare_database.py |
| ... | ... |

---

## Repo Alignment Map

### AGenNext-Enterprise ← CORE
```
Uses: SoftwareApplication, Person, Organization, Thing
Files: base_entity.py, *_database.py, waltid_*.py
```

### AGenNext-Protocols ← PROTOCOLS
```
Should Use: Action, Event, Thing
Align: Protocol definitions as Schema.org Actions
```

### AGenNext-SkillRegistry ← SKILLS
```
Should Use: definedTerm, Pronunciation, Thing
Align: Skills as Schema.org definedTerm
```

### AgentID ← IDENTITY
```
Should Use: Person, Organization, Thing
Align: DIDs → Schema.org Person.identifier
```

### agent-studio ← UI
```
Should Use: SoftwareApplication, WebPage
Align: UI components as Schema.org CreativeWork
```

### agent-kube ← INFRA
```
Should Use: SoftwareApplication, Container, ComputedService
Align: K8s as Schema.org computedService
```

---

## Alignment Checklist

| Repo | Schema.org Type | Status | Action |
|------|-------------|--------|--------|
| Enterprise | SoftwareApplication | ✅ | Reference |
| Protocols | Action | ⬜ | Add Schema.org imports |
| SkillRegistry | definedTerm | ⬜ | Map skills |
| AgentID | Person.identifier | ⬜ | Add DID mapping |
| agent-studio | SoftwareApplication | ⬜ | Use base_entity |
| agent-kube | ComputedService | ⬜ | Add schema mapping |

---

## Implementation

### Option 1: Import from Enterprise

```python
# In other repos, add dependency
from agennext_enterprise import Entity, SoftwareApplication
```

### Option 2: Use Schema.org JSON-LD

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Agent Graph",
  "applicationCategory": "https://schema.org/AIAgent"
}
```

### Option 3: Reference Only

```python
# Document alignment without code dependency
AGENT_SCHEMA = "SoftwareApplication"
```

---

## Reference

- **Schema Source**: `schema-org-implementation` branch in AGenNext-Enterprise
- **Common Types**: base_entity.py (SoftwareApplication, Person, Thing)
- **Database Types**: 22 × *_database.py
- **Reference**: https://github.com/AGenNext/AGenNext-Enterprise/blob/schema-org-implementation/base_entity.py
- **Discussion**: GitHub Issues

---

## Quick Reference

```python
# All repos should import from:
from agennext_enterprise import Entity

# Entity extends Schema.org SoftwareApplication
entity = Entity()  # → @type: SoftwareApplication
```

*Last Updated: 2024-05-12*