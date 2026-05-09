# Multi-Agent Team Flow - Using OpenAI

## 4-Step Flow Diagram

```
     STEP 1           STEP 2           STEP 3           STEP 4
  +---------+     +---------+     +---------+     +---------+
  | SELECT  | --> |  GET UI  | --> | CREATE  | --> |  RUN    |
  |FRAMEWORK|     |         |     |  TEAM   |     |         |
  +---------+     +---------+     +---------+     +---------+
       |               |               |               |
       v               v               v               v
FrameworkSelector  MicrosoftUI   CrewAIAgent     .run()
 .get_framework()  .group_chat()   .add()      "task"
```

## 3 Framework Options

| Framework | UI Method | OpenAI Models | Use Case |
|-----------|----------|--------------|----------|
| Microsoft | group_chat() | gpt-4o, claude-3 | Group chat |
| CrewAI | crew_builder() | gpt-4o, claude-3 | Sequential crew |
| LangGraph | workflow_builder() | gpt-4o, claude-3 | Graph workflow |

## Code Example

```python
from agentnext import *

# 1. Select framework
fw = FrameworkSelector.get_framework('crewai')

# 2. Get UI component
ui = CrewAIUI.crew_builder()

# 3. Create agent team (all OpenAI)
team = [
    {'model': 'gpt-4o', 'role': 'Researcher'},
    {'model': 'gpt-4o', 'role': 'Writer'},
    {'model': 'gpt-4o', 'role': 'Editor'},
]

# 4. Run task
# result = crew.run("Write about AI")
```

## Agent Flow: Research -> Write -> Review

```
OpenAI Agents:
  [Researcher(gpt-4o)] --> [Writer(gpt-4o)] --> [Reviewer(gpt-4o)]
        |                         |                         |
    Research task            Write content             Review output
```
