"""LlamaIndex Agent SDK - Data-augmented LLM agents."""

from typing import Optional, List, Any
import os

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig


class LlamaIndexAgent(BaseAgent):
    """LlamaIndex (formerly GPT Index) agent specialist.
    
    Capabilities:
    - Query engine generation
    - Data agents
    - Chat engines
    - Router configs
    - Tool definitions
    - Index creation
    
    Tools: QueryEngine, ChatEngine, Router, DataAgent
    Skills: rag, data-querying, document-search, tool-augmented
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            agent_id="llamaindex-writer",
            name="LlamaIndex Agent Writer",
            description="LlamaIndex - RAG agents, query engines, data tools",
            capabilities=[
                "query_engine",
                "data_agent",
                "chat_engine",
                "router_config",
                "tool_definition",
                "index_creation",
            ],
            skills=["rag", "data-querying", "document-search", "indexing", "tool-augmented"],
            api_key=api_key or os.getenv("LLM_API_KEY"),
        )
        
        self.llm_config = LLMConfig.from_env()
        self._llm = None
    
    def _get_port(self) -> int:
        return 8008
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        if "query" in ct:
            return self._query_engine(request)
        elif "chat" in ct:
            return self._chat_engine(request)
        elif "agent" in ct or "data" in ct:
            return self._data_agent(request)
        elif "router" in ct:
            return self._router_config(request)
        elif "index" in ct:
            return self._index_creation(request)
        else:
            return self._tool_def(request)
    
    def _query_engine(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""Query Engine for {request.topic}"""

from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.chat_engine import CondenseQuestionChatEngine

# Load data
documents = SimpleDirectoryReader("data/").load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)

# Create query engine
query_engine = index.as_query_engine(
    similarity_top_k=3,
    response_mode="tree_summarize",
)

# Use it
response = query_engine.query("Your question here")
print(response)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "query-engine", "skill": "rag"},
        )
    
    def _chat_engine(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""Chat Engine for {request.topic}"""

from llama_index import VectorStoreIndex
from llama_index.chat_engine import CondenseQuestionChatEngine

# Create index
index = VectorStoreIndex.from_documents(documents)

# Create chat engine with memory
chat_engine = CondenseQuestionChatEngine.from_defaults(
    llm=llm,
    chat_history=[],  # Add memory here
)

# Start chatting
response = chat_engine.chat("Your message")
print(response.response)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "chat-engine", "skill": "rag"},
        )
    
    def _data_agent(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""Data Agent for {request.topic}"""

from llama_index.indices.struct_type import IndexStructType
from llama_index.agent import OpenAIAgent

# Create data agent with tools
agent = OpenAIAgent.from_tools(
    [
        # Query engine tool
        query_engine_tool,
        # File read tool
        read_file_tool,
        # Custom tools
    ],
    llm=llm,
    verbose=True,
)

# Run agent
response = agent.chat("Your question about the data")
print(response.response)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "data-agent", "skill": "tool-augmented"},
        )
    
    def _router_config(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""Router Config for {request.topic}"""

from llama_index import VectorStoreIndex, SummaryIndex
from llama_index.objects import ObjectMapping

# Create multiple indices
vector_index = VectorStoreIndex.from_documents(v_docs)
summary_index = SummaryIndex.from_documents(s_docs)

# Configure router
from llama_index.query_engine.router_query_engine import RouterQueryEngine

router = RouterQueryEngine.from_defaults(
    selector=LLMMultiSelector.from_defaults(),
    query_engine_tools=[
        vector_index.as_query_engine(),
        summary_index.as_query_engine(),
    ],
)

# Auto-select based on query
response = router.query("Your question")
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "router", "skill": "rag"},
        )
    
    def _index_creation(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""Index Creation for {request.topic}"""

from llama_index import (
    VectorStoreIndex,
    SummaryIndex,
    KnowledgeGraphIndex,
)
from llama_index.storage.storage_context import StorageContext

# Vector index (semantic search)
vector_idx = VectorStoreIndex.from_documents(docs)

# Summary index (LLM summaries)
summary_idx = SummaryIndex.from_documents(docs)

# Knowledge graph (relationships)
kg_idx = KnowledgeGraphIndex.from_documents(
    docs,
    kg_triplet_extract_fn=extract_triplets,
)

# Persist
storage_context.persist(persist_dir="index storage/")
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "index-creation", "skill": "indexing"},
        )
    
    def _tool_def(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""LlamaIndex Tool for {request.topic}"""

from llama_index.tools import QueryEngineTool, ToolMetadata

# Create query engine tool
query_tool = QueryEngineTool(
    query_engine,
    metadata=ToolMetadata(
        name="{request.topic.lower().replace(' ', '_')}",
        description="Query {request.topic} data",
    ),
)

# Use with OpenAI agent
from llama_index.agent import OpenAIAgent
agent = OpenAIAgent.from_tools([query_tool])
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "tool-definition", "skill": "tool-augmented"},
        )