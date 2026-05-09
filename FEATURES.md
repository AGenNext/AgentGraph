# Agent Framework Feature Matrix
# Grounded in official documentation

## Supported Frameworks

| Feature | LangGraph | LangChain | AutoGen | CrewAI | OpenAI SDK | Anthropic | Custom |
|--------|----------|----------|--------|--------|-----------|----------|--------|
| **Checkpoint/Save State** | ✅ Native | ✅ Native | ⚠️ Manual | ✅ Native | ⚠️ Manual | ⚠️ Manual | 🔧 You implement |
| **Memory/Persistence** | ✅ Native | ✅ Native | ⚠️ Manual | ✅ Native | ⚠️ Manual | ⚠️ Manual | 🔧 You implement |
| **Human-in-Loop** | ✅ Native | ✅ Native | ✅ Native | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | 🔧 You implement |
| **Multi-Agent** | ⚠️ Manual | ⚠️ Manual | ✅ Native | ✅ Native | ⚠️ Manual | ⚠️ Manual | 🔧 You implement |
| **Tool Use** | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ⚠️ Manual | 🔧 You implement |
| **Streaming** | ✅ Native | ✅ Native | ⚠️ Manual | ✅ Native | ✅ Native | ✅ Native | 🔧 You implement |

---

## Framework Feature Details

### LangGraph ⭐ RECOMMENDED
**Official Docs:** https://docs.langgraph.ai/

| Feature | Status | Documentation |
|---------|--------|--------------|
| Checkpoint/Persistence | ✅ Native | [Persistence Guide](https://docs.langchain.com/oss/python/langgraph/persistence) |
| Memory Store | ✅ Native | [Memory Guide](https://docs.langchain.com/oss/python/langgraph/add-memory) |
| Human-in-Loop | ✅ Native | [Concepts: Memory](https://docs.langchain.com/oss/python/concepts/memory) |

**Key Features:**
- `MemorySaver` / `SqliteSaver` for checkpointing
- `InMemoryStore` for persistence
- `interrupt()` for human-in-the-loop
- StateGraph for complex workflows

**Code Example:**
```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}
graph.invoke(input, config)  # State auto-saved
```

---

### LangChain
**Official Docs:** https://python.langchain.com/

| Feature | Status | Documentation |
|---------|--------|--------------|
| Checkpoint/Memory | ✅ Native | Uses LangGraph under the hood |
| Memory Store | ✅ Native | [Memory Overview](https://docs.langchain.com/oss/python/concepts/memory) |
| Human-in-Loop | ✅ Native | Via LangGraph interrupt |

**Key Features:**
- Built on LangGraph
- LangChain memory modules
- LCEL for streaming

---

### AutoGen (Microsoft)
**Official Docs:** https://microsoft.github.io/autogen/

| Feature | Status | Documentation |
|---------|--------|--------------|
| Multi-Agent | ✅ Native | [Multi-Agent](https://microsoft.github.io/autogen/current/) |
| Human-in-Loop | ✅ Native | [Human Feedback](https://microsoft.github.io/autogen/current/) |
| Checkpoint | ⚠️ Manual | Need to implement |

**Key Features:**
- `ConversableAgent` for multi-agent
- `initiate_chat` for human feedback
- Microsoft support

---

### CrewAI ⭐ Good for Multi-Agent
**Official Docs:** https://docs.crewai.com/

| Feature | Status | Documentation |
|---------|--------|--------------|
| Memory | ✅ Native | [Memory Guide](https://docs.crewai.com/en/concepts/memory) |
| Multi-Agent | ✅ Native | [Crews](https://docs.crewai.com/) |
| Checkpoint | ⚠️ Manual | Via memory system |

**Key Features:**
- `Memory` class with semantic recall
- `Crew` for multi-agent orchestration
- Process modes: sequential, hierarchical

---

### OpenAI Agents SDK
**Official Docs:** https://openai.com/index/agents/

| Feature | Status | Documentation |
|---------|--------|--------------|
| Tool Use | ✅ Native | Built-in |
| Streaming | ✅ Native | Built-in |
| Checkpoint | ⚠️ Manual | Need to implement |

---

### Anthropic (Claude)
**Official Docs:** https://docs.anthropic.com/

| Feature | Status | Documentation |
|---------|--------|--------------|
| Tool Use | ⚠️ Manual | Via function calling |
| Computer Use | ✅ Native | [Computer Use](https://docs.anthropic.com/) |
| Checkpoint | ⚠️ Manual | Need to implement |

---

## This Backend API Endpoints

### Core Task Operations
| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/tasks` | POST | Create task |
| `/tasks/{id}` | GET | Get task |
| `/tasks/{id}/context` | POST | Provide context |
| `/tasks/{id}/stop` | POST | External stop |
| `/tasks/{id}/cancel` | POST | Cancel task |
| `/tasks` | GET | List tasks |

### Pre-Flight (Gather context → run to completion)
| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/tasks/preflight` | POST | Submit with pre-flight |

### Checkpoints (Save state at each stop)
| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/tasks/checkpoints` | POST | Submit with checkpoints |
| `/tasks/{id}/checkpoint/state` | GET | Get current checkpoint |
| `/tasks/{id}/checkpoint/history` | GET | Get all checkpoints |
| `/tasks/{id}/checkpoint/{i}/resume` | POST | Resume from checkpoint |
| `/tasks/{id}/learnings` | GET | Get all learnings |

### Framework Support
| Framework | Adapter | Documentation |
|------------|---------|--------------|
| langgraph | `LangGraphAdapter()` | [docs.langgraph.ai](https://docs.langgraph.ai/) |
| langchain | `LangChainAdapter()` | [python.langchain.com](https://python.langchain.com/) |
| autogen | `AutoGenAdapter()` | [microsoft.github.io/autogen](https://microsoft.github.io/autogen/) |
| crewai | `CrewAIAdapter()` | [docs.crewai.com](https://docs.crewai.com/) |
| openai | `OpenAIAdapter()` | [openai.com/agents](https://openai.com/index/agents/) |
| anthropic | `AnthropicAdapter()` | [docs.anthropic.com](https://docs.anthropic.com/) |

---

## Running the Backend

```bash
# Install dependencies
cd agent-backend
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --port 8000

# Test
curl http://localhost:8000/health
```