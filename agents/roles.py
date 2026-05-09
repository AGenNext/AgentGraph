"""
Enterprise Agent - AI Provider with Multiple Auth Methods.

Each provider can use different auth methods.
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


class AuthMethod(Enum):
    """Authentication methods per provider."""
    # API Key based
    API_KEY = "api_key"
    OAUTH = "oauth"
    
    # AWS/IAM based
    IAM = "iam"
    AWS_CREDENTIALS = "aws_credentials"
    AWS_IAM_ROLE = "iam_role"
    
    # Azure
    AZURE_MI = "managed_identity"
    AZURE_AD = "azure_ad"
    
    # Google
    GCP_SERVICE_ACCOUNT = "gcp_service_account"
    
    # Enterprise
    ENTRA_APP_REGISTRATION = "entra_app"


class AIProvider:
    """AI Provider - multiple auth methods."""
    
    # Provider -> supported auth methods
    PROVIDER_AUTH = {
        "openai": ["api_key", "oauth"],
        "anthropic": ["api_key"],
        "google": ["api_key", "gcp_service_account"],
        "azure": ["api_key", "managed_identity", "azure_ad"],
        "bedrock": ["iam", "aws_credentials", "iam_role"],
        "groq": ["api_key"],
        "openrouter": ["api_key"],
        "nvidia": ["api_key", "nvidia_nim"],
    }
    
    # Model capabilities
    MODEL_CAPABILITIES = {
        "gpt-4o": ["vision", "function-calling", "json", "streaming", "text-to-speech", "dall-e-3"],
        "gpt-4o-mini": ["function-calling", "json", "streaming"],
        "o1": ["reasoning", "chain-of-thought", "math"],
        "claude-3-5-sonnet": ["vision", "function-calling", "json", "streaming", "thinking"],
        "gemini-2.0-flash": ["vision", "function-calling", "json", "streaming", "text-to-speech"],
        "gemini-2.5-pro": ["vision", "function-calling", "json", "streaming", "thinking"],
    }
    
    def __init__(self):
        self._providers = {}
        self._models = {}
    
    def register(self, provider_name: str, auth_method: str, auth_config: dict):
        """Register provider with auth config."""
        self._providers[provider_name] = {
            "auth_method": auth_method,
            "auth_config": auth_config,
        }
    
    def get_supported_auth(self, provider_name: str) -> List[str]:
        return self.PROVIDER_AUTH.get(provider_name, [])
    
    def get_capabilities(self, model: str) -> List[str]:
        return self.MODEL_CAPABILITIES.get(model, [])


ai_provider = AIProvider()


# === REGISTRIES ===

class MCPRegistry:
    def __init__(self):
        self._tools = {}
        self._resources = {}
        self._prompts = {}
    def register_tool(self, name, tool_fn):
        self._tools[name] = tool_fn
    def register_resource(self, uri, data):
        self._resources[uri] = data
    def register_prompt(self, name, prompt):
        self._prompts[name] = prompt


class MemorySystem:
    def __init__(self):
        self._sessions = {}
    def create_session(self, session_id):
        self._sessions[session_id] = {"id": session_id, "messages": []}


class RAGRegistry:
    def __init__(self):
        self._kb = {}
    def register_kb(self, name, kb_config):
        self._kb[name] = kb_config


class ToolRegistry:
    def __init__(self):
        self._tools = {}
    def register(self, name, tool_fn, description=""):
        self._tools[name] = {"fn": tool_fn, "description": description}


class SkillRegistry:
    def __init__(self):
        self._skills = {}
    def register(self, name, skill_config, role=None):
        self._skills[name] = skill_config


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
    
    # === AI PROVIDER (with auth) ===
    ai_provider_name: str = "openai"
    auth_method: str = "api_key"           # Which auth method
    provider_api_key: Optional[str] = None  # For api_key
    provider_base_url: Optional[str] = None
    
    # Azure/AWS specific
    subscription_id: Optional[str] = None
    resource_group: Optional[str] = None
    managed_identity: Optional[str] = None
    
    # AWS specific  
    aws_region: Optional[str] = None
    iam_role_arn: Optional[str] = None
    
    # Google specific
    gcp_project: Optional[str] = None
    gcp_location: Optional[str] = None
    
    # Model
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


def get_supported_auth(provider: str) -> List[str]:
    return ai_provider.get_supported_auth(provider)


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
