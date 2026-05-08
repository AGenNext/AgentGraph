# Agent Registry - Project Plan

![Alpha](https://img.shields.io/badge/Status-Alpha-red?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-0.1.0-blue?style=for-the-badge)

## ALPHA RELEASE NOTICE

```
+---------------------------------------------------------------+
|                     ALPHA RELEASE                             |
+---------------------------------------------------------------+
|  This project is in active development.                        |
|                                                               |
|  WARNING: API may change without notice                       |
|  WARNING: Not recommended for production use                  |
|  FEEDBACK: issues@agennext.io                                |
+---------------------------------------------------------------+
```

---

## Overview
Enterprise Multi-Agent Team Platform with support for:

- OpenAI SDK
- Microsoft Agent Framework
- Google ADK
- Salesforce Agent SDK
- LangGraph Orchestration
- A2A Protocol

---

## MILESTONES

### M1: Core Framework (DONE)

| Task | Status |
|------|--------|
| AgentRegistry class | DONE |
| AgentConfig with roles | DONE |
| Provider clients (5 providers) | DONE |
| Authentication system | DONE |
| Model selection | DONE |

---

### M2: UI Toolkits (DONE)

| Task | Status |
|------|--------|
| UI builders for all SDKs | DONE |
| Gradio components | DONE |
| Streamlit components | DONE |
| Runnable examples | DONE |
| Platform UI spec | DONE |

---

### M3: Platform UI (IN PROGRESS)

| Task | Status |
|------|--------|
| Agent List screen | IN PROGRESS |
| Add/Edit Agent form | TODO |
| Clone Agent modal | TODO |
| Version History | TODO |
| Dark mode | TODO |
| Mobile responsive | TODO |
| A11y accessibility | TODO |

---

### M4: Agent Team Management (PLANNED)

| Task | Status |
|------|--------|
| Create Team API | TODO |
| Add agents to team | TODO |
| Role definitions | TODO |
| Workflow orchestration | TODO |
| Handoff rules | TODO |
| Team chat UI | TODO |

---

### M5: Deployment (PLANNED)

| Task | Status |
|------|--------|
| Docker image | TODO |
| Docker Compose | TODO |
| K8s Helm chart | TODO |
| GitHub Actions | TODO |
| Release v2.0 | TODO |

---

## TASK BOARD

### Done

| ID | Task |
|----|------|
| D-001 | AgentRegistry class |
| D-002 | Provider clients |
| D-003 | UI builders |
| D-004 | Examples |
| D-005 | Platform UI spec |

### In Progress

| ID | Task |
|----|------|
| T-001 | Agent List screen |

### Backlog

| ID | Task | Priority |
|----|------|----------|
| T-002 | Add/Edit form | High |
| T-003 | Clone modal | Medium |
| T-004 | Version history | Medium |
| T-005 | Dark mode | Medium |
| T-006 | Mobile responsive | Medium |
| T-007 | A11y compliance | Low |

---

## Progress

```
M1: 100%
M2: 100%
M3: 30%
M4: 0%
M5: 0%

Overall: 42%
```

---

## ROADMAP

```
2026
==============================================================

Q1 -----------------------------------------------
  DONE: AgentRegistry Core
  DONE: Provider Clients
  DONE: Authentication

Q2 ----------------------------------------------  WE ARE HERE
  IN PROGRESS: Platform UI

Q3 -----------------------------------------------
  PLANNED: Agent Teams
  PLANNED: Multi-Agent Collaboration
  PLANNED: A2A Protocol

Q4 -----------------------------------------------
  PLANNED: Docker & Kubernetes
  PLANNED: Production Release v2.0
```

---

## QUICK START

```bash
# 1. Clone
git clone https://github.com/AGenNext/AGenNext-Registry.git

# 2. Install
pip install -r requirements.txt

# 3. Run UI
python ui/examples.py chat
```

---

## RESOURCES

| Resource | Link |
|----------|------|
| Documentation | README.md |
| UI Spec | platform-ui/SPEC.md |
| Issues | github.com/AGenNext/AGenNext-Registry/issues |

---

Last updated: 2026-05-08
Status: ALPHA
