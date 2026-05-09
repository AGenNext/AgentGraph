# AGenNext - Multi-Framework Agent Backend

Unified Python package for building AI agents across 11 frameworks with full frontend (UI) and backend integration.

## Features

- **Frontend (UI)**: 60 component method calls across 11 frameworks
- **Backend (Agents)**: 9 agent classes
- **Framework Selector**: Switch between frameworks easily

## Installation

```bash
pip install -e .
```

## Usage

```python
from agentnext import *

# 1. Select Framework
fw = FrameworkSelector.get_framework('langgraph')

# 2. Get UI Component
ui = LangGraphUI.node_palette()

# 3. Create Agent
agent = LangGraphClient()

# 4. Run
response = agent.chat("Hello!")
```

## 11 Supported Frameworks

| Framework | Components | UI Methods |
|-----------|------------|------------|
| langgraph | 15 | workflow_builder, node_palette, human_in_loop, etc. |
| autogen | 9 | studio, group_chat, code_executor, etc. |
| anthropic | 5 | chat_component, artifacts_component, etc. |
| microsoft | 5 | group_chat, studio, etc. |
| salesforce | 5 | einstein_agent, crm_integration, etc. |
| google | 4 | agent_builder, session_manager, etc. |
| crewai | 4 | crew_builder, process_flow, etc. |
| llamaindex | 4 | index_builder, query_engine, etc. |
| langchain | 3 | chain_builder, tool_registry, etc. |
| openai | 3 | chat_component, assistant_component, etc. |
| smolagents | 3 | agent_builder, code_agent, etc. |

**Total: 60 component calls across 11 frameworks**

## Component Summary

| Unique Methods | Shared | Total Calls |
|---------------|--------|------------|
| 41 | 10 | 60 |

- **41 unique methods**: Different functionality per framework
- **10 shared**: Used by 2+ frameworks (node_palette, visual_canvas, etc.)
- **60 calls**: Total invocations across all frameworks

## UI Components (LangGraph Example)

```python
from agentnext import LangGraphUI

# Node Palette (8 node types)
LangGraphUI.node_palette()

# Human in Loop (3 ways)
LangGraphUI.human_in_loop()
LangGraphUI.approval_gate()
LangGraphUI.human_feedback()

# Workflow Editor
LangGraphUI.branch_editor()
LangGraphUI.edge_editor()
LangGraphUI.loop_editor()
LangGraphUI.visual_canvas()
LangGraphUI.yaml_editor()
```

## Architecture

```
┌─────────────────────────────────────────────┐
│           AGenNext Package                  │
├─────────────────────────────────────────────┤
│  FRONTEND (UI)     │   BACKEND (Agents)  │
│  ─────────────     │   ─────────────  │
│  17 UI Classes   │   9 Agents    │
│  60 Components   │   A2A Client  │
│  11 Frameworks   │   Providers    │
└─────────────────────────────────────────────┘
```

## Exports

```python
from agentnext import *

# UI
OpenAIUI, AnthropicUI, LangGraphUI, LangChainUI, GoogleUI, 
MicrosoftUI, CrewAIUI, AutoGenUI, LlamaIndexUI, SalesforceUI,
SmolAgentsUI

# Builders
OpenAIBuilder, LangGraphBuilder, LangChainBuilder, 
MicrosoftBuilder, GoogleBuilder, GradioBuilder

# Agents
OpenAIAgent, LangGraphClient, LangChainAgent, CrewAIAgent,
AutoGenAgent, GoogleAgent, MicrosoftAgent, LlamaIndexAgent

# Protocol
A2AClient, AgentCard, Task, TaskStatus

# Framework Selector
FrameworkSelector
```

## License

MIT
