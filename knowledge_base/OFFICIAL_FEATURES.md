# Agent Framework Official Features

## LANGGRAPH ⭐
docs: https://docs.langgraph.ai

| Feature | Implementation |
|---------|----------------|
| **CHECKPOINTS** | |
| Save/Resume State | MemorySaver, SqliteSaver, PostgresSaver, RedisSaver |
| State History | thread_id, checkpoint_id |
| **MEMORY** | |
| Short-term | InMemoryStore |
| Long-term | PostgresStore, MongoDBStore, RedisStore |
| **HUMAN-IN-LOOP** | |
| Interrupt | interrupt() |
| Suspend | suspend_node() |
| Resume | resume() |
| **TOOLS** | |
| Function Calling | Built-in |
| Code Execution | PythonREPLTool |

---

## LANGCHAIN
docs: https://python.langchain.com

| Feature | Implementation |
|---------|----------------|
| **MEMORY** | |
| Buffer | BufferMemory |
| Window | ConversationBufferWindowMemory |
| Entity | EntityMemory |
| Summary | ConversationSummaryMemory |
| **AGENTS** | |
| Functions | create_openai_functions_agent |
| JSON | create_json_agent |
| SQL | create_sql_agent |
| Vectorstore | create_vectorstore_agent |
| **CHAINS** | |
| Basic | LLMChain |
| Chat | ConversationChain |
| RAG | RetrievalQAChain |

---

## CREWAI
docs: https://docs.crewai.com

| Feature | Implementation |
|---------|----------------|
| **AGENTS** | |
| Role-based | Agent(role=...) |
| **CREW** | |
| Orchestration | Crew(...) |
| **PROCESS** | |
| Sequential | Process.SEQUENTIAL |
| Hierarchical | Process.HIERARCHICAL |
| **MEMORY** | |
| Semantic | Memory() |
| **TOOLS** | |
| Search | SerperDevTool |
| Web Scrape | ScrapeWebsiteTool |

---

## AUTOGEN
docs: https://microsoft.github.io/autogen

| Feature | Implementation |
|---------|----------------|
| **AGENTS** | |
| Conversable | ConversableAgent |
| User Proxy | UserProxyAgent |
| **HUMAN INPUT** | |
| Never | NEVER |
| On Terminate | TERMINATE |
| Always | ALWAYS |
| **MULTI-AGENT** | |
| Group | GroupChat |
| Manager | GroupChatManager |
| **CODE** | |
| Executor | CodeExecutor |

---

## OPENAI AGENTS SDK
docs: https://platform.openai.com/docs/agents

| Feature | Implementation |
|---------|----------------|
| **TOOLS** | |
| Function Calling | Built-in |
| **STREAMING** | |
| Token Stream | response.stream() |
| **ADVANCED** | |
| Handoffs | handoff() |
| Guardrails | Guardrail class |
| Tracing | Built-in |

---

## ANTHROPIC
docs: https://docs.anthropic.com

| Feature | Implementation |
|---------|----------------|
| **AGENT LOOP** | |
| Tool Use | stop_reason: "tool_use" |
| Loop | while tool_use: execute() |
| **TOOLS** | |
| Text Editor | str_replace_based_edit_tool |
| Bash | bash tool |
| **COMPUTER USE** | |
| Screen | screen capture |
| Mouse | mouse move/click |
| Keyboard | type input |
| **MCP** | |
| Protocol | Model Context Protocol |

---

## LLAMAINDEX
docs: https://docs.llamaindex.ai

| Feature | Implementation |
|---------|----------------|
| **INDEXING** | |
| Vector | VectorStoreIndex |
| Summary | SummaryIndex |
| Knowledge Graph | KnowledgeGraphIndex |
| **QUERY** | |
| Retriever | RetrieverQueryEngine |
| **AGENTS** | |
| Query | QueryEngineAgent |
| ReAct | ReActAgent |
| **CONNECTORS** | |
| PDF | PDFReader |
| CSV | CSVReader |
| SQL | SQLDatabaseReader |

---

## LITELLM
docs: https://docs.litellm.ai

| Feature | Implementation |
|---------|----------------|
| **LLM PROXY** | |
| Providers | OpenAI, Anthropic, Azure, Google |
| **STREAMING** | |
| Token | stream=True |
| **LOGGING** | |
| Langfuse | LangfuseLogger |
| LangSmith | LangSmithLogger |
| **CACHING** | |
| Redis | RedisCache |
| In-memory | GPTCache |

---

## GITHUB COPILOT
docs: https://docs.github.com/en/copilot

| Feature | Implementation |
|---------|----------------|
| **CHAT** | |
| UI | Copilot Chat |
| IDE | VS Code, IntelliJ |
| CLI | gh copilot |
| **CUSTOM AGENTS** | |
| Build | Create custom |
| Skills | Add skills |
| **MEMORY** | |
| Context | Project memory |
| Enterprise | Enterprise knowledge |

---

## SALESFORCE AGENTFORCE
docs: https://developer.salesforce.com/docs/ai/agentforce

| Feature | Implementation |
|---------|----------------|
| **BUILDER** | |
| No-code | Agent Builder |
| **INTEGRATION** | |
| Flow | Flow Builder |
| Apex | Apex actions |
| **SECURITY** | |
| Trust | Einstein Trust Layer |
| **TOPICS** | |
| Trigger | Topic Launcher |

---

## GOOGLE VERTEX AI
docs: https://cloud.google.com/vertex-ai/docs

| Feature | Implementation |
|---------|----------------|
| **MODELS** | |
| Gemini | Gemini models |
| **AGENT** | |
| Builder | Agent Builder |
| **GROUNDING** | |
| Search | Vertex Search |
| **KNOWLEDGE** | |
| Base | Knowledge Base |

---

## AWS BEDROCK
docs: https://docs.aws.amazon.com/bedrock/

| Feature | Implementation |
|---------|----------------|
| **MODELS** | |
| Amazon | Titan |
| Anthropic | Claude |
| Meta | Llama |
| Mistral | Mistral |
| **AGENTS** | |
| Bedrock | Bedrock Agents |
| **KNOWLEDGE** | |
| Base | Knowledge Base |
| **GUARDRAILS** | |
| Content | Bedrock Guardrails |

---

## MICROSOFT AZURE AI
docs: https://learn.microsoft.com/azure/ai-services/

| Feature | Implementation |
|---------|----------------|
| **OPENAI** | |
| Azure | Azure OpenAI |
| **FOUNDRY** | |
| Platform | AI Foundry |
| **AGENTS** | |
| Build | AI Agents |
| **FABRIC** | |
| Data | Microsoft Fabric |

---

## MCP (Model Context Protocol)
docs: https://modelcontextprotocol.io

| Feature | Implementation |
|---------|----------------|
| **SERVERS** | |
| Filesystem | Filesystem server |
| GitHub | GitHub server |
| Postgres | Postgres server |
| **CLIENT** | |
| SDK | Python, TypeScript |

---

## SMOLAGENTS (HuggingFace)
docs: https://smolagents.ai

| Feature | Implementation |
|---------|----------------|
| **AGENTS** | |
| Code | CodeAgent |
| ReAct | ReactAgent |
| **CODE** | |
| Interpreter | Python interpreter |
| **MODELS** | |
| HuggingFace | transformers, inference API |

---

## DOCKER
docs: https://docs.docker.com

| Feature | Implementation |
|---------|----------------|
| **BUILD** | |
| Assistant | Docker AI |
| **COMPOSE** | |
| Multi-container | Compose |
| **SECURITY** | |
| Scanning | Docker Scout |
