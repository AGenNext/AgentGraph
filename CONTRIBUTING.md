# Contributing a New SDK Agent

Thank you for contributing! This guide walks you through adding a new SDK agent to the Content Writing Team.

## Quick Start

1. Create your agent file: `agents/<sdk_name>_agent.py`
2. Add to registry: `agents/__init__.py`
3. Add agent card: `a2a/card.py`

---

## Step 1: Create Your Agent

Copy this template:

```python
"""<SDK Name> Agent SDK - Brief description."""

from typing import Optional
import os

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig


class MySDKAgent(BaseAgent):
    """Your SDK agent description.
    
    Capabilities:
    - Capability one
    - Capability two
    
    Tools: tool_one, tool_two
    Skills: skill_one, skill_two
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            agent_id="mysdk-writer",
            name="MySDK Writer",
            description="Your SDK description",
            capabilities=[
                "capability_one",
                "capability_two",
            ],
            skills=["skill_one", "skill_two"],
            api_key=api_key or os.getenv("MY_API_KEY"),
        )
        
        self.llm_config = LLMConfig.from_env()
        self._llm = None
    
    def _get_port(self) -> int:
        return 801X  # Unique port (see below)
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        # Route by content type
        if "some" in ct:
            return self._some_content(request)
        else:
            return self._default(request)
    
    def _some_content(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content="Your generated content here",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "something", "skill": "skill_name"},
        )
    
    def _default(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f"# {request.topic}\n\nDefault content...",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "default"},
        )
```

---

## Step 2: Required Attributes

| Attribute | Description | Example |
|----------|------------|--------|
| `agent_id` | Unique ID | `"openai-writer"` |
| `name` | Display name | `"OpenAI Writer"` |
| `description` | What it does | `"Creative content..."` |
| `capabilities` | List of capabilities | `["generate_creative", "write_blog"]` |
| `skills` | List of skills | `["creative-writing"]` |
| `_get_port()` | Return unique port | `8001` |

### Port Assignment

```
8001 - OpenAI          8010 - Anthropic
8002 - Salesforce      8011 - AWS Bedrock
8003 - Microsoft       8012 - Snowflake
8004 - Google          8013 - Azure AI Foundry
8005 - Docker         8014 - AutoGen
8006 - GitHub         8015 - CrewAI
8007 - OpenHands      8016 - (your agent)
8008 - LlamaIndex     8017 - (your agent)
8009 - LangChain     8018+ - (your agent)
```

---

## Step 3: Register Your Agent

In `agents/__init__.py`:

```python
from .my_sdk_agent import MySDKAgent

__all__ = [
    # ... existing agents ...
    "MySDKAgent",
]
```

---

## Step 4: Add Agent Card

In `a2a/card.py`:

```python
MYSDK_AGENT_CARD = AgentCard(
    agentId="mysdk-writer",
    name="MySDK Writer",
    description="Your SDK description",
    url="http://localhost:801X",  # Your port
    version="1.0.0",
    capabilities=[
        AgentCapability(name="capability_one", description="Does one"),
        AgentCapability(name="capability_two", description="Does two"),
    ],
    skills=[
        AgentSkill(
            id="my-sdk-writing",
            name="MySDK Writing", 
            description="Generate my-sdk content",
            tags=["sdk", "specialty"],
        ),
    ]
)
```

Then add to `AGENT_CARDS` dict:
```python
AGENT_CARDS = {
    # ... existing ...
    "mysdk-writer": MYSDK_AGENT_CARD,
}
```

---

## Content Types

Support these content types based on your SDK:

| Content Type | Use Case |
|--------------|----------|
| `blog` | Blog posts |
| `agent` | Agent code |
| `tool` | Tool definitions |
| `sql` | SQL queries |
| `deployment` | Config files |
| `workflow` | CI/CD pipelines |
| `documentation` | Docs/READMEs |
| `api` | API code |

---

## Testing Your Agent

```bash
# Test card display
python main.py --mode cards

# Test single agent
python main.py --mode demo --agent mysdk --topic "Hello" --content-type blog

# Test team
python main.py --mode team --topic "Your Topic" --content-type blog
```

---

## Environment Variables

Recommend these env vars in your agent:

| Variable | Description |
|----------|------------|
| `MY_API_KEY` | API key for your SDK |
| `LLM_API_KEY` | Fallback LLM key |
| `MY_BASE_URL` | Custom endpoint |

---

## Questions?

- Open an issue: [Link to issues]
- Join our Discord: [Link]

---

## License

By contributing, you agree to license under MIT.