"""
Enterprise Agent Config - Simplified.

Key fields only:
- Identity (from SSO)
- Owner/Sponsor (governance)
- Secret ref (points to secret manager)
- Business scope (projects, products, groups)
- Runtime (orchestrator, LLM)
"""

from enum import Enum
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime


class AgentRole(Enum):
    PROJECT_DRIVER = "project_driver"
    PRODUCT_LEAD = "product_lead"
    GROUP_ADMIN = "group_admin"
    TEAM_LEAD = "team_lead"
    EMPLOYEE_ASSISTANT = "assistant"


class AgentStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"
    DEPROVISIONED = "deprovisioned"


class DeprovisioningReason(Enum):
    DISABLED = "disabled"
    TERMINATED = "terminated"
    SECURITY_CONCERN = "security_concern"
    IDLE = "idle"
    MANUAL = "manual"


@dataclass
class AgentConfig:
    """Enterprise agent config - simplified."""
    role: AgentRole
    
    # === IDENTITY (from SSO - just provide ID, system maps) ===
    identity_id: Optional[str] = None  # Provided by IdP
    identity_provider: Optional[str] = None  # entra/okta/google
    
    # === SECRET REF (points to secret manager) ===
    secret_ref: Optional[str] = None  # In secret manager
    
    # === GOVERNANCE (mandatory) ===
    owner: str  # Required
    sponsor: str  # Required
    
    # === SCOPE (business) ===
    reports_to: Optional[str] = None
    priority: int = 1
    projects: List[str] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    
    # === LIFECYCLE ===
    status: AgentStatus = AgentStatus.ACTIVE
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    deprovisioned_at: Optional[datetime] = None
    deprovisioning_reason: Optional[DeprovisioningReason] = None
    
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
