# AI Agent Runtime Repositories

## Top Agent Frameworks (GitHub)

Reference: https://github.com/topics/ai-agents

| # | Repository | Stars | Language | Schema.org |
|---|------------|-------|----------|------------|
| 1 | VoltAgent | 8.7k | TypeScript | SoftwareApplication |
| 2 | AgentScope | N/A | Python | SoftwareApplication |
| 3 | AgentScope Runtime | N/A | Python | SoftwareApplication |
| 4 | deepset/haystack | 23.7k | Python | SoftwareApplication |
| 5 | Microsoft Agent Framework | N/A | C#/Python | SoftwareApplication |
| 6 | GitHub Copilot SDK | N/A | TypeScript | SoftwareApplication |

## Agent Platform Architecture

```
┌──────────────────────────────────┐
│     Agent Runtime Platform        │
├──────────────────────────────────┤
│  ┌────────────┐   ┌───────────┐ │
│  │  Memory   │   │  Skills   │ │
│  │  (RAG)   │   │  (MCP)   │ │
│  └─────┬────┘   └─────┬─────┘ │
│        │              │        │
│  ┌─────┴─────────────┴─────┐ │
│  │    Agent Engine         │ │
│  │  (LLM, Tools, Guard) │ │
│  └──────────┬──────────┘ │
│             │             │
│  ┌──────────┴──────────┐ │
│  │   Execution Layer    │ │
│  │  (Runtime Platform) │ │
│  └───────────────────┘ │
└──────────────────────────────────┘
```

## Agent Runtime Features

| Feature | Description | Schema.org Type |
|---------|-------------|----------------|
| Memory | Long/short term | KnowledgeGraph |
| Skills | Tool capabilities | Service |
| RAG | Knowledge retrieval | Dataset |
| Guardrails | Safety checks | Legislation |
| Voice | Audio I/O | AudioObject |
| MCP | Model Context Protocol | Action |
| Workflow | Multi-step | PlanAction |

## Schema.org Mapping

```python
@dataclass
class AgentRuntime:
    name: str = ""           # SoftwareApplication.name
    version: str = ""
    
    # Capabilities
    memory: bool = False    # KnowledgeGraph
    rag: bool = False       # Dataset
    voice: bool = False    # Audio
    multi_agent: bool = False
    
    # Runtime
    runtime_type: str = ""  # RuntimePlatform
    sandbox: str = ""       # VirtualLocation
    
    # Schema.org
    additional_type: str = "SoftwareApplication"
    supports_smart_integration: bool = False
    application_category: str = "DeveloperApplication"
```

## Implementation

```python
agent_platforms = {
    "VoltAgent": {
        "stars": 8700,
        "language": "TypeScript",
        "features": ["Memory", "RAG", "MCP", "Voice", "Workflow"],
    },
    "AgentScope": {
        "language": "Python",
        "features": ["Multi-Agent", "RAG", "Voice", "Deployment"],
    },
    "Haystack": {
        "stars": 23741,
        "language": "Python",
        "features": ["RAG", "Pipeline", "Evaluation"],
    },
    "GitHub Copilot": {
        "language": "TypeScript",
        "features": ["Guardrails", "MCP", "Tools"],
    },
}
```

## Agent Components

| Component | Schema.org | Implementation |
|-----------|-----------|----------------|
| Agent | SoftwareApplication | Agent engine |
| Memory | KnowledgeGraph | Vector DB |
| Skills | Service | Tool functions |
| Guardrails | Legislation | Policy enforcement |
| Tools | Action | API calls |
| Context | DataFeed | Prompt context |

Reference: https://github.com/topics/agent-runtime | https://schema.org/SoftwareApplication