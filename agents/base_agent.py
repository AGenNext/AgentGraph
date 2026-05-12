"""Base agent class with A2A support."""

from abc import ABC, abstractmethod
from typing import Any, Optional
from dataclasses import dataclass, field
import uuid

from a2a.messages import AgentResult, TaskStatus, Message
from a2a.protocol import A2AProtocol
from a2a.card import AgentCard


@dataclass
class ContentRequest:
    """Content generation request."""
    
    topic: str
    content_type: str
    style: str = "professional"
    length: str = "medium"
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class ContentResult:
    """Content generation result."""
    
    content: str
    agent_id: str
    quality_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Base class for multi-agent team members with A2A support."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        description: str,
        capabilities: list[str],
        skills: list[str],
        api_key: Optional[str] = None,
    ):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.skills = skills
        self.api_key = api_key
        
        # A2A protocol instance
        self.protocol = A2AProtocol(agent_id, f"http://localhost:{self._get_port()}")
    
    @abstractmethod
    def _get_port(self) -> int:
        """Get the port for this agent's server."""
        pass
    
    @abstractmethod
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        """Generate content - to be implemented by subclasses."""
        pass
    
    def get_agent_card(self) -> AgentCard:
        """Get the agent card for capability discovery."""
        from ..a2a.messages import AgentCapability, AgentSkill
        from ..a2a.card import AgentCard
        
        return AgentCard(
            agentId=self.agent_id,
            name=self.name,
            description=self.description,
            url=f"http://localhost:{self._get_port()}",
            version="1.0.0",
            capabilities=[
                AgentCapability(name=cap, description=f"Ability to {cap.replace('_', ' ')}")
                for cap in self.capabilities
            ],
            skills=[
                AgentSkill(id=skill, name=skill.replace("_", " ").title(), description=f"Skill in {skill}")
                for skill in self.skills
            ],
        )
    
    async def handle_request(self, request: ContentRequest) -> ContentResult:
        """Handle a content generation request."""
        # Create task
        task = self.protocol.create_task()
        
        # Update status to working
        self.protocol.update_status(task.id, TaskStatus.WORKING)
        
        # Generate content
        result = self._generate_content(request)
        
        # Update status to completed
        self.protocol.update_status(task.id, TaskStatus.COMPLETED)
        
        return result
    
    async def receive_delegated_task(
        self,
        capability: str,
        context: dict[str, Any],
    ) -> AgentResult:
        """Receive a delegated task from another agent."""
        if capability not in self.capabilities:
            raise ValueError(f"Capability {capability} not supported by {self.name}")
        
        # Create request from context
        content_request = ContentRequest(
            topic=context.get("topic", ""),
            content_type=context.get("content_type", "general"),
            style=context.get("style", "professional"),
            length=context.get("length", "medium"),
            context=context.get("context", {}),
        )
        
        # Generate content
        result = await self.handle_request(content_request)
        
        return AgentResult(
            agent_id=self.agent_id,
            capability=capability,
            content=result.content,
            quality_score=result.quality_score,
            metadata=result.metadata,
        )
    
    def can_handle(self, capability: str) -> bool:
        """Check if this agent can handle a capability."""
        return capability in self.capabilities
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.agent_id}, name={self.name})"