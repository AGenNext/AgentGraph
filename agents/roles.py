"""
Enterprise Agent Roles.

Each role has preferred orchestrator and LLM - configurable.
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
    """Config for agent role - all fields configurable."""
    role: AgentRole
    
    # Reporting
    reports_to: Optional[str] = None
    priority: int = 1
    
    # Ownership / Scope
    projects: List[str] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    engages_with: List[str] = field(default_factory=list)
    manages: List[str] = field(default_factory=list)
    
    # Runtime - configurable (defaults provided)
    orchestrator: str = "langgraph"  # Can override: set via config
    llm: Optional[str] = None       # Can override: set via config


# Default orchestrator and LLM per role
ROLE_DEFAULTS = {
    AgentRole.PROJECT_DRIVER: {
        "orchestrator": "langgraph",
        "llm": "gpt-4o",
    },
    AgentRole.PRODUCT_LEAD: {
        "orchestrator": "langgraph", 
        "llm": "gpt-4o",
    },
    AgentRole.GROUP_ADMIN: {
        "orchestrator": "langgraph",
        "llm": "gemini-2.0-flash",
    },
    AgentRole.TEAM_LEAD: {
        "orchestrator": "langgraph",
        "llm": "gpt-4",
    },
    AgentRole.EMPLOYEE_ASSISTANT: {
        "orchestrator": "langgraph",
        "llm": "gemini-2.0-flash",
    },
}


ROLE_BEHAVIORS = {
    AgentRole.PROJECT_DRIVER: {"behavior": "drives", "delegates": True, "approves": True},
    AgentRole.PRODUCT_LEAD: {"behavior": "owns", "delegates": True, "approves": True},
    AgentRole.GROUP_ADMIN: {"behavior": "collaborates", "facilitates": True, "engages": True},
    AgentRole.TEAM_LEAD: {"behavior": "leads", "manages": True, "coaches": True},
    AgentRole.EMPLOYEE_ASSISTANT: {"behavior": "assists", "supports": True},
}
