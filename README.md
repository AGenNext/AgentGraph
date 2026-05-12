# Schema.org Implementation Platform

> Comprehensive Schema.org V30.0 implementation with databases, graphs, AI agents, and visualization.

[![Schema.org](https://img.shields.io/badge/Schema.org-V30.0-blue)](https://schema.org/docs/full.html)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow)](https://python.org)

## Overview

This is a comprehensive implementation of Schema.org types, mapped to domain databases, with AI agent capabilities, graph visualization, and CRUD operations.

## Features

- ✅ **11 Core Schema.org Types** - Complete implementation
- ✅ **100+ Sub-types** - Full type hierarchy
- ✅ **22 Domain Databases** - Mapped to Schema.org
- ✅ **Graph Visualization** - React xyflow + SurrealDB
- ✅ **Time Search** - Date-based filtering
- ✅ **AI Agents** - LangGraph integration
- ✅ **Vibe Coding** - Bolt.new prompt ready
- ✅ **Docker Support** - Containerized deployment

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the platform
python schema_org.py
```

## Documentation

### Core Schema.org Types

| Type | Description | Databases |
|------|-------------|-----------|
| Thing | Root type | All |
| Person | People | 6 (person_organization, skills, etc.) |
| Organization | Companies | 5 (banking, healthcare, etc.) |
| Place | Locations | 4 (realestate, travel, etc.) |
| Product | Products | 3 (retail, automotive, etc.) |
| Event | Events | 2 (events_database, sports) |
| CreativeWork | Content | 5 (book, music, movie, etc.) |
| Action | Actions | action_mapper, skill_action_tool |
| Intangible | Services | job_postings, offers |
| MedicalEntity | Medical | healthcare_database |
| StructuredValue | Values | kernel_primitives |

### Key Files

```
schema_org.py              # Core Schema.org implementation
schema_org_orm.py         # ORM layer
schema_org_graph.py        # Graph relationships
surrealdb_schema.py       # SurrealDB schema
time_search.py           # Time-based search
schema_org_utils.py      # Utilities
action_mapper.py         # Action mappings
skill_action_tool_map.py # Skill → Action → Tool mapping
```

### Database Mappings

```python
# Example: Person → Domain databases
Person:
  - skills_database.py
  - employment_graph.py
  - person_organization.py
  - social_graph.py
  - healthcare_database.py
  - education_database.py

# Example: Product → Domain databases
Product:
  - retail_database.py
  - automotive_database.py
  - realestate_database.py
```

## Frontend

### React xyflow Visualization

```bash
# Install
npm install @xyflow/react

# Use component
import SchemaOrgHierarchy from './SchemaOrgHierarchy'
<SchemaOrgHierarchy />
```

Reference: `SchemaOrgHierarchy.tsx`

### Bolt.new Vibe Coding

1. Go to https://stackblitz.com/bolt.new
2. Paste prompt from `BOLT_NEW_PROMPT.md`
3. Get your Schema.org UI!

## API Endpoints

```python
# SurrealDB schema - 10 tables
- things, persons, organizations
- places, products, events
- creative_works, actions
- intangibles, medical_entities

# Graph relationships
- type_hierarchy (extends)
- property_edges (properties)

# Time search
- Query by: startDate, endDate, dateCreated
- Operators: =, !=, <, >, <=, >=
```

## Transformed Frameworks

All frameworks mapped to Schema.org primitives:

| Framework | Schema.org Type |
|-----------|----------------|
| GDPR | Legislation |
| HIPAA | MedicalGuideline |
| SOC2 | Credential |
| ISO27001 | Credential |
| OAuth2 | Action |
| SAML | Action |
| AWS | WebAPI |
| Azure | WebAPI |
| Node.js | RuntimePlatform |
| SurrealDB | Database |

## Graph

```
Thing (root)
├── Action ────→ 16 sub-types
├── CreativeWork ────→ Book, Movie, Software, WebPage
├── Event ────→ 8 sub-types
├── Intangible ────→ Service, Ticket, Offer
├── MedicalEntity ────→ Anatomy, MedTech
├── Organization ────→ Corp, Business, Government
├── Person ────→ Patient, Athlete, Author
├── Place ────→ Civic, Residence, Landform
├── Product ────→ IndividualProduct
└── StructuredValue ────→ Geo, ContactPoint
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file

## References

- [Schema.org](https://schema.org/docs/full.html) - Official documentation
- [SurrealDB](https://surrealdb.com) - In-memory graph database
- [React Flow](https://reactflow.dev) - Graph visualization
- [LangGraph](https://github.com/langchain-ai/langgraph) - AI agent framework

---

**Version**: 30.0  
**Last Updated**: 2026-05-11  
**Branch**: schema-org-implementation