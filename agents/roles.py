"""
Enterprise Agent Roles.

Five enterprise roles:
- Project Driver: Drives multiple projects & products
- Product Lead: Owns product direction  
- Group Admin: Drives collaboration across groups
- Team Lead: Leads team members
- Employee Assistant: Supports employees
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
    role: AgentRole
    reports_to: Optional[str] = None
    priority: int = 1
    projects: List[str] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    engages_with: List[str] = field(default_factory=list)
    manages: List[str] = field(default_factory=list)


ROLE_BEHAVIORS = {
    AgentRole.PROJECT_DRIVER: {
        "behavior": "drives", 
        "delegates": True, 
        "approves": True,
        "multi": True,  # Drives multiple
    },
    AgentRole.PRODUCT_LEAD: {"behavior": "owns", "delegates": True, "approves": True},
    AgentRole.GROUP_ADMIN: {"behavior": "collaborates", "facilitates": True, "engages": True},
    AgentRole.TEAM_LEAD: {"behavior": "leads", "manages": True, "coaches": True},
    AgentRole.EMPLOYEE_ASSISTANT: {"behavior": "assists", "supports": True},
}
