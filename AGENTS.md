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
| long_term_memory | Persistent storage (PostgreSQL, Redis) |
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
