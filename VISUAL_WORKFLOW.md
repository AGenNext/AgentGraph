# Visual Workflow - Build OpenAI Agent

```ascii
                    ╔═══════════════════════════════════════╗
                    ║   Build OpenAI Agent Flow     ║
                    ╚═══════════════════════════════════════╝

  STEP 1              STEP 2              STEP 3             STEP 4
┌────────┐       ┌────────┐       ┌────────┐       ┌────────┐
│ SELECT │──────▶│  GET   │──────▶│ CREATE│──────▶│ CHAT   │
│FRAMEWRK│       │ UI CMPNT│       │ AGENT │       │        │
└────────┘       └────────┘       └────────┘       └────────┘
     │                │                │                │
     ▼                ▼                ▼                ▼
FrameworkSelector  OpenAIUI       OpenAIAgent      agent.chat()
.get_framework()  .chat_component()  .chat(message)
     │
     ▼
┌────────────────────────────────┐
│ {                              │
│  name: "OpenAI",               │
│  color: "#10A37F",           │
│  models: ["gpt-4o",          │
│          "gpt-4o-mini",      │
│          "o1", "o3-mini"]    │
│ }                              │
└────────────────────────────────┘
```

```python
# Full Code Flow
from agentnext import *

# 1️⃣ Select framework
fw = FrameworkSelector.get_framework('openai')

# 2️⃣ Get UI component  
ui = OpenAIUI.chat_component(model='gpt-4o')

# 3️⃣ Create agent
agent = OpenAIAgent(model='gpt-4o', api_key='sk-...')

# 4️⃣ Chat
response = agent.chat("Hello!")
```

---

### UI Components by Framework

| Framework  | Chat | Assistant | Workflow | Tools | Memory | Embeddings |
|-----------|------|----------|---------|-------|--------|----------|
| OpenAIUI  | ✅  | ✅      | -      | -      | -        | ✅ |
| AnthropicUI| ✅  | -        | -      | -      | -        | - |
| LangGraphUI| -   | -        | ✅     | -      | ✅       | - |
| LangChainUI| -   | -        | ✅     | ✅     | ✅       | - |
| GoogleUI  | ✅  | -        | -      | -      | ✅       | - |
| MicrosoftUI| -   | -        | -      | ✅     | -        | - |
| CrewAIUI  | -   | -        | ✅     | -      | -        | - |
| LlamaIndexUI| -  | -        | -      | -      | ✅       | - |
| SalesforceUI| -  | -        | -      | -      | -        | - |

---

### Full Stack Architecture

```
┌──────────────────────────────────────────────────────────┐
│  FRONTEND (UI)                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │Framework  │  │ OpenAIUI  │  │ Gradio/   │   │
│  │Selector  │  │Builder   │  │Streamlit  │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
├──────────────────────────────────────────────────────────┤
│  BACKEND (API)                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ OpenAI    │  │LangGraph  │  │ LangChain │   │
│  │ Agent    │  │ Client   │  │ Agent    │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
├──────────────────────────────────────────────────────────┤
│  DATA (SurrealDB)                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ Assistant │  │  Thread   │  │   Run    │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
└──────────────────────────────────────────────────────────┘
```
