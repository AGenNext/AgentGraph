# Schema.org Platform Alignment

> How all AGenNext repos should follow Schema.org for interoperability

## ⚠️ COMMON BRANCH: `schema-org-implementation`

**ONE DB + ONE SCHEMA** for all 88 AGenNext repos:

| Source | URL |
|--------|-----|
| **Branch** | `schema-org-implementation` |
| **Schema** | https://github.com/AGenNext/AGenNext-Enterprise/tree/schema-org-implementation |
| **Entity** | base_entity.py (SoftwareApplication) |
| **Database** | 22 × *_database.py |

### Usage

```python
# All repos import from common:
from agennext_enterprise import Entity

# Entity → @type: SoftwareApplication
```

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