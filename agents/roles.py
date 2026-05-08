"""
Enterprise Agent - IAM/IGA Role references.

Roles point to IAM/IGA systems - not hardcoded values.
Just like credentials point to secret manager.
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
    """Enterprise agent - role refs from IAM/IGA."""
    role: AgentRole
    
    # === IDENTITY (from SSO/IdP) ===
    identity_id: Optional[str] = None
    identity_provider: Optional[str] = None
    principal_name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    
    # === SECRET MANAGER ===
    secret_manager: Optional[str] = None  # aws-secrets/vault/azure-keyvault
    secret_refs: List[str] = field(default_factory=list)
    credential_rotation: str = "auto"
    credential_expires_at: Optional[datetime] = None
    
    # === OAUTH SCOPES ===
    oauth_scopes: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    
    # === IAM ROLES (reference from IdP) ===
    iam_system: Optional[str] = None  # entra/okta/google
    iam_role_refs: List[str] = field(default_factory=list)  # Role refs
    iam_group_refs: List[str] = field(default_factory=list)  # Group refs
    
    # === IGA ROLES (reference from IGA) ===
    iga_system: Optional[str] = None  # saviynt/sailpoint/sap-iga
    iga_role_refs: List[str] = field(default_factory=list)  # Role refs
    iga_entitlement_refs: List[str] = field(default_factory=list)  # Entitlement refs
    access_certified: bool = False
    access_certified_by: Optional[str] = None
    access_certified_at: Optional[datetime] = None
    
    # === GOVERNANCE ===
    owner: str
    sponsor: str
    reports_to: Optional[str] = None
    priority: int = 1
    
    # === LIFECYCLE ===
    status: AgentStatus = AgentStatus.ACTIVE
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    
    deprovisioned_at: Optional[datetime] = None
    deprovisioning_reason: Optional[DeprovisioningReason] = None
    disable_reason: Optional[str] = None
    
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
