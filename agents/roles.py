"""
Enterprise Agent Config - Own registries.

We own: MCP, Memory System, RAG, Capabilities, Tools, Skills.
External: Identity (SSO), Secret (Secret Manager).
"""

from enum import Enum
from typing import Optional, List
from dataclasses import dataclass, field


class AgentRole(Enum):
    PROJECT_DRIVER = "project_driver"
    PRODUCT_LEAD = "product_lead"
    GROUP_ADMIN = "group_admin"
    TEAM_LEAD = "team_lead"
    EMPLOYEE_ASSISTANT = "assistant"


# === REGISTRIES (we own these) ===

class MCPRegistry:
    """MCP - Model Context Protocol registry."""
    def __init__(self):
        self._tools = {}
        self._resources = {}
        self._prompts = {}
    
    def register_tool(self, name: str, tool_fn):
        self._tools[name] = tool_fn
    def register_resource(self, uri: str, data):
        self._resources[uri] = data
    def register_prompt(self, name: str, prompt: str):
        self._prompts[name] = prompt


class MemorySystem:
    """Memory system - session, context, history."""
    def __init__(self):
        self._sessions = {}
        self._context = {}
        self._history = {}
    
    def create_session(self, session_id: str):
        self._sessions[session_id] = {"id": session_id, "messages": []}
    def add_message(self, session_id: str, role: str, content: str):
        if session_id in self._sessions:
            self._sessions[session_id]["messages"].append({"role": role, "content": content})


class RAGRegistry:
    """RAG - Knowledge base registry."""
    def __init__(self):
        self._knowledge_bases = {}
        self._embeddings = {}
        self._retrievers = {}
    
    def register_kb(self, name: str, kb_config: dict):
        self._knowledge_bases[name] = kb_config
    def register_retriever(self, name: str, retriever_fn):
        self._retrievers[name] = retriever_fn


class ToolRegistry:
    """Tool registry - function calls, APIs."""
    def __init__(self):
        self._tools = {}
    
    def register(self, name: str, tool_fn, description: str = ""):
        self._tools[name] = {"fn": tool_fn, "description": description}


class CapabilityRegistry:
    """Capability registry - LLM features."""
    def __init__(self):
        self._capabilities = {}
    
    def register(self, name: str, capability_fn):
        self._capabilities[name] = capability_fn


class SkillRegistry:
    """Skill registry - agent skills."""
    def __init__(self):
        self._skills = {}
        self._skills_by_role = {}
    
    def register(self, name: str, skill_config: dict, role: str = None):
        self._skills[name] = skill_config
        if role:
            if role not in self._skills_by_role:
                self._skills_by_role[role] = []
            self._skills_by_role[role].append(name)


# === GLOBAL REGISTRIES ===
mcp_registry = MCPRegistry()
memory_system = MemorySystem()
rag_registry = RAGRegistry()
tool_registry = ToolRegistry()
capability_registry = CapabilityRegistry()
skill_registry = SkillRegistry()


# === AGENT CONFIG ===

@dataclass
class AgentConfig:
    """Enterprise agent config - we own MCP/Memory/RAG/Tools/Capabilities/Skills."""
    role: AgentRole
    
    # === IDENTITY (external) ===
    identity_id: str          # From SSO/IdP
    identity_provider: str   # entra/okta/google
    
    # === SECRET (external) ===
    secret_ref: str          # From secret manager
    
    # === GOVERNANCE (required) ===
    owner: str
    sponsor: str
    
    # === SCOPE ===
    reports_to: Optional[str] = None
    projects: List[str] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    engages_with: List[str] = field(default_factory=list)
    manages: List[str] = field(default_factory=list)
    
    # === OUR REGISTRIES ===
    
    # MCP (our tools, resources, prompts)
    mcp_tools: List[str] = field(default_factory=list)
    mcp_resources: List[str] = field(default_factory=list)
    mcp_prompts: List[str] = field(default_factory=list)
    
    # Memory (our session/context)
    memory_type: str = "session"  # session/context/echoic
    
    # RAG / Knowledge (our knowledge bases)
    knowledge_bases: List[str] = field(default_factory=list)
    
    # Capabilities (our LLM features)
    capabilities: List[str] = field(default_factory=list)
    
    # Tools (our function calls)
    tools: List[str] = field(default_factory=list)
    
    # Skills (our agent skills)
    skills: List[str] = field(default_factory=list)
    
    # Employee Assistant
    employee_email: Optional[str] = None
    it_admin_defaults: dict = field(default_factory=dict)
    employee_overrides: dict = field(default_factory=dict)
    
    # === RUNTIME ===
    orchestrator: str = "langgraph"
    llm: Optional[str] = None


ROLE_DEFAULTS = {
    AgentRole.PROJECT_DRIVER: {"orchestrator": "langgraph", "llm": "gpt-4o"},
    AgentRole.PRODUCT_LEAD: {"orchestrator": "langgraph", "llm": "gpt-4o"},
    AgentRole.GROUP_ADMIN: {"orchestrator": "langgraph", "llm": "gemini-2.0-flash"},
    AgentRole.TEAM_LEAD: {"orchestrator": "langgraph", "llm": "gpt-4"},
    AgentRole.EMPLOYEE_ASSISTANT: {"orchestrator": "langgraph", "llm": "gemini-2.0-flash"},
}


ROLE_BEHAVIORS = {
    AgentRole.PROJECT_DRIVER: {"behavior": "drives", "delegates": True, "approves": True},
    AgentRole.PRODUCT_LEAD: {"behavior": "owns", "delegates": True, "approves": True},
    AgentRole.GROUP_ADMIN: {"behavior": "collaborates", "facilitates": True, "engages": True},
    AgentRole.TEAM_LEAD: {"behavior": "leads", "manages": True, "coaches": True},
    AgentRole.EMPLOYEE_ASSISTANT: {"behavior": "assists", "supports": True},
}


# === REGISTRY FUNCTIONS ===

def create_mcp_tool(name: str, tool_fn):
    """Register an MCP tool."""
    mcp_registry.register_tool(name, tool_fn)

def create_session(session_id: str):
    """Create agent memory session."""
    memory_system.create_session(session_id)

def register_knowledge_base(name: str, kb_config: dict):
    """Register a knowledge base."""
    rag_registry.register_kb(name, kb_config)

def register_tool(name: str, tool_fn, description: str = ""):
    """Register a tool."""
    tool_registry.register(name, tool_fn, description)

def register_capability(name: str, capability_fn):
    """Register a capability."""
    capability_registry.register(name, capability_fn)

def register_skill(name: str, skill_config: dict, role: str = None):
    """Register a skill."""
    skill_registry.register(name, skill_config, role)
