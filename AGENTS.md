# OpenHands Agent Memory - AGenNext Registry

## Project Context

**Repository:** https://github.com/AGenNext/AGenNext-Enterprise
**Status:** ALPHA (0.1.0)

---

## What Was Built

### Done (M1-M2)
- AgentRegistry core class
- Provider clients: OpenAI, Google, Microsoft, Anthropic, Azure, Custom
- Authentication system: api_key, oauth, gcp_service_account, managed_identity, azure_ad, iam
- Model selection
- UI builders: OpenAI, Google, Microsoft, LangChain, Gradio, Streamlit
- Runnable examples
- Platform UI specification (4 screens)

### In Progress (M3 - 30%)
- Platform UI: Agent List, Add/Edit, Clone, Version History

### Planned (M4-M5)
- Agent Teams
- Docker/Kubernetes deployment

---

## Key Files

| Path | Purpose |
|------|---------|
| `agents/base_agent.py` | Core agent class |
| `agents/roles.py` | Agent roles and config |
| `agents/providers.py` | Provider clients |
| `ui/` | UI builders for every SDK |
| `platform-ui/SPEC.md` | UI spec (4 screens) |
| `PROJECTS.md` | Roadmap with milestones |

---

## Current Focus

Build Platform UI (M3) - 4 screens:
1. Agent List (/agents)
2. Add/Edit Agent (/agents/new, /agents/edit/{id})
3. Clone Agent (/agents/clone/{id})
4. Version History (/agents/{id}/history)

---

## Commands

```bash
# Run UI
python ui/examples.py chat

# Streamlit
streamlit run ui/streamlit_examples.py
```

---

## User Preferences

- No files created without approval
- Show plan BEFORE execution
- Use planning mode before building
- Mark all tasks with status (DONE/TODO/IN PROGRESS)

## Mandatory Runtime Preread

Before starting work on this repository, any agent working on the runtime,
database, schema, identity, governance, or protocol layers must first load the
following guidance into memory and follow it during the session:

- `surreal/README.md`
- `surreal/AGENT.md`

This preread is mandatory before making changes related to:

- SurrealDB runtime structure
- schema design
- functions and events
- Entra Agent Identity and Lifecycle Management
- Governance Tool Kit
- A2A and protocol-layer behavior

## Builder Constraint

Build the world the agent itself must live in.

The agent implementing this runtime is not exempt from the security,
governance, identity, protocol, or database constraints of the runtime it is
helping create. Any agent working in this repository must follow the same
rules, assumptions, and enforcement model that the platform is intended to
apply to other agents and users.

## World Model

Humans are not outside the system.

Humans and agents are first-class participants in the same runtime world, with
identity, state, governance, and interaction modeled inside the system rather
than around it.

Time and location are primitives.

They must be treated as native parts of the runtime model, not as optional
metadata added after the fact. By default, time and location should be modeled
on every object unless there is a concrete reason not to do so.

Time moves forward only.

The runtime should model time the way real-world events progress. Temporal
reversal or world-order overrides are not allowed unless explicitly authorized
by the user.

The world does not stop because one node has gone down.

The system must assume partial failure and continuity. Data continuity relies
on the database and distributed layer, and service recovery relies on
Kubernetes self-healing rather than global pause semantics. Kubernetes
self-healing is mandatory for the production world model. Production failure is
not an acceptable stopping condition; the world must keep moving.

If changes are reverted, they are reverted at a later time.

Reversion does not erase time. Any rollback, compensation, or corrective action
must be modeled as a new event in forward time, not as deletion of what
happened before.

Immutable audit logs are mandatory.

Audit history must be append-only and generated at input, processing, and
output levels at every stage, including LLM streaming. Material events are not
silently rewritten or erased. Corrections, reversions, compensations, and
policy actions must appear as new audit events in forward time. This audit
layer exists not only for governance and security, but also to debug and
improve LLM behavior over time.

---

## Documentation URLs (VERIFIED)

| Framework | URL |
|-----------|-----|
| LangGraph | https://python.langchain.com/docs/langgraph/ |
| LangChain | https://python.langchain.com/docs/concepts/ |
| AutoGen | https://microsoft.github.io/autogen/0.2/ |
| CrewAI | https://docs.crewai.com/ |
| OpenAI | https://platform.openai.com/docs/agents/ |
| Anthropic | https://docs.anthropic.com/en/docs/ |

---

## Feature Schema (15 Features)

| Feature | Description |
|---------|-------------|
| checkpoints | Save and resume state |
| short_term_memory | In-process memory |
| long_term_memory | Persistent storage (SurrealDB, Redis) |
| semantic_memory | Embedding-based memory |
| human_interrupt | Pause agent execution |
| human_feedback | Request human input |
| approval_gates | Require approval to proceed |
| multi_agent | Multiple agent orchestration |
| function_calling | Tool/function calling |
| code_interpreter | Execute code |
| web_search | Search the web |
| streaming | Token-by-token streaming |
| computer_use | Control computer directly |
| mcp | Model Context Protocol |
| guardrails | Input/output validation |

---

## LangGraph SDK API Structure

**Core Classes:**
- `StateGraph` - Create state-based graphs
- `node` - Node in graph (function)
- `START` / `END` - Graph entry/exit points
- `add_node()` - Add node to graph
- `add_edge()` - Connect nodes
- `compile()` - Compile graph

**Key Concepts:**
- `state` - Agent state schema
- `messages` - Chat message history
- `checkpoint` - Save/resume state

---

*Last updated: 2026-05-09*
---

## Rules

- DO NOT add fake contact info (emails, URLs)
- Always use real/existing links only
- Ask user approval before adding external resources
- Verify all links before committing

---

## Known Issues

- Fake email in README (REMOVED)
- localhost in healthcheck (OK - this is standard for Docker)

---

## Audit Done

- Full repo audit completed
- Removed fake emails from: SECURITY.md, PROJECTS.md, DOCKER_README.md, orchestrator
- Replaced placeholder URLs with real ones
- Added rule: no fake contact/placeholders
