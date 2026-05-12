"""
A2A (Agent-to-Agent) SDK

Python SDK for agent-to-agent communication.

Reference:
- https://github.com/AGenNext/a2a-protocol
- Google A2A Protocol: https://a2a-protocol.ai/

Features:
- Agent discovery
- Task delegation
- Message passing
- State sync
- Streaming responses
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum
import uuid
import json
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor


# =============================================================================
# A2A TYPES
# =============================================================================

class AgentState(Enum):
    """Agent state"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class TaskStatus(Enum):
    """Task status"""
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MessageRole(Enum):
    """Message role"""
    AGENT = "agent"
    USER = "user"
    SYSTEM = "system"


@dataclass
class AgentCapability:
    """Agent capability"""
    name: str
    description: str
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentInfo:
    """Agent information"""
    agent_id: str
    name: str
    description: str
    
    # Capabilities
    capabilities: List[AgentCapability] = field(default_factory=list)
    
    # State
    state: AgentState = AgentState.IDLE
    
    # Metadata
    version: str = "1.0"
    skills: List[str] = field(default_factory=list)


@dataclass
class Message:
    """A2A message"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    role: MessageRole = MessageRole.AGENT
    
    # Content
    content: str = ""
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Reply to
    reply_to: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "messageId": self.message_id,
            "role": self.role.value,
            "content": self.content,
            "attachments": self.attachments,
            "timestamp": self.timestamp,
            "replyTo": self.reply_to
        }


@dataclass
class Task:
    """A2A task"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    
    # Status
    status: TaskStatus = TaskStatus.SUBMITTED
    status_message: str = ""
    
    # Messages
    messages: List[Message] = field(default_factory=list)
    
    # Artifacts (results)
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Additional data
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_message(self, message: Message) -> None:
        """Add message to task"""
        self.messages.append(message)
        self.updated_at = datetime.utcnow().isoformat()
    
    def add_artifact(self, artifact: Dict[str, Any]) -> None:
        """Add artifact to task"""
        self.artifacts.append(artifact)
        self.updated_at = datetime.utcnow().isoformat()


# =============================================================================
# A2A CLIENT
# =============================================================================

@dataclass
class A2ASDK:
    """A2A Python SDK"""
    
    agent_id: str = ""
    agent_name: str = ""
    agent_description: str = ""
    
    # Server URL
    server_url: str = "http://localhost:10000"
    
    # Local agent
    local_agent: Optional[AgentInfo] = None
    
    # Message handlers
    message_handlers: Dict[str, Callable] = field(default_factory=dict)
    
    # Task handlers
    task_handlers: Dict[str, Callable] = field(default_factory=dict)
    
    # Registered agents
    registered_agents: Dict[str, AgentInfo] = field(default_factory=dict)
    
    # Active tasks
    active_tasks: Dict[str, Task] = field(default_factory=dict)
    
    # Message queue
    message_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    
    # =================================================================
    # AGENT REGISTRATION
    # =================================================================
    
    def register_agent(
        self,
        agent_id: str,
        name: str,
        description: str,
        capabilities: List[AgentCapability] = None,
        skills: List[str] = None
    ) -> AgentInfo:
        """Register this agent"""
        
        self.local_agent = AgentInfo(
            agent_id=agent_id,
            name=name,
            description=description,
            capabilities=capabilities or [],
            skills=skills or []
        )
        
        self.agent_id = agent_id
        self.agent_name = name
        self.agent_description = description
        
        return self.local_agent
    
    def register_remote_agent(
        self,
        agent_id: str,
        name: str,
        description: str,
        capabilities: List[AgentCapability] = None,
        server_url: str = None
    ) -> AgentInfo:
        """Register a remote agent"""
        
        agent_info = AgentInfo(
            agent_id=agent_id,
            name=name,
            description=description,
            capabilities=capabilities or []
        )
        
        self.registered_agents[agent_id] = agent_info
        
        return agent_info
    
    def discover_agents(self, filter_skills: List[str] = None) -> List[AgentInfo]:
        """Discover available agents"""
        
        agents = list(self.registered_agents.values())
        
        if filter_skills:
            agents = [
                a for a in agents
                if any(s in a.skills for s in filter_skills)
            ]
        
        return agents
    
    # =================================================================
    # TASK OPERATIONS
    # =================================================================
    
    def create_task(
        self,
        agent_id: str,
        message: str,
        metadata: Dict[str, Any] = None
    ) -> Task:
        """Create a new task"""
        
        task = Task(
            agent_id=agent_id,
            status=TaskStatus.SUBMITTED
        )
        
        # Add initial message
        task.add_message(Message(
            role=MessageRole.USER,
            content=message
        ))
        
        if metadata:
            task.metadata = metadata
        
        # Store task
        self.active_tasks[task.task_id] = task
        
        return task
    
    def submit_task(self, task: Task) -> Task:
        """Submit task to agent"""
        
        # Update status
        task.status = TaskStatus.WORKING
        task.updated_at = datetime.utcnow().isoformat()
        
        # Look up handler
        handler = self.task_handlers.get(task.agent_id)
        if handler:
            # Execute handler
            result = handler(task)
            task.add_artifact({"result": result})
            task.status = TaskStatus.COMPLETED
        else:
            task.status = TaskStatus.FAILED
            task.status_message = "No handler registered"
        
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.active_tasks.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        task = self.active_tasks.get(task_id)
        if task and task.status == TaskStatus.WORKING:
            task.status = TaskStatus.CANCELLED
            return True
        return False
    
    # =================================================================
    # MESSAGE OPERATIONS
    # =================================================================
    
    def send_message(
        self,
        target_agent_id: str,
        content: str,
        attachments: List[Dict[str, Any]] = None
    ) -> Message:
        """Send message to agent"""
        
        message = Message(
            role=MessageRole.AGENT,
            content=content,
            attachments=attachments or []
        )
        
        # Look up handler
        handler = self.message_handlers.get(target_agent_id)
        if handler:
            response = handler(message)
            return response
        else:
            # Create error response
            return Message(
                role=MessageRole.AGENT,
                content=f"No handler for agent {target_agent_id}"
            )
    
    def broadcast_message(
        self,
        content: str,
        filter_skills: List[str] = None
    ) -> Dict[str, Message]:
        """Broadcast message to multiple agents"""
        
        responses = {}
        
        # Find agents
        agents = self.discover_agents(filter_skills)
        
        for agent in agents:
            responses[agent.agent_id] = self.send_message(
                agent.agent_id,
                content
            )
        
        return responses
    
    # =================================================================
    # EVENT HANDLERS
    # =================================================================
    
    def on_message(self, agent_id: str, handler: Callable) -> None:
        """Register message handler"""
        self.message_handlers[agent_id] = handler
    
    def on_task(self, agent_id: str, handler: Callable) -> None:
        """Register task handler"""
        self.task_handlers[agent_id] = handler
    
    def handle_message(self, message: Message) -> Message:
        """Handle incoming message"""
        
        # Look for reply
        if message.reply_to:
            task = self.active_tasks.get(message.reply_to)
            if task:
                task.add_message(message)
                return message
        
        return Message(
            role=MessageRole.AGENT,
            content="Message received"
        )
    
    # =================================================================
    # STATE SYNC
    # =================================================================
    
    def get_agent_state(self, agent_id: str) -> AgentState:
        """Get agent state"""
        
        if agent_id == self.agent_id:
            return self.local_agent.state if self.local_agent else AgentState.OFFLINE
        
        agent = self.registered_agents.get(agent_id)
        return agent.state if agent else AgentState.OFFLINE
    
    def update_agent_state(self, state: AgentState) -> None:
        """Update local agent state"""
        
        if self.local_agent:
            self.local_agent.state = state
    
    def sync_states(self) -> Dict[str, AgentState]:
        """Sync all agent states"""
        
        return {
            aid: agent.state
            for aid, agent in self.registered_agents.items()
        }
    
    # =================================================================
    # STREAMING
    # =================================================================
    
    async def stream_message(
        self,
        target_agent_id: str,
        content: str
    ) -> asyncio.Queue:
        """Stream message to agent"""
        
        queue = asyncio.Queue()
        
        async def stream():
            message = Message(content=content)
            await queue.put(message)
            
            # Process in chunks
            words = content.split()
            for i, word in enumerate(words):
                await asyncio.sleep(0.1)
                await queue.put({"chunk": word, "index": i})
            
            await queue.put({"done": True})
        
        asyncio.create_task(stream())
        return queue
    
    # =================================================================
    # HELPERS
    # =================================================================
    
    def to_json(self, obj: Any) -> str:
        """Serialize to JSON"""
        return json.dumps(obj, default=lambda x: x.__dict__)
    
    def from_json(self, data: str) -> Any:
        """Deserialize from JSON"""
        return json.loads(data)


# =============================================================================
# A2A PROTOCOL MESSAGES
# =============================================================================

_AGENT_CARD_JSON = '''
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 1
}
'''

_TASK_SUBMIT_JSON = '''
{
  "jsonrpc": "2.0",
  "method": "tasks/send",
  "params": {
    "id": "task-id",
    "message": {
      "role": "user",
      "parts": [{"type": "text", "text": "message"}]
    }
  },
  "id": 1
}
'''


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example():
    """Example usage"""
    
    # Create SDK
    sdk = A2ASDK(
        agent_id="agent-001",
        agent_name="CodingAgent",
        agent_description="AI coding agent",
        server_url="http://localhost:10000"
    )
    
    # Register local agent
    sdk.register_agent(
        agent_id="agent-001",
        name="CodingAgent",
        description="AI coding agent",
        skills=["python", "javascript"]
    )
    
    # Register remote agent
    sdk.register_agent(
        agent_id="agent-002",
        name="DataAgent",
        description="Data processing agent",
        server_url="http://localhost:10001"
    )
    
    # Discover agents
    agents = sdk.discover_agents()
    print(f"Found {len(agents)} agents")
    
    # Create task
    task = sdk.create_task(
        agent_id="agent-002",
        message="Process this data"
    )
    print(f"Created task: {task.task_id}")
    
    # Send message
    response = sdk.send_message(
        target_agent_id="agent-002",
        content="Hello"
    )
    print(f"Response: {response.content}")


if __name__ == "__main__":
    example()