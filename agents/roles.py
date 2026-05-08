"""
Enterprise Agent Roles.

Agents can have different enterprise roles:
- Project Driver: Leads and drives projects
- Product Lead: Owns product direction
- Employee Assistant: Supports employees
- Group Admin: Drives work through collaboration
"""

from enum import Enum
from typing import Optional
from dataclasses import dataclass, field


class AgentRole(Enum):
    """Enterprise agent roles."""
    PROJECT_DRIVER = "project_driver"
    PRODUCT_LEAD = "product_lead"
    EMPLOYEE_ASSISTANT = "assistant"
    GROUP_ADMIN = "group_admin"


@dataclass
class AgentRoleConfig:
    """Configuration for agent role."""
    role: AgentRole
    reports_to: Optional[str] = None
    team_size: int = 0
    priority: int = 1
    owns: list[str] = field(default_factory=list)
    engages_with: list[str] = field(default_factory=list)


ROLE_BEHAVIORS = {
    AgentRole.PROJECT_DRIVER: {
        "behavior": "drives",
        "delegates": True,
        "approves": True,
    },
    AgentRole.PRODUCT_LEAD: {
        "behavior": "owns",
        "delegates": True,
        "approves": True,
    },
    AgentRole.EMPLOYEE_ASSISTANT: {
        "behavior": "assists",
        "delegates": False,
        "approves": False,
    },
    AgentRole.GROUP_ADMIN: {
        "behavior": "collaborates",
        "delegates": False,
        "approves": False,
        "engages": True,
        "facilitates": True,
    },
}
