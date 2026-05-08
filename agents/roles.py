"""
Enterprise Agent Roles.

Agents can have different enterprise roles:
- Project Driver: Leads and drives projects to completion
- Product Lead: Owns product direction and roadmap
- Employee Assistant: Supports employees with tasks
"""


from enum import Enum
from typing import Optional
from dataclasses import dataclass


class AgentRole(Enum):
    """Enterprise agent roles."""
    PROJECT_DRIVER = "project_driver"  # Drives projects
    PRODUCT_LEAD = "product_lead"     # Owns product
    EMPLOYEE_ASSISTANT = "assistant"   # Supports employees


@dataclass
class AgentRoleConfig:
    """Configuration for agent role."""
    role: AgentRole
    reports_to: Optional[str] = None    # Agent ID this reports to
    team_size: int = 0                 # Team members
    priority: int = 1                 # Priority level
    owns: list[str] = None             # Owned projects/products


# Role-based behavior
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
}
