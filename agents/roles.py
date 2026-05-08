"""
Enterprise Agent Config - capabilities from AI provider based on model.

We own: MCP, Memory, RAG, Tools, Skills.
AI Provider: provides capabilities based on model.
External: Identity, Secret.
"""

from enum import Enum
from typing import Optional, List, Dict
from dataclasses import dataclass, field


class AgentRole(Enum):
    PROJECT_DRIVER = "project_driver"
    PRODUCT_LEAD = "product_lead"
    GROUP_ADMIN = "group_admin"
    TEAM_LEAD = "team_lead"
    EMPLOYEE_ASSISTANT = "assistant"


# === AI PROVIDER REGISTRY ===

class AIProvider:
    """AI Provider - capabilities based on model."""
    
    # Model -> capabilities mapping
    MODEL_CAPABILITIES = {
        # GPT-4o family
        "gpt-4o": ["vision", "function-calling", "json", "streaming", "text-to-speech", "dall-e-3", "realtime"],
        "gpt-4o-mini": ["function-calling", "json", "streaming"],
        
        # Claude family  
        "claude-3-5-sonnet": ["vision", "function-calling", "json", "streaming", "thinking", "text-to-speech"],
        "claude-3-opus": ["vision", "function-calling", "json", "streaming", "thinking"],
        
        # Gemini family
        "gemini-2.0-flash": ["vision", "function-calling", "json", "streaming", "native-tools", "text-to-speech", "image-generation"],
        "gemini-2.0-flash-lite": ["function-calling", "json", "streaming"],
        
        # Azure OpenAI
        "azure-gpt-4o": ["vision", "function-calling", "json"],
        "azure-claude": ["vision", "function-calling"],
        
        # Groq
        "groq-llama-3": ["function-calling", "streaming"],
        "groq-mixtral": ["function-calling", "streaming"],
    }
    
    def __init__(self):
        self._providers = {}
        self._models = {}
    
    def register(self, provider_name: str, api_key: str, base_url: str = None):
        """Register AI provider."""
        self._providers[provider_name] = {
            "api_key": api_key,
            "base_url": base_url,
        }
    
    def add_model(self, provider_name: str, model_name: str, capabilities: List[str] = None):
        """Add model to provider."""
        if model_name not in self.MODEL_CAPABILITIES:
            self._models[model_name] = {
                "provider": provider_name,
                "capabilities": capabilities or [],
            }
    
    def get_capabilities(self, model_name: str) -> List[str]:
        """Get capabilities for a model."""
        return self.MODEL_CAPABILITIES.get(model_name, [])
    
    def get_provider(self, model_name: str) -> Optional[str]:
        """Get provider name for a model."""
        return self._models.get(model_name, {}).get("provider")


ai_provider = AIProvider()


# === MCP REGISTRY ===

class MCPRegistry:
    """MCP registry."""
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


# === MEMORY SYSTEM ===

class MemorySystem:
    """Memory system."""
    def __init__(self):
        self._sessions = {}
    def create_session(self, session_id: str):
        self._sessions[session_id] = {"id": session_id, "messages": []}


# === RAG REGISTRY ===

class RAGRegistry:
    """RAG registry."""
    def __init__(self):
        self._knowledge_bases = {}
    def register_kb(self, name: str, kb_config: dict):
        self._knowledge_bases[name] = kb_config


# === TOOL REGISTRY ===

class ToolRegistry:
    """Tool registry."""
    def __init__(self):
        self._tools = {}
    def register(self, name: str, tool_fn, description: str = ""):
        self._tools[name] = {"fn": tool_fn, "description": description}


# === SKILL REGISTRY ===

class SkillRegistry:
    """Skill registry."""
    def __init__(self):
        self._skills = {}
    def register(self, name: str, skill_config: dict, role: str = None):
        self._skills[name] = skill_config


# === GLOBAL REGISTRIES ===
mcp_registry = MCPRegistry()
memory_system = MemorySystem()
rag_registry = RAGRegistry()
tool_registry = ToolRegistry()
skill_registry = SkillRegistry()


# === AGENT CONFIG ===

@dataclass
class AgentConfig:
    """Enterprise agent config."""
    role: AgentRole
    
    # === EXTERNAL ===
    identity_id: str
    identity_provider: str
    secret_ref: str
    
    # === GOVERNANCE ===
    owner: str
    sponsor: str
    
    # === SCOPE ===
    reports_to: Optional[str] = None
    projects: List[str] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    engages_with: List[str] = field(default_factory=list)
    manages: List[str] = field(default_factory=list)
    
    # === AI PROVIDER (capabilities from model) ===
    ai_provider_name: str = "openai"
    model: str = "gpt-4o"
    
    # === OUR REGISTRIES ===
    mcp_tools: List[str] = field(default_factory=list)
    memory_type: str = "session"
    knowledge_bases: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    
    # === EMPLOYEE ASSISTANT ===
    employee_email: Optional[str] = None
    it_admin_defaults: dict = field(default_factory=dict)
    employee_overrides: dict = field(default_factory=dict)
    
    # === RUNTIME ===
    orchestrator: str = "langgraph"
    llm: Optional[str] = None


def get_capabilities(model: str) -> List[str]:
    """Get capabilities for model from AI provider."""
    return ai_provider.get_capabilities(model)


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
