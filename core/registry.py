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
        
        # Framework features (capabilities from documentation)
        framework_features = [
            # LangGraph features
            ("checkpoints", "Checkpoints", "Save and resume state", "langgraph"),
            ("short_term_memory", "Short-term Memory", "In-process memory", "langgraph"),
            ("long_term_memory", "Long-term Memory", "Persistent storage", "langgraph"),
            ("semantic_memory", "Semantic Memory", "Embedding-based memory", "langgraph"),
            ("human_interrupt", "Human Interrupt", "Pause agent execution", "langgraph"),
            ("human_feedback", "Human Feedback", "Request human input", "langgraph"),
            ("multi_agent", "Multi-Agent", "Multiple agent orchestration", "langgraph"),
            ("function_calling", "Function Calling", "Tool/function calling", "langgraph"),
            ("code_interpreter", "Code Interpreter", "Execute code", "langgraph"),
            ("web_search", "Web Search", "Search the web", "langgraph"),
            ("streaming", "Streaming", "Stream agent output", "langgraph"),
            ("mcp", "MCP", "Model Context Protocol", "langgraph"),
            
            # LangChain features
            ("lc_checkpoints", "Checkpoints", "Save and resume state", "langchain"),
            ("lc_memory", "Memory", "In-memory缓冲", "langchain"),
            ("lc_retriever", "Retriever", "Document retriever", "langchain"),
            ("lc_vectorstore", "VectorStore", "Vector database", "langchain"),
            ("lc_embeddings", "Embeddings", "Text embeddings", "langchain"),
            ("lc_document_loader", "DocumentLoader", "Load documents", "langchain"),
            ("lc_text_splitter", "TextSplitter", "Split long text", "langchain"),
            ("lc_tools", "LC Tools", "LangChain tools", "langchain"),
            ("lc_agent", "Agent", "LangChain agent", "langchain"),
            ("lc_chain", "Chain", "LC Chain", "langchain"),
            
            # AutoGen features
            ("ag_conversable", "ConversableAgent", "Conversable agent", "autogen"),
            ("ag_user_proxy", "UserProxyAgent", "User proxy agent", "autogen"),
            ("ag_group_chat", "GroupChat", "Group chat manager", "autogen"),
            ("ag_code_executor", "CodeExecutor", "Execute code", "autogen"),
            ("ag_listener", "Listener", "Event listener", "autogen"),
            ("ag_logger", "Logger", "Logging", "autogen"),
            ("ag_cache", "Cache", "Cache agent", "autogen"),
            ("ag_human", "HumanInput", "Human input", "autogen"),
            
            # CrewAI features
            ("crew_agent", "Agent", "CrewAI agent", "crewai"),
            ("crew_task", "Task", "CrewAI task", "crewai"),
            ("crew_crew", "Crew", "Crew manager", "crewai"),
            ("crew_process", "Process", "Crew process", "crewai"),
            ("crew_memory", "Memory", "Crew memory", "crewai"),
            ("crew_storage", "Storage", "Crew storage", "crewai"),
            ("crew_knowledge", "Knowledge", "Knowledge base", "crewai"),
            ("crew_training", "Training", "Train agents", "crewai"),
            
            # OpenAI features
            ("oa_instruction", "Instruction", "Agent instructions", "openai"),
            ("oa_tools", "Tools", "OpenAI tools", "openai"),
            ("oa_model", "Model", "Model selection", "openai"),
            ("oa_context", "Context", "Context window", "openai"),
            ("oa_file_search", "File Search", "Search files", "openai"),
            ("oa_code_interpreter", "Code Interpreter", "Execute code", "openai"),
            
            # Anthropic features
            ("ac_tool_use", "Tool Use", "Claude tool use", "anthropic"),
            ("ac_computer_use", "Computer Use", "Computer use", "anthropic"),
            ("ac_mcp", "MCP", "Model Context Protocol", "anthropic"),
            ("ac_haiku", "Haiku", "Fast model", "anthropic"),
            ("ac_sonnet", "Sonnet", "Balanced model", "anthropic"),
            ("ac_opus", "Opus", "Powerful model", "anthropic"),
            
            # Google features
            ("gggemini", "Gemini", "Gemini model", "google"),
            ("gg_vertex", "Vertex AI", "Google Vertex AI", "google"),
            ("gg_search", "Google Search", "Search via Google", "google"),
            ("gg_code_execution", "Code Execution", "Execute code", "google"),
            ("gg_function", "Function Calling", "Google functions", "google"),
        ]
        for fid, name, desc, fw in framework_features:
            self._tools[fid] = ToolEntry(
                id=generate_did("tool", fid), 
                name=name, 
                description=desc, 
                namespace="tool", 
                framework=fw
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
