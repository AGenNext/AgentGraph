# Agent Registry - Project Plan

## Overview
Enterprise Multi-Agent Team Platform with support for:

- OpenAI SDK
- Microsoft Agent Framework  
- Google ADK
- Salesforce Agent SDK
- LangGraph Orchestration
- A2A Protocol

---

## 📋 Project Phases

### Phase 1: Core Framework ✅ DONE
- [x] Agent roles and governance
- [x] Provider integration
- [x] Authentication (multiple methods)
- [x] Model selection

### Phase 2: Providers & APIs ✅ DONE
- [x] OpenAI client
- [x] Anthropic client
- [x] Google Gemini client
- [x] Azure OpenAI client
- [x] AWS Bedrock client
- [x] Custom/OpenAI-compatible provider

### Phase 3: UI Toolkits ✅ DONE
- [x] OpenAI UI Builder
- [x] Microsoft UI Builder
- [x] Google UI Builder
- [x] LangChain UI Builder
- [x] Gradio builders
- [x] Streamlit builders
- [x] Runnable examples

### Phase 4: Platform UI 📋 IN PROGRESS
- [ ] Agent List screen
- [ ] Add/Edit Agent screen
- [ ] Clone Agent screen
- [ ] Version History screen
- [ ] Dark mode support
- [ ] Mobile responsive
- [ ] Accessibility (A11y)

### Phase 5: Agent Team Management
- [ ] Create team
- [ ] Add multiple agents to team
- [ ] Define roles (Supervisor/Worker/Router)
- [ ] Configure collaboration (sequential/parallel)
- [ ] Handoff rules

### Phase 6: Deployment
- [ ] Docker image
- [ ] Docker Compose
- [ ] Kubernetes helm chart
- [ ] GitHub Actions CI/CD

---

## 📦 Components

### Agents Module (`/agents`)
| Component | Status |
|-----------|--------|
| base_agent.py | ✅ |
| roles.py | ✅ |
| providers.py | ✅ |
| coordinator.py | ✅ |
| openai_agent.py | ✅ |
| microsoft_agent.py | ✅ |
| google_agent.py | ✅ |
| langchain_agent.py | ✅ |

### UI Module (`/ui`)
| Component | Status |
|-----------|--------|
| __init__.py | ✅ |
| openai_builder.py | ✅ |
| microsoft_builder.py | ✅ |
| google_builder.py | ✅ |
| langchain_builder.py | ✅ |
| gradio_builder.py | ✅ |
| streamlit_builder.py | ✅ |
| examples.py | ✅ |

### Platform UI (`/platform-ui`)
| Component | Status |
|-----------|--------|
| SPEC.md | ✅ |
| Agent List | 📋 |
| Add/Edit | 📋 |
| Clone | 📋 |
| History | 📋 |

---

## 🎯 Milestones

| Milestone | Target | Status |
|----------|--------|--------|
| v1.0 Core | Q1 2026 | ✅ |
| v1.5 UI | Q2 2026 | 📋 |
| v2.0 Teams | Q3 2026 | ⏳ |
| v2.5 Deploy | Q4 2026 | ⏳ |

---

## 👥 Contributors
Placeholder for contributor data.

---

## 📞 Support
- Issues: Open GitHub issue
- Discussions: Use GitHub Discussions

---

## 🎯 MILESTONES

### M1: Core Framework (COMPLETED)
**Target:** Q1 2026  
**Status:** ✅ Complete

**Deliverables:**
- AgentRegistry class
- AgentConfig with roles
- Provider clients (5 providers)
- Authentication system
- Model selection

---

### M2: UI Toolkits (COMPLETED)
**Target:** Q2 2026  
**Status:** ✅ Complete

**Deliverables:**
- UI builders for all SDKs
- Gradio components
- Streamlit components
- Runnable examples

---

### M3: Platform UI (CURRENT)
**Target:** Q2 2026  
**Status:** 🔄 In Progress

**Tasks:**
- [ ] Agent List screen (screens/agents/) - @todo
- [ ] Add/Edit Agent form (@todo)
- [ ] Clone Agent modal (@todo)
- [ ] Version History (@todo)
- [ ] Dark mode (@todo)
- [ ] Mobile responsive (@todo)
- [ ] A11y accessibility (@todo)

**Owner:** @platform-team  
**ETA:** 4 weeks

---

### M4: Agent Team Management
**Target:** Q3 2026  
**Status:** ⏳ Planned

**Tasks:**
- [ ] Create Team API (@todo)
- [ ] Add agents to team (@todo)
- [ ] Role definitions (@todo)
- [ ] Workflow orchestration (@todo)
- [ ] Handoff rules (@todo)
- [ ] Team chat UI (@todo)

---

### M5: Deployment
**Target:** Q4 2026  
**Status:** ⏳ Planned

**Tasks:**
- [ ] Docker image (@todo)
- [ ] Docker Compose (@todo)
- [ ] K8s Helm chart (@todo)
- [ ] GitHub Actions (@todo)
- [ ] Release v2.0 (@todo)

---

## 📝 TASK BOARD

### Backlog
| ID | Task | Priority | Assignee |
|----|------|----------|----------|
| T-001 | Implement Agent List | High | @todo |
| T-002 | Add/Edit form | High | @todo |
| T-003 | Clone modal | Medium | @todo |
| T-004 | Version history | Medium | @todo |
| T-005 | Dark mode | Medium | @todo |
| T-006 | Mobile responsive | Medium | @todo |
| T-007 | A11y compliance | Low | @todo |

### In Progress
| ID | Task | Assignee |
|----|------|----------|
| T-001 | Agent List | @in-progress |

### Done
| ID | Task |
|----|------|
| D-001 | AgentRegistry class |
| D-002 | Provider clients |
| D-003 | UI builders |
| D-004 | Examples |

---

## 🔗 Dependencies

```
M1 (Core) ─────┐
               ├─► M3 (UI) ──► M4 (Teams) ──► M5 (Deploy)
M2 (Toolkits) ─┘
```

---

## 📊 Progress

```
M1: ████████████████████ 100%
M2: ████████████████████ 100%
M3: ████████░░░░░░░░░░░ 30%
M4: ░░░░░░░░░░░░░░░░░░ 0%
M5: ░░░░░░░░░░░░░░░░░░ 0%

Overall: ████████░░░░░ 25%
```
