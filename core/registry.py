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
        
        # Framework tools (populated from integrations)
        framework_tools = [
            # LangGraph tools
            ("web_search", "Web Search", "Search the web for information", "langgraph"),
            ("state_graph", "StateGraph", "Create state-based graphs", "langgraph"),
            ("react_agent", "ReAct Agent", "Reasoning + Action agent", "langgraph"),
            ("tool_node", "ToolNode", "Execute tools in graph", "langgraph"),
            ("chat_model", "ChatOpenAI", "OpenAI chat model", "langgraph"),
            ("llm_chain", "LLMChain", "LLM chain wrapper", "langgraph"),
            ("agent_executor", "AgentExecutor", "Run agent with tools", "langgraph"),
            ("streaming", "Streaming", "Stream agent output", "langgraph"),
            ("checkpoint", "CheckpointSaver", "Save checkpoint", "langgraph"),
            ("memory", "Memory", "Agent memory", "langgraph"),
            
            # LangChain tools
            ("langchain_code", "LangChain Code", "Generate LangChain code", "langchain"),
            ("tool_use", "Tool Use", "Use tools in chains", "langchain"),
            ("retriever", "Retriever", "Document retriever", "langchain"),
            ("vectorstore", "VectorStore", "Vector database", "langchain"),
            ("embeddings", "Embeddings", "Text embeddings", "langchain"),
            ("document_loader", "DocumentLoader", "Load documents", "langchain"),
            ("text_splitter", "TextSplitter", "Split long text", "langchain"),
            ("hub", "Hub", "LangChain hub", "langchain"),
            
            # AutoGen tools  
            ("autogen_code", "AutoGen Code", "Generate AutoGen agents", "autogen"),
            ("assistant", "AssistantAgent", "Multi-agent assistant", "autogen"),
            ("user_proxy", "UserProxyAgent", "User proxy agent", "autogen"),
            ("group_chat", "GroupChat", "Groupchat manager", "autogen"),
            ("code_executor", "CodeExecutor", "Execute code", "autogen"),
            
            # CrewAI tools
            ("crewai_code", "CrewAI Code", "Generate CrewAI pipelines", "crewai"),
            ("agent_crew", "Agent", "CrewAI agent", "crewai"),
            ("task_crew", "Task", "CrewAI task", "crewai"),
            ("crew_crew", "Crew", "Crew manager", "crewai"),
            ("process_crew", "Process", "Crew process", "crewai"),
            
            # OpenAI tools
            ("openai_api", "OpenAI API", "Interact with OpenAI models", "openai"),
            ("gpt4", "GPT-4", "GPT-4 model", "openai"),
            ("gpt35", "GPT-3.5", "GPT-3.5 model", "openai"),
            ("dalle", "DALL-E", "Image generation", "openai"),
            ("whisper", "Whisper", "Speech to text", "openai"),
            ("tts", "TTS", "Text to speech", "openai"),
            
            # Anthropic tools
            ("anthropic_api", "Anthropic API", "Interact with Claude models", "anthropic"),
            ("claude3", "Claude 3", "Claude 3 model", "anthropic"),
            ("claude3opus", "Claude 3 Opus", "Claude 3 Opus", "anthropic"),
            ("claude3sonnet", "Claude 3 Sonnet", "Claude 3 Sonnet", "anthropic"),
            ("claude3haiku", "Claude 3 Haiku", "Claude 3 Haiku", "anthropic"),
            ("claude2", "Claude 2", "Claude 2 model", "anthropic"),
            
            # Google tools
            ("google_search", "Google Search", "Search via Google", "google"),
            ("gemini", "Gemini", "Gemini model", "google"),
            ("vertex_ai", "Vertex AI", "Google Vertex AI", "google"),
        ]
        for tid, name, desc, fw in framework_tools:
            self._tools[tid] = ToolEntry(id=generate_did("tool", tid), name=name, description=desc, namespace="tool", framework=fw)
    
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
