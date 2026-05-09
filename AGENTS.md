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

*Last updated: 2026-05-08*
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
