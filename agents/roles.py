"""
Enterprise Agent - Complete AI Provider Capabilities.

All capabilities based on model from AI provider.
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


class AIProvider:
    """AI Provider - all capabilities by model."""
    
    # COMPLETE MODEL CAPABILITIES
    MODEL_CAPABILITIES = {
        # === OPENAI ===
        "gpt-4o": [
            "vision", "function-calling", "json", "streaming", 
            "text-to-speech", "dall-e-3", "realtime", 
            "fine-tuning", "batch"
        ],
        "gpt-4o-mini": [
            "function-calling", "json", "streaming",
            "batch", "fine-tuning"
        ],
        "o1": [
            "reasoning", "chain-of-thought", "math", "code-generation",
            "step-by-step"
        ],
        "o3-mini": [
            "reasoning", "chain-of-thought", "math",
            "code-generation", "fast"
        ],
        
        # === ANTHROPIC ===
        "claude-3-5-sonnet": [
            "vision", "function-calling", "json", "streaming",
            "thinking", "text-to-speech", "computer-use"
        ],
        "claude-3-opus": [
            "vision", "function-calling", "json",
            "streaming", "thinking", "computer-use"
        ],
        "claude-3-haiku": [
            "function-calling", "json", "streaming",
            "fast"
        ],
        
        # === GOOGLE ===
        "gemini-2.0-flash": [
            "vision", "function-calling", "json", "streaming",
            "text-to-speech", "image-generation", "native-tools"
        ],
        "gemini-2.5-pro": [
            "vision", "function-calling", "json", "streaming",
            "thinking", "long-context", "code-execution"
        ],
        "gemini-1.5-flash": [
            "vision", "function-calling", "json", "streaming"
        ],
        
        # === AZURE OPENAI ===
        "azure-gpt-4o": [
            "vision", "function-calling", "json"
        ],
        "azure-gpt-4o-mini": [
            "function-calling", "json", "fast"
        ],
        
        # === AWS BEDROCK ===
        "bedrock-claude": [
            "vision", "function-calling", "json", "thinking"
        ],
        "bedrock-llama": [
            "function-calling", "json"
        ],
        "bedrock-titan": [
            "function-calling", "json"
        ],
        
        # === GROQ ===
        "groq-llama-3-70b": [
            "function-calling", "streaming", "fast"
        ],
        "groq-mixtral": [
            "function-calling", "streaming", "fast"
        ],
        
        # === NVIDIA ===
        "nvidia-llama": [
            "function-calling", "json", "streaming"
        ],
        "nvidia-mixtral": [
            "function-calling", "streaming", "fast"
        ],
        
        # === OPENROUTER ===
        "openrouter-gpt-4": [
            "vision", "function-calling", "json"
        ],
        "openrouter-claude": [
            "vision", "function-calling", "thinking"
        ],
    }
    
    def __init__(self):
        self._providers = {}
        self._models = {}
    
    def register(self, provider_name: str, api_key: str, base_url: str = None):
        self._providers[provider_name] = {"api_key": api_key, "base_url": base_url}
    
    def get_capabilities(self, model: str) -> List[str]:
        return self.MODEL_CAPABILITIES.get(model, [])
    
    def get_provider(self, model: str) -> Optional[str]:
        return self._models.get(model, {}).get("provider")


ai_provider = AIProvider()


# === REGISTRIES ===

class MCPRegistry:
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
    def __init__(self):
        self._sessions = {}
    def create_session(self, session_id: str):
        self._sessions[session_id] = {"id": session_id, "messages": []}


class RAGRegistry:
    def __init__(self):
        self._knowledge_bases = {}
    def register_kb(self, name: str, kb_config: dict):
        self._knowledge_bases[name] = kb_config


class ToolRegistry:
    def __init__(self):
        self._tools = {}
    def register(self, name: str, tool_fn, description: str = ""):
        self._tools[name] = {"fn": tool_fn, "description": description}


class SkillRegistry:
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
    
    # === AI PROVIDER ===
    ai_provider_name: str = "openai"
    provider_api_key: Optional[str] = None
    provider_base_url: Optional[str] = None
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
