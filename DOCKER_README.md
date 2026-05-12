# From Docker to Agent - Full Walkthrough

## 1. Pull/Running the Docker Image

```bash
# Pull the image
docker pull agennext/agent-registry:latest

# Run it
docker run -d -p 8501:8501 -p 7860:7860 agennext/agent-registry:latest

# Check it's running
docker ps
```

## 2. Access the UI

Open in browser:
- **Gradio**: http://localhost:7860
- **Streamlit**: http://localhost:8501

## 3. Choose Your SDK

| SDK | UI | Components |
|-----|-----|-----------|
| OpenAI | Playground | chat, finetune, assistant |
| Google | Vision, Grounded | vision, grounded |
| Microsoft | AI Agent, Copilot | ai_agent, copilot |
| LangChain | RAG, Agent | rag(), agent_builder() |
| LangGraph | Workflow | workflow(), node_editor() |

## 4. Create an Agent

### Option A: Via Gradio UI

```bash
# Run Gradio
docker run -d -p 7860:7860 agennext/agent-registry:latest \
    python ui/examples.py openai
```

Then in the UI:
1. Select your SDK (OpenAI/Google/Microsoft/LangChain)
2. Pick component (chat/playground/RAG)
3. Configure model/parameters
4. Click "Run"

### Option B: Via Python Code

```python
from ui import OpenAIBuilder
from agents.providers import create_client

# 1. Create provider client
client = create_client("openai", {
    "provider_api_key": "sk-...",
})

# 2. Define agent function
def my_agent(msg, model="gpt-4o"):
    return client.chat([{"role": "user", "content": msg}], model=model)

# 3. Build UI
builder = OpenAIBuilder(my_agent)
demo = builder.playground()
demo.launch()
```

### Option C: Via Config File

```yaml
# agents.yaml
agent:
  name: "my-agent"
  provider: "openai"
  model: "gpt-4o"
  ui: "chat"
```

## 5. Configure Identity & Auth

```python
from agents.roles import AgentConfig, AgentRole

config = AgentConfig(
    role=AgentRole.PROJECT_DRIVER,
    identity_id="agent-123",
    identity_provider="entra",
    secret_ref="ai-agent-key",
    owner="",
    sponsor="",
    
    # Provider + Auth
    ai_provider_name="openai",
    auth_method="api_key",
    provider_api_key="sk-...",
    model="gpt-4o",
)
```

## 6. Register Agent

```python
from agents.base_agent import BaseAgent

# Register to registry
agent = BaseAgent(config)
agent.register()

# Verify
agent.list()
```

## 7. Full Example

```python
# main.py
from ui import OpenAIBuilder
from agents.providers import create_client
from agents.roles import AgentConfig, AgentRole

# 1. Configure agent
config = AgentConfig(
    role=AgentRole.PROJECT_DRIVER,
    identity_id="my-agent",
    identity_provider="entra",
    secret_ref="agent-key",
    owner="",
    sponsor="",
    ai_provider_name="openai",
    auth_method="api_key",
    provider_api_key="sk-...",
    model="gpt-4o",
)

# 2. Create provider client
client = create_client("openai", {"provider_api_key": config.provider_api_key})

# 3. Define agent function
def run_agent(msg):
    return client.chat([{"role": "user", "content": msg}], model=config.model)

# 4. Build UI
builder = OpenAIBuilder(run_agent)
demo = builder.playground()

# 5. Run
if __name__ == "__main__":
    demo.launch()
```

## 8. Run in Docker

```bash
# Build
docker build -t my-agent .

# Run
docker run -d -p 7860:7860 \
    -e OPENAI_API_KEY=sk-... \
    my-agent

# Or with docker-compose
docker-compose up -d
```

## Summary Flow

```
Docker Image → Access UI → Select SDK → Build Agent → Configure Auth → Run
     ↓           ↓          ↓         ↓            ↓
DockerHub   Browser    OpenAI    Builder   Identity   Demo
                       Google   LangChain  Provider  Container
                       Microsoft LangGraph
```
