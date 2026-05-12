# AGenNext Enterprise - Database Schema

## Overview

PostgreSQL database with Prisma ORM for multi-framework agent backend.

## Connection

```env
DATABASE_URL=postgresql://agent:agent@postgres:5432/agent
```

## Schema Models

### Task

Represents an agent task execution.

| Field | Type | Description |
|-------|------|------------|
| id | String (UUID) | Primary key |
| status | TaskStatus | Current task status |
| framework | FrameworkType | Agent framework used |
| submission | JSON | TaskSubmission object |
| context | JSON? | TaskContext when provided |
| result | JSON? | Execution result |
| createdAt | DateTime | Creation timestamp |

### Checkpoint

Snapshot of task state for resume/learning.

| Field | Type | Description |
|-------|------|------------|
| id | Int | Primary key (auto) |
| taskId | String | FK to Task |
| step | Int | Checkpoint step number |
| learnings | String[] | Array of learnings |
| decisions | JSON[] | Decision history |
| mistakesFixed | JSON[] | Fixed mistakes |
| context | JSON? | Full context snapshot |
| savedAt | DateTime | Save timestamp |

### Learning

Individual learning from task execution.

| Field | Type | Description |
|-------|------|------------|
| id | Int | Primary key (auto) |
| taskId | String | FK to Task |
| learning | String | Learning text |
| createdAt | DateTime | Creation timestamp |

## Enums

### TaskStatus

- `PENDING_CONTEXT` - Waiting for context input
- `RUNNING` - Currently executing
- `COMPLETED` - Successfully finished
- `STOPPED` - Manually stopped
- `FAILED` - Execution failed

### FrameworkType

- `LANGGRAPH` - LangGraph
- `LANGCHAIN` - LangChain
- `AUTOGEN` - Microsoft AutoGen
- `CREWAI` - CrewAI
- `OPENAI` - OpenAI Agents SDK
- `ANTHROPIC` - Anthropic Claude
- `CUSTOM` - Custom agent

## API Registry Integration

### Agents Using This Schema

| Agent | Framework | Uses Schema |
|-------|----------|-----------|
| openai_agent.py | OPENAI | Task, Checkpoint |
| langgraph_client.py | LANGGRAPH | Task, Checkpoint, Learning |
| langchain_client.py | LANGCHAIN | Task, Checkpoint |
| crewai_agent.py | CREWAI | Task, Checkpoint |
| autogen_agent.py | AUTOGEN | Task, Checkpoint |
| coordinator.py | CUSTOM | Task, Learning |

### Endpoints Using This Schema

- `POST /tasks` - Create task → Task model
- `GET /tasks/{id}` - Get task → Task model  
- `POST /tasks/{id}/checkpoint` - Save checkpoint → Checkpoint model
- `GET /tasks/{id}/learnings` - Get learnings → Learning[]

## Migrations

Run migrations with:
```bash
npx prisma migrate dev --name init
npx prisma generate
```