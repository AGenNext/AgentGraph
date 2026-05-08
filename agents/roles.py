"""
Enterprise Agent Roles.

Each enterprise agent has:
- Owner: Accountable for agent outcomes
- Sponsor: Budget/strategy approval
- IT Admin: Config defaults (for Employee Assistant)
- Employee: Can override (for Assistant)
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
class AgentRoleConfig:
    """Enterprise agent configuration with governance."""
    role: AgentRole
    
    # Governance - who owns/approves
    owner: Optional[str] = None      # Accountable for outcomes
    sponsor: Optional[str] = None     # Budget/strategy approval
    reports_to: Optional[str] = None # Reporting chain
    priority: int = 1
    
    # Scope
    projects: List[str] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    engages_with: List[str] = field(default_factory=list)
    manages: List[str] = field(default_factory=list)
    
    # Employee Assistant specifics
    employee_email: Optional[str] = None
    it_admin_defaults: dict = field(default_factory=dict)
    employee_overrides: dict = field(default_factory=dict)
    
    # Runtime
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
