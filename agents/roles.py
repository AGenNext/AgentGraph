"""
Enterprise Agent Config - Minimal.

Lifecycle managed by IAM/IGA tools, not here.
We just need identity + governance + runtime.
"""

from enum import Enum
from typing import Optional, List
from dataclasses import dataclass, field


class AgentRole(Enum):
    """Functional roles for agents."""
    PROJECT_DRIVER = "project_driver"
    PRODUCT_LEAD = "product_lead"
    GROUP_ADMIN = "group_admin"
    TEAM_LEAD = "team_lead"
    EMPLOYEE_ASSISTANT = "assistant"


@dataclass
class AgentConfig:
    """
    Minimal agent config.
    
    Lifecycle managed by IAM/IGA tools externally.
    """
    role: AgentRole
    
    # === IDENTITY (from SSO) ===
    identity_id: str  # From identity provider
    identity_provider: str  # entra/okta/google/cognito
    
    # === SECRET (from secret manager) ===
    secret_ref: str  # In vault/aws-secrets/azure-keyvault
    
    # === GOVERNANCE (required) ===
    owner: str  # Accountable for agent
    sponsor: str  # Budget/strategy
    
    # === SCOPE ===
    reports_to: Optional[str] = None
    projects: List[str] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    engages_with: List[str] = field(default_factory=list)
    manages: List[str] = field(default_factory=list)
    
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
