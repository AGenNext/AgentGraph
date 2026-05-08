"""
Enterprise Agent Config - Tools, Capabilities, Integrations, Memory, Knowledge.

All external references - we just define what exists.
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


@dataclass
class AgentConfig:
    """Enterprise agent config - minimal core, external refs."""
    role: AgentRole
    
    # === IDENTITY (from IdP) ===
    identity_id: str
    identity_provider: str  # entra/okta/google
    
    # === SECRET (from secret manager) ===
    secret_ref: str
    
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
    
    # === TOOLS & CAPABILITIES (from platforms) ===
    integrations: List[str] = field(default_factory=list)  # API connectors
    capabilities: List[str] = field(default_factory=list)  # LLM features
    
    # === COMMUNICATIONS (from comms platform) ===
    comms_refs: List[str] = field(default_factory=list)  # slack/teams/email
    
    # === MEMORY (from memory platform) ===
    memory_refs: List[str] = field(default_factory=list)  # redis/vector-db
    
    # === KNOWLEDGE BASES (from RAG platform) ===
    knowledge_refs: List[str] = field(default_factory=list)  # pinecone/qdrant/mongo
    
    # === EMPLOYEE ASSISTANT ===
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
