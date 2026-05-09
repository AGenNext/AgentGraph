"""A2A Protocol package."""

from .messages import (
    Task,
    TaskStatus,
    Message,
    MessageRole,
    AgentResult,
    AgentCard,
    AgentCapability,
    AgentSkill,
)
from .protocol import A2AProtocol
from .card import (
    get_agent_card,
    get_all_agent_cards,
    AGENT_CARDS,
)
from .client import A2AClient

__all__ = [
    "Task",
    "TaskStatus", 
    "Message",
    "MessageRole",
    "AgentResult",
    "AgentCard",
    "AgentCapability",
    "AgentSkill",
    "A2AProtocol",
    "get_agent_card",
    "get_all_agent_cards",
    "AGENT_CARDS",
    "A2AClient",
]