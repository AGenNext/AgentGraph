# Multi-Agent Team - Content Writing System with A2A

## Project Overview
- **Project Name**: Multi-Agent Content Writing Team
- **Type**: Collaborative AI agent team with A2A protocol
- **Core Functionality**: A team of specialized AI agents (OpenAI, Salesforce, Microsoft, Google) that collaborate via Agent-to-Agent (A2A) communication, orchestrated by LangGraph
- **Target Users**: Content teams, marketing departments, agencies needing collaborative AI writing

## Architecture

### Agent Communication Protocol (A2A)
- JSON-RPC 2.0 based protocol for inter-agent communication
- Task-based messaging with status tracking
- Agent cards for capability discovery
- Streaming support for real-time content generation
- **Team Coordination**: Agents delegate tasks, share context, and aggregate results

### Multi-Agent Team

#### 1. OpenAI Agent (Creative Writer)
- **Model**: GPT-4 / GPT-4o
- **Role**: Creative content, storytelling, blog posts
- **A2A Capabilities**: generate_creative, write_blog, storytelling

#### 2. Salesforce Agent (Sales Writer)  
- **Model**: Einstein AI / Salesforce CRM
- **Role**: Sales copy, business content, CRM data integration
- **A2A Capabilities**: sales_copy, business_content, crm_integration

#### 3. Microsoft Agent (Enterprise Writer)
- **Model**: Azure OpenAI / Copilot
- **Role**: Enterprise content, technical docs, Microsoft 365 integration
- **A2A Capabilities**: enterprise_content, technical_docs, m365_integration

#### 4. Google Agent (Research Writer)
- **Model**: Gemini / Vertex AI
- **Role**: Research, factual content, SEO optimization
- **A2A Capabilities**: research_content, seo_optimization, factual_writing

### LangGraph Team Orchestrator
- **Team State**: Shared context across agents
- **Workflow**: Parallel execution with aggregation
- **Leader Election**: Coordinator agent for task distribution
- **Result Synthesis**: Combine outputs from all agents

## Functionality Specification

### Core Features

1. **Team Coordinator**
   - Analyze content request
   - Delegate to appropriate agents
   - Coordinate A2A communication
   - Aggregate team results

2. **A2A Team Communication**
   - Agent discovery via agent cards
   - Task delegation between team agents
   - Result sharing and synthesis
   - Collaborative writing workflow

3. **Parallel Generation**
   - Request content from multiple agents
   - Aggregate and synthesize results
   - Quality scoring and selection

4. **Content Types Supported**
   - Blog posts (OpenAI lead)
   - Marketing copy (Salesforce lead)
   - Technical documentation (Microsoft lead)
   - SEO content (Google lead)
   - Enterprise campaigns (mult-agent)

### Team Data Flow
1. User input → Team Coordinator → Agent selection
2. Selected agents → A2A task distribution
3. Agent responses → Result synthesis
4. Synthesized content → User output

### Team Roles
- **Coordinator**: Orchestrates team workflow (LangGraph)
- **Primary Agent**: Leads specific content type
- **Support Agents**: Provide supplementary content
- **Synthesis Agent**: Combines outputs

### Data Flow
1. User input → LangGraph router → SDK agents (parallel)
2. Agent responses → Aggregation node → Quality scoring
3. Best content → User output with A2A metadata

## File Structure
```
content-writing-agent/
├── main.py                 # Entry point
├── agents/
│   ├── __init__.py
│   ├── openai_agent.py    # OpenAI agent implementation
│   ├── salesforce_agent.py # Salesforce agent
│   ├── microsoft_agent.py  # Microsoft Azure agent
│   ├── google_agent.py     # Google ADK agent
│   └── base_agent.py      # Base agent class
├── orchestrator/
│   ├── __init__.py
│   └── langgraph_workflow.py # LangGraph definition
├── a2a/
│   ├── __init__.py
│   ├── protocol.py        # A2A protocol implementation
│   ├── card.py           # Agent card
│   └── client.py         # A2A client
├── core/
│   ├── __init__.py
│   ├── router.py         # Content router
│   ├── aggregator.py     # Response aggregator
│   └── scorer.py         # Quality scorer
├── config.py             # Configuration
├── requirements.txt     # Dependencies
└── pyproject.toml      # Project metadata
```

## Acceptance Criteria

1. ✓ LangGraph orchestrates multiple SDK agents
2. ✓ Each SDK has working agent implementation
3. ✓ A2A protocol enables agent communication
4. ✓ Content can be generated in parallel
5. ✓ Responses are aggregated and scored
6. ✓ Type hints and docstrings throughout
7. ✓ Proper error handling
8. ✓ Configuration via environment variables