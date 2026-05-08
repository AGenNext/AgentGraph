"""OpenHands Agent SDK - Generate OpenHands agents and SDK code."""

from typing import Optional, List
import os

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig


class OpenHandsAgent(BaseAgent):
    """OpenHands SDK content specialist.
    
    Capabilities:
    - Agent code generation
    - Tool definitions
    - Skill creation
    - SDK documentation
    - Agent configuration
    
    Tools: browser, terminal, editor, file_operations
    Skills: agent-development, tool-creation, skill-definition
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            agent_id="openhands-sdk-writer",
            name="OpenHands SDK Writer",
            description="OpenHands agent SDK - agents, tools, skills, config",
            capabilities=[
                "agent_code",
                "tool_definition", 
                "skill_creation",
                "sdk_docs",
                "agent_config",
            ],
            skills=["agent-development", "tool-creation", "skill-definition", "python"],
            api_key=api_key or os.getenv("LLM_API_KEY"),
        )
        
        self.llm_config = LLMConfig.from_env()
        self._llm = None
    
    def _get_port(self) -> int:
        return 8007
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        if "agent" in ct:
            return self._agent_code(request)
        elif "tool" in ct:
            return self._tool_def(request)
        elif "skill" in ct:
            return self._skill_create(request)
        elif "config" in ct:
            return self._agent_config(request)
        else:
            return self._sdk_docs(request)
    
    def _agent_code(self, request: ContentRequest) -> ContentResult:
        name = request.topic.replace(" ", "").replace("-", "")
        return ContentResult(
            content=f'''"""OpenHands Agent: {request.topic}"""

from openhands.runtime import Agent

class {name}Agent(Agent):
    """Agent for {request.topic}."""
    
    def __init__(self):
        super().__init__(
            name="{request.topic.lower().replace(' ', '-')}",
            description="{request.topic}",
        )
    
    async def step(self, state):
        """Execute one step."""
        action = state.get("last_action")
        
        if action == "think":
            thought = await self.llm.think(state.get("input", ""))
            state.update(thought=thought)
        
        elif action == "observe":
            obs = await self.tools.call(state.get("tool"), state.get("args", {{}}))
            state.update(observation=obs)
        
        return state


if __name__ == "__main__":
    from openhands.runtime import run_agent
    run_agent({name}Agent())
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "agent-code", "skill": "agent-development"},
        )
    
    def _tool_def(self, request: ContentRequest) -> ContentResult:
        name = request.topic.replace(" ", "_").replace("-", "_")
        return ContentResult(
            content=f'''"""Tool: {request.topic}"""

from openhands.tools import Tool

class {name.title().replace("_", "")}Tool(Tool):
    """Tool for {request.topic}."""
    
    name = "{name}"
    description = "Tool description for {request.topic}"
    
    parameters = {{
        "type": "object",
        "properties": {{
            "input": {{"type": "string", "description": "Input"}}
        }},
        "required": ["input"]
    }}
    
    async def execute(self, params):
        input_text = params.get("input", "")
        result = self._process(input_text)
        return result
    
    def _process(self, input_text: str) -> str:
        return f"Result: {{input_text}}"
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "tool-definition", "skill": "tool-creation"},
        )
    
    def _skill_create(self, request: ContentRequest) -> ContentResult:
        name = request.topic.replace(" ", "-").lower()
        return ContentResult(
            content=f'''# OpenHands Skill: {name}

## Definition
- **Name**: {name}
- **Description**: Skill for {request.topic}
- **Version**: 1.0.0

## Triggers
- `{name}`
- related keywords

## Example Usage

```python
from openhands.skills import invoke_skill
result = await invoke_skill("{name}", input="...")
```

or via natural language:

> "Help me with {request.topic}"
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "skill", "skill": "skill-definition"},
        )
    
    def _agent_config(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''# {request.topic} Agent Config

name: {request.topic.lower().replace(' ', '-')}
version: 1.0.0
description: "{request.topic}"

llm:
  provider: openai
  model: gpt-4o
  temperature: 0.7

tools:
  - browse
  - terminal
  - editor

capabilities:
  - reasoning
  - tool_use

safety:
  max_iterations: 100
  timeout: 300
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "agent-config", "skill": "configuration"},
        )
    
    def _sdk_docs(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''# OpenHands SDK: {request.topic}

## Installation

```bash
pip install openhands-sdk
```

## Quick Start

```python
from openhands import Agent, run_agent

agent = Agent(
    name="{request.topic.lower().replace(' ', '-')}",
    description="{request.topic}",
)

result = await run_agent(agent, input="Task here")
```

## Core Concepts

### Agent
```python
class MyAgent(Agent):
    async def step(self, state):
        return state
```

### Tool
```python
class MyTool(Tool):
    name = "my_tool"
    async def execute(self, params):
        return result
```

### Skill
```python
@skill
async def my_skill(input: str) -> str:
    return result
```
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "sdk-docs", "skill": "documentation"},
        )