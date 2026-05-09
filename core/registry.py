"""Registry System - Internal Decentralized IDs.

Internal DID format: did:content-team:{namespace}:{name}:v{version}

For WaltID blockchain integration (separate repo), use:
- WALTID_API_URL
- WALTID_API_KEY  
- WALTID_ISSUER_DID
"""

import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


def generate_did(namespace: str, name: str, version: str = "v1") -> str:
    return f"did:content-team:{namespace}:{name}:{version}"


def parse_did(did: str) -> Dict[str, str]:
    parts = did.split(":")
    if len(parts) >= 5:
        return dict(zip(["scheme", "authority", "namespace", "name", "version"], parts))
    return {}


@dataclass
class RegistryEntry:
    id: str
    name: str
    description: str
    namespace: str
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    version: str = "v1"


@dataclass
class SkillEntry(RegistryEntry):
    namespace: str = "skill"


@dataclass
class PromptEntry(RegistryEntry):
    namespace: str = "prompt"


@dataclass
class ToolEntry(RegistryEntry):
    namespace: str = "tool"
    framework: Optional[str] = None
    kind: str = "class"  # class, function
    category: str = "core"  # core, agent, model, memory, tool, utils
    parameters: dict = field(default_factory=dict)
    config_schema: dict = field(default_factory=dict)
    api_spec: Optional[str] = None  # OpenAPI spec for the tool


class Registry:
    def __init__(self):
        self._skills: Dict[str, SkillEntry] = {}
        self._prompts: Dict[str, PromptEntry] = {}
        self._tools: Dict[str, ToolEntry] = {}
        self._load_builtins()
    
    def _load_builtins(self):
        # Built-in skills
        for sid, name, desc in [("coding", "Coding", "Generate code"), ("research", "Research", "Research")]:
            self._skills[sid] = SkillEntry(id=generate_did("skill", sid), name=name, description=desc, namespace="skill")
        # Built-in prompts
        for pid, name, desc in [("creative", "Creative Writing", "Creative content")]:
            self._prompts[pid] = PromptEntry(id=generate_did("prompt", pid), name=name, description=desc, namespace="prompt")
        
        # Framework tools with full config
        framework_tools = [
            # LangGraph SDK core classes
            ("state_graph", "StateGraph", "Create state-based graphs", "langgraph", "class", "agent", 
             {}, {"state_schema": {"type": "object", "description": "State schema"}}),
            ("react_agent", "ReAct Agent", "Reasoning + Action agent", "langgraph", "class", "agent",
             {}, {"llm": {"type": "object"}, "tools": {"type": "array"}}),
            ("tool_node", "ToolNode", "Execute tools in graph", "langgraph", "class", "tool",
             {}, {"tool": {"type": "function"}}),
            ("chat_model", "ChatOpenAI", "OpenAI chat model", "langgraph", "class", "model",
             {}, {"model": {"type": "string", "default": "gpt-4"}, "temperature": {"type": "number"}}),
            ("agent_executor", "AgentExecutor", "Run agent with tools", "langgraph", "class", "agent",
             {}, {"agent": {"type": "object"}, "tools": {"type": "array"}}),
            ("streaming", "Streaming", "Stream agent output", "langgraph", "function", "utils", {}, {}),
            ("checkpoint", "CheckpointSaver", "Save checkpoint", "langgraph", "class", "memory", {}, {}),
            
            # LangChain
            ("llm_chain", "LLMChain", "LLM chain wrapper", "langchain", "class", "agent",
             {}, {"llm": {"type": "object"}, "prompt": {"type": "string"}}),
            ("retriever", "Retriever", "Document retriever", "langchain", "class", "tool", {}, {}),
            ("vectorstore", "VectorStore", "Vector database", "langchain", "class", "memory",
             {}, {"embedding_function": {"type": "function"}}),
            ("embeddings", "Embeddings", "Text embeddings", "langchain", "class", "model", {}, {}),
            ("document_loader", "DocumentLoader", "Load documents", "langchain", "class", "utils", {}, {}),
            ("text_splitter", "TextSplitter", "Split long text", "langchain", "class", "utils", 
             {}, {"chunk_size": {"type": "number", "default": 1000}}),
            
            # AutoGen
            ("assistant", "AssistantAgent", "Multi-agent assistant", "autogen", "class", "agent",
             {}, {"name": {"type": "string"}, "llm_config": {"type": "object"}}),
            ("user_proxy", "UserProxyAgent", "User proxy agent", "autogen", "class", "agent",
             {}, {"human_input_mode": {"type": "string"}}),
            ("group_chat", "GroupChat", "Groupchat manager", "autogen", "class", "agent",
             {}, {"agents": {"type": "array"}}),
            ("code_executor", "CodeExecutor", "Execute code", "autogen", "class", "tool", {}, {}),
            
            # CrewAI
            ("agent_crew", "Agent", "CrewAI agent", "crewai", "class", "agent",
             {}, {"role": {"type": "string"}, "goal": {"type": "string"}}),
            ("task_crew", "Task", "CrewAI task", "crewai", "class", "agent",
             {}, {"description": {"type": "string"}, "agent": {"type": "object"}}),
            ("crew_crew", "Crew", "Crew manager", "crewai", "class", "agent",
             {}, {"agents": {"type": "array"}, "tasks": {"type": "array"}}),
            ("process_crew", "Process", "Crew process", "crewai", "class", "utils", {}, {}),
            
            # OpenAI
            ("gpt4", "GPT-4", "GPT-4 model", "openai", "class", "model",
             {}, {"model": {"type": "string", "default": "gpt-4"}, "temperature": {"type": "number"}}),
            ("gpt35", "GPT-3.5", "GPT-3.5 model", "openai", "class", "model", {}, {}),
            ("dalle", "DALL-E", "Image generation", "openai", "class", "model",
             {}, {"model": {"type": "string"}, "size": {"type": "string"}}),
            ("whisper", "Whisper", "Speech to text", "openai", "class", "tool", {}, {}),
            ("tts", "TTS", "Text to speech", "openai", "class", "tool", {}, {}),
            
            # Anthropic
            ("claude3opus", "Claude 3 Opus", "Claude 3 Opus", "anthropic", "class", "model",
             {}, {"model": {"type": "string"}, "max_tokens": {"type": "number"}}),
            ("claude3sonnet", "Claude 3 Sonnet", "Claude 3 Sonnet", "anthropic", "class", "model", {}, {}),
            ("claude3haiku", "Claude 3 Haiku", "Claude 3 Haiku", "anthropic", "class", "model", {}, {}),
            
            # Google
            ("gemini", "Gemini", "Gemini model", "google", "class", "model",
             {}, {"model": {"type": "string"}, "temperature": {"type": "number"}}),
            ("vertex_ai", "Vertex AI", "Google Vertex AI", "google", "class", "model", {}, {}),
            ("google_search", "Google Search", "Search via Google", "google", "function", "tool", {}, {}),
        ]
        for tid, name, desc, fw, kind, cat, params, config in framework_tools:
            self._tools[tid] = ToolEntry(
                id=generate_did("tool", tid), 
                name=name, 
                description=desc, 
                namespace="tool", 
                framework=fw,
                kind=kind,
                category=cat,
                parameters=params,
                config_schema=config
            )
    
    def get_skill(self, name: str) -> Optional[SkillEntry]:
        return self._skills.get(name)
    def get_prompt(self, name: str) -> Optional[PromptEntry]:
        return self._prompts.get(name)
    def get_tool(self, name: str) -> Optional[ToolEntry]:
        return self._tools.get(name)
    def list_skills(self) -> List[SkillEntry]:
        return list(self._skills.values())
    def list_prompts(self) -> List[PromptEntry]:
        return list(self._prompts.values())
    def list_tools(self) -> List[ToolEntry]:
        return list(self._tools.values())


REGISTRY = Registry()


def get_registry() -> Registry:
    return REGISTRY
