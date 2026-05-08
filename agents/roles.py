"""
Enterprise Agent Roles - Microsoft Entra Agent ID aligned.

Includes:
- Identity: object_id, UPN, displayName
- Credentials & scopes  
- Lifecycle management
- Owner & Sponsor governance
"""

from enum import Enum
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime


class AgentRole(Enum):
    """Enterprise agent roles."""
    PROJECT_DRIVER = "project_driver"
    PRODUCT_LEAD = "product_lead"
    GROUP_ADMIN = "group_admin"
    TEAM_LEAD = "team_lead"
    EMPLOYEE_ASSISTANT = "assistant"


class AgentStatus(Enum):
    """Agent lifecycle status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"
    DEPROVISIONED = "deprovisioned"


class DeprovisioningReason(Enum):
    """Why agent was disabled."""
    DISABLED = "disabled"
    TERMINATED = "terminated"
    SECURITY_CONCERN = "security_concern"
    IDLE = "idle"
    MANUAL = "manual"


@dataclass
class AgentConfig:
    """
    Enterprise agent config - Entra Agent ID aligned.
    """
    role: AgentRole
    
    # === IDENTITY ===
    object_id: Optional[str] = None
    user_principal_name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    
    # === CREDENTIALS ===
    credentials: List[dict] = field(default_factory=list)
    identifier_uris: List[str] = field(default_factory=list)
    scopes: List[str] = field(default_factory=list)
    app_roles: List[str] = field(default_factory=list)
    
    # === GOVERNANCE ===
    owner: str
    sponsor: str
    reports_to: Optional[str] = None
    priority: int = 1
    
    # === LIFECYCLE MANAGEMENT ===
    status: AgentStatus = AgentStatus.ACTIVE
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    
    # Deprovisioning
    deprovisioned_at: Optional[datetime] = None
    deprovisioning_reason: Optional[DeprovisioningReason] = None
    disable_reason: Optional[str] = None
    
    # Expiration
    expires_at: Optional[datetime] = None
    renewal_required: bool = True
    
    # === SCOPE ===
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
