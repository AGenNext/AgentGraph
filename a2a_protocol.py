"""
Agent-to-Agent (A2A) Communication

Protocol for agents communicating with each other:
- Agent Card (discovery)
- Agent Tasks (async)
- Message formats
- Protocol handling

Reference:
- Anthropic A2A Protocol: https://docs.anthropic.com/en/docs/agent-model
- Agent Communication Protocol
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum
import json
import secrets


# =============================================================================
# AGENT CARD
# =============================================================================

class AgentStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"


@dataclass
class AgentCard:
    """Agent discovery card"""
    id: str
    
    name: str
    
    description: str = ""
    
    url: str = ""
    
    version: str = "1.0.0"
    
    status: AgentStatus = AgentStatus.ONLINE
    
    capabilities: List[str] = field(default_factory=list)
    
    skills: List[str] = field(default_factory=list)
    
    tools: List[str] = field(default_factory=list)
    
    language: str = "en"
    
    auth: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "version": self.version,
            "status": self.status.value,
            "capabilities": self.capabilities,
            "skills": self.skills,
            "tools": self.tools,
            "language": self.language
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> AgentCard:
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            url=data.get("url", ""),
            status=AgentStatus(data.get("status", "online"))
        )


# =============================================================================
# AGENT TASKS
# =============================================================================

class TaskStatus(Enum):
    SUBMITTED = "submitted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentTask:
    """Agent task"""
    id: str
    
    agent_id: str
    
    status: TaskStatus = TaskStatus.SUBMITTED
    
    message: Dict = field(default_factory=dict)
    
    result: Any = None
    
    error: Optional[str] = None
    
    created_at: datetime = field(default_factory=datetime.now)
    
    completed_at: Optional[datetime] = None
    
    artifacts: Dict[str, Any] = field(default_factory=dict)
    
    history: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "status": self.status.value,
            "message": self.message,
            "result": self.result,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


# =============================================================================
# MESSAGES
# =============================================================================

@dataclass
class Message:
    """A2A Message"""
    id: str
    
    type: str = "message"  # message, task, task_result
    
    role: str = "user"  # user, agent
    
    content: str = ""
    
    parts: List[Dict] = field(default_factory=list)
    
    model: str = "gpt-4"
    
    temperature: float = 0.7
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "role": self.role,
            "content": self.content,
            "parts": self.parts,
            "model": self.model,
            "temperature": self.temperature
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> Message:
        return cls(
            id=data.get("id", secrets.token_urlsafe(16)),
            type=data.get("type", "message"),
            role=data.get("role", "user"),
            content=data.get("content", ""),
            parts=data.get("parts", []),
            model=data.get("model", "gpt-4"),
            temperature=data.get("temperature", 0.7)
        )


# =============================================================================
# A2A CLIENT
# =============================================================================

class A2AClient:
    """A2A Client for communicating with agents"""
    
    def __init__(self):
        self.agent_cards: Dict[str, AgentCard] = {}
        
        self.tasks: Dict[str, AgentTask] = {}
        
        self.message_handlers: Dict[str, Callable] = {}
    
    # Discovery
    def register_agent(self, card: AgentCard):
        """Register agent card"""
        self.agent_cards[card.id] = card
    
    def discover_agents(self, capabilities: List[str] = None) -> List[AgentCard]:
        """Discover agents"""
        agents = list(self.agent_cards.values())
        
        if capabilities:
            agents = [
                a for a in agents
                if any(cap in a.capabilities for cap in capabilities)
            ]
        
        return [a for a in agents if a.status == AgentStatus.ONLINE]
    
    def get_agent_card(self, agent_id: str) -> Optional[AgentCard]:
        """Get agent card"""
        return self.agent_cards.get(agent_id)
    
    # Tasks
    def submit_task(
        self,
        agent_id: str,
        message: str,
        context: Dict = None
    ) -> AgentTask:
        """Submit task to agent"""
        task = AgentTask(
            id=secrets.token_urlsafe(16),
            agent_id=agent_id,
            message={
                "content": message,
                "context": context or {}
            }
        )
        
        self.tasks[task.id] = task
        
        return task
    
    def get_task(self, task_id: str) -> Optional[AgentTask]:
        """Get task"""
        return self.tasks.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel task"""
        task = self.tasks.get(task_id)
        if task and task.status in [TaskStatus.SUBMITTED, TaskStatus.IN_PROGRESS]:
            task.status = TaskStatus.FAILED
            task.error = "Cancelled"
            return True
        return False
    
    # Send message
    def send_message(
        self,
        agent_id: str,
        content: str,
        metadata: Dict = None
    ) -> Message:
        """Send message to agent"""
        msg = Message(
            id=secrets.token_urlsafe(16),
            content=content,
            metadata=metadata or {}
        )
        
        agent = self.agent_cards.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # Process message (simplified)
        response = self._process_message(agent, msg)
        
        return response
    
    def _process_message(self, agent: AgentCard, message: Message) -> Message:
        """Process message (simplified)"""
        response = Message(
            id=secrets.token_urlsafe(16),
            type="message",
            role="agent",
            content=f"Response from {agent.name}: {message.content}"
        )
        
        return response
    
    # Events
    def on_message(self, handler: Callable):
        """Register message handler"""
        self.message_handlers["message"] = handler
    
    def on_task(self, handler: Callable):
        """Register task handler"""
        self.message_handlers["task"] = handler


# =============================================================================
# A2A SERVER
# =============================================================================

class A2AServer:
    """A2A Server for hosting agents"""
    
    def __init__(self, agent_id: str, agent_name: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        
        self.card: AgentCard = None
        
        self.task_handlers: Dict[str, Callable] = {}
        
        self.message_handlers: Dict[str, Callable] = {}
        
        self.middleware: List[Callable] = []
    
    def set_card(self, card: AgentCard):
        """Set agent card"""
        self.card = card
    
    def register_task_handler(self, name: str, handler: Callable):
        """Register task handler"""
        self.task_handlers[name] = handler
    
    def register_message_handler(self, handler: Callable):
        """Register message handler"""
        self.message_handlers["default"] = handler
    
    def add_middleware(self, middleware: Callable):
        """Add middleware"""
        self.middleware.append(middleware)
    
    def handle_message(self, message: Dict) -> Dict:
        """Handle incoming message"""
        msg = Message.from_dict(message)
        
        # Apply middleware
        for mw in self.middleware:
            msg = mw(msg)
        
        # Process
        response = self._process_message(msg)
        
        return response.to_dict()
    
    def _process_message(self, message: Message) -> Message:
        """Process message"""
        for handler in self.message_handlers.values():
            result = handler(message)
            if result:
                return result
        
        # Default response
        return Message(
            id=secrets.token_urlsafe(16),
            type="message",
            role="agent",
            content="Message processed"
        )
    
    def handle_task(self, task: Dict) -> Dict:
        """Handle incoming task"""
        task_obj = AgentTask(
            id=task.get("id", secrets.token_urlsafe(16)),
            agent_id=self.agent_id,
            message=task.get("message", {})
        )
        
        task_obj.status = TaskStatus.IN_PROGRESS
        
        # Process
        task_obj.result = self._process_task(task_obj)
        
        task_obj.status = TaskStatus.COMPLETED
        
        return task_obj.to_dict()
    
    def _process_task(self, task: AgentTask) -> Any:
        """Process task"""
        for handler in self.task_handlers.values():
            result = handler(task)
            if result:
                return result
        
        return {"result": "Task completed"}
    
    def get_card_json(self) -> Dict:
        """Get card as JSON"""
        if not self.card:
            self.card = AgentCard(
                id=self.agent_id,
                name=self.agent_name
            )
        return self.card.to_dict()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Agent-to-Agent (A2A)")
    print("=" * 50)
    
    # Client
    print("\n1. A2A Client")
    client = A2AClient()
    
    # Register agents
    assistant = AgentCard(
        id="assistant",
        name="Assistant",
        description="Helpful assistant",
        capabilities=["search", "compute"],
        skills=["general", "coding"]
    )
    
    research = AgentCard(
        id="researcher",
        name="Researcher",
        description="Research agent",
        capabilities=["search", "analyze"],
        skills=["research", "data"]
    )
    
    client.register_agent(assistant)
    client.register_agent(research)
    
    print(f"   Registered: {len(client.agent_cards)} agents")
    
    # Discover
    agents = client.discover_agents(["search"])
    print(f"   Search agents: {len(agents)}")
    
    # Send message
    response = client.send_message("assistant", "Hello")
    print(f"   Response: {response.content[:30]}...")
    
    # Submit task
    task = client.submit_task("assistant", "Research AI")
    print(f"   Task: {task.id} ({task.status.value})")
    
    # Server
    print("\n2. A2A Server")
    server = A2AServer("assistant", "Assistant")
    
    @server.register_message_handler
    def handle_message(msg: Message) -> Message:
        return Message(
            id=secrets.token_urlsafe(16),
            role="agent",
            content=f"Echo: {msg.content}"
        )
    
    card = server.get_card_json()
    print(f"   Card: {card['name']}")
    
    # Handle message
    result = server.handle_message({
        "id": "msg-1",
        "content": "Test"
    })
    print(f"   Result: {result['content']}")


if __name__ == "__main__":
    main()


"""
A2A Usage

    # Client - Discover and communicate
    client = A2AClient()
    client.register_agent(AgentCard(...))
    
    agents = client.discover_agents(["search"])
    response = client.send_message(agent_id, "Hello")
    task = client.submit_task(agent_id, "Research AI")
    
    # Server - Host agent
    server = A2AServer("agent-id", "Agent Name")
    server.register_message_handler(lambda m: Message(...))
    
    card = server.get_card_json()
    result = server.handle_message({"content": "Hello"})
"""