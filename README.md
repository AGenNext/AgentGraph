# Content Writing Multi-Agent Team 🤖

A collaborative AI agent team powered by multiple SDKs with LangChain Deep Agent orchestration and A2A protocol support.

## Features

- **15+ SDK Agents** - OpenAI, Salesforce, Microsoft, Google, Docker, GitHub, OpenHands, LlamaIndex, LangChain, Snowflake, Azure AI Foundry, AutoGen, CrewAI, and more
- **LangChain Deep Agent Orchestration** - Graph-based workflow for multi-agent collaboration
- **A2A Protocol** - Agent-to-Agent communication for task delegation
- **Flexible LLM** - Works with OpenAI-compatible APIs (Ollama, LM Studio, custom endpoints)
- **Content Types** - Code, configs, documentation, blog posts, SQL, and more

## Quick Start

```bash
pip install -r requirements.txt
python main.py --mode cards        # View all agents
python main.py --mode demo        # Single agent demo
python main.py --mode team        # Multi-agent demo
python main.py --mode a2a         # A2A protocol demo
```

## Supported LLM Providers

| Provider | Model | Tools | Skills |
|---------|-------|------|-------|
| OpenAI | gpt-4o | code_interpreter, file_search | reasoning, coding |
| Anthropic | Claude | computer_use | reasoning, analysis |
| Google | Gemini | code_execution | research, multimodal |
| AWS Bedrock | Claude | bedrock_knowledge_base | enterprise |
| Ollama | llama3 | (local) | local |
| LM Studio | local | (local) | local |

## Agents

| # | Agent | SDK | Capabilities |
|---|-------|-----|------------|
| 1 | OpenAI Agent | OpenAI SDK | creative, blog |
| 2 | Salesforce Agent | Salesforce | sales, CRM |
| 3 | Microsoft Agent | Azure AI | enterprise |
| 4 | Google Agent | Google ADK | research, SEO |
| 5 | Docker Agent | Docker | k8s, deployment |
| 6 | GitHub Agent | GitHub SDK | PRs, actions |
| 7 | OpenHands Agent | OpenHands SDK | agent code |
| 8 | LlamaIndex Agent | LlamaIndex | RAG, query |
| 9 | LangChain Agent | LangChain | chains, tools |
| 10 | Snowflake Agent | Snowflake | SQL, ML |
| 11 | Azure Foundry | Azure AI | deployments |
| 12 | AutoGen | Microsoft | multi-agent |
| 13 | CrewAI | CrewAI | crew orchestration |
| 14 | Team Coordinator | LangChain Deep Agent | orchestration |

## Environment Variables

```bash
# LLM Providers (auto-detected)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
MISTRAL_API_KEY=...
COHERE_API_KEY=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...

# Custom endpoint
LLM_BASE_URL=http://localhost:1141/v1
LLM_MODEL=llama3

# Local models
OLLAMA_HOST=http://localhost:1141
LMSTUDIO_HOST=http://localhost:1234
```

## Usage

### Single Agent
```python
from agents import OpenAIAgent

agent = OpenAIAgent()
result = agent._generate_content(ContentRequest(
    topic="AI",
    content_type="blog"
))
print(result.content)
```

### Multi-Agent Team
```python
from orchestrator.langgraph_workflow import run_team_workflow

result = run_team_workflow(
    topic="Cloud Computing",
    content_type="comprehensive"
)
print(result["content"])
```

### With Custom LLM
```python
from core.llm_client import create_llm_client

llm = create_llm_client("ollama", model="llama3")
result = llm.generate("Write about AI")
```

## Documentation

- [Contributing Guide](CONTRIBUTING.md) - Add new SDK agents
- [SPEC.md](SPEC.md) - Technical specification
- [A2A Protocol](a2a/) - Agent communication

## License

MIT