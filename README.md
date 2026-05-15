# AGenNext Enterprise Agent Platform

> Comprehensive enterprise AI agent management with multiple specialized agent types, chat UI, channel integrations, and multimodal support.

[![Platform](https://img.shields.io/badge/AGenNext-1.0.0-blue)](https://github.com/AGenNext/AgentGraph)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org)

## Overview

AGenNext is an enterprise-grade agent management platform featuring:
- Multiple specialized agent types (Sales, DevOps, Research, Code, etc.)
- Chat UI with multimodal support
- Channel integrations (WhatsApp, Slack, Teams)
- Memory bank & decision logging
- Deep research capabilities
- Docker-ready production deployment

## Quick Start

```bash
# Frontend (Next.js)
cd agennext-ui
npm install
npm run dev

# Backend (FastAPI)
pip install fastapi uvicorn surrealdb
python server.py
```

## Platform Services

| Service | Port | Framework |
|---------|------|-----------|
| Frontend | 3000 | Next.js 14 |
| Backend | 8000 | FastAPI |

## Key Features

- **Agent Types**: Sales, DevOps, Research, Code, Security, Multimodal
- **Tools**: Web Search, Image Gen, TTS, STT, Code Executor
- **Memory Bank**: Persistent knowledge with table view
- **Decision Log**: Agent reasoning trail
- **Deep Research**: Multi-stage research
- **Channel Integrations**: WhatsApp, Slack, Teams

## Deployment

```bash
# Docker Compose
docker compose up -d

# Or from GitHub
git clone -b feature/complete-platform https://github.com/AGenNext/AgentGraph.git
cd AgentGraph
docker compose up -d
```

## API Endpoints

- `/frameworks` - Agent frameworks
- `/tools` - Available tools
- `/models` - Model gateway
- `/memory` - Agent memory
- `/channels` - Integrations
- `/research` - Deep research
- `/notebook/cells` - Code notebooks

## Documentation

See [VPS-DEPLOY.md](./VPS-DEPLOY.md) for production deployment to VPS.
 
### SurrealDB Schema

- Canonical schema: [surreal/schema/schema-org-surrealdb.surql](/Users/apple/Agent-Graph/surreal/schema/schema-org-surrealdb.surql:1)
- Schema helper: [schema_org_orm.py](/Users/apple/Agent-Graph/schema_org_orm.py:1)
- Database notes: [docs/database.md](/Users/apple/Agent-Graph/docs/database.md:1)

```bash
# Apply schema changes with SurrealKit
cargo install surrealkit
surrealkit sync
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
schema_org_orm.py         # SurrealDB schema helper
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
- [SurrealDB](https://surrealdb.com) - Multi-model database
- [React Flow](https://reactflow.dev) - Graph visualization
- [LangGraph](https://github.com/langchain-ai/langgraph) - AI agent framework

---

**Version**: 30.0  
**Last Updated**: 2026-05-11  
**Branch**: schema-org-implementation
