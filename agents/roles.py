"""
Enterprise Agent Roles.

Four enterprise roles:
- Project Driver: Leads projects
- Product Lead: Owns product
- Group Admin: Drives collaboration
- Team Lead: Leads team members
- Employee Assistant: Supports employees
"""

from enum import Enum
from typing import Optional
from dataclasses import dataclass, field


class AgentRole(Enum):
    PROJECT_DRIVER = "project_driver"
    PRODUCT_LEAD = "product_lead"
    GROUP_ADMIN = "group_admin"
    TEAM_LEAD = "team_lead"
    EMPLOYEE_ASSISTANT = "assistant"


@dataclass
class AgentRoleConfig:
    role: AgentRole
    reports_to: Optional[str] = None
    team_size: int = 0
    priority: int = 1
    owns: list[str] = field(default_factory=list)
    engages_with: list[str] = field(default_factory=list)
    manages: list[str] = field(default_factory=list)


ROLE_BEHAVIORS = {
    AgentRole.PROJECT_DRIVER: {"behavior": "drives", "delegates": True, "approves": True},
    AgentRole.PRODUCT_LEAD: {"behavior": "owns", "delegates": True, "approves": True},
    AgentRole.GROUP_ADMIN: {"behavior": "collaborates", "facilitates": True, "engages": True},
    AgentRole.TEAM_LEAD: {"behavior": "leads", "manages": True, "coaches": True},
    AgentRole.EMPLOYEE_ASSISTANT: {"behavior": "assists", "supports": True},
}
