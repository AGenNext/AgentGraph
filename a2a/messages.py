"""A2A Protocol Messages for multi-agent communication."""

from typing import Any, Literal, Optional
from pydantic import BaseModel, Field
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enum for A2A protocol."""
    
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class MessageRole(str, Enum):
    """Message role for A2A protocol."""
    
    USER = "user"
    AGENT = "agent"


# Agent Card Types
class AgentCapability(BaseModel):
    """Agent capability definition."""
    
    name: str
    description: str
    inputModes: list[str] = ["text"]
    outputModes: list[str] = ["text"]


class AgentSkill(BaseModel):
    """Agent skill definition."""
    
    id: str
    name: str
    description: str
    tags: list[str] = []


class AgentCard(BaseModel):
    """A2A Agent Card for capability discovery."""
    
    agentId: str
    name: str
    description: str
    url: str
    version: str = "1.0.0"
    capabilities: list[AgentCapability] = []
    skills: list[AgentSkill] = []
    supportsAuthenticatedExtensions: bool = False
    supportsStreaming: bool = True


# Message Types
class Message(BaseModel):
    """A2A Message for inter-agent communication."""
    
    role: MessageRole
    content: str
    messageId: Optional[str] = None
    metadata: dict[str, Any] = {}


class TaskPart(BaseModel):
    """Task part containing content."""
    
    type: Literal["message", "image", "audio", "video", "file"] = "message"
    text: Optional[str] = None
    metadata: dict[str, Any] = {}


class Task(BaseModel):
    """A2A Task for agent communication."""
    
    id: str
    status: TaskStatus = TaskStatus.SUBMITTED
    sessionId: Optional[str] = None
    history: list[Message] = []
    metadata: dict[str, Any] = {}


class TaskSubmitParams(BaseModel):
    """Parameters for task submission."""
    
    id: str
    message: Message
    sessionId: Optional[str] = None
    skillIds: list[str] = []


class TaskSubmitResult(BaseModel):
    """Result of task submission."""
    
    id: str
    status: TaskStatus
    result: Optional[str] = None
    metadata: dict[str, Any] = {}


# JSON-RPC Types
class JSONRPCRequest(BaseModel):
    """JSON-RPC 2.0 request."""
    
    jsonrpc: Literal["2.0"] = "2.0"
    id: Optional[str] = None
    method: str
    params: dict[str, Any] = {}


class JSONRPCResponse(BaseModel):
    """JSON-RPC 2.0 response."""
    
    jsonrpc: Literal["2.0"] = "2.0"
    id: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[dict[str, Any]] = None


# Stream Events
class TaskStatusUpdateEvent(BaseModel):
    """Task status update event."""
    
    id: str
    status: TaskStatus
    metadata: dict[str, Any] = {}


class TaskArtifactUpdateEvent(BaseModel):
    """Task artifact update event."""
    
    id: str
    artifacts: list[dict[str, Any]] = []


# Team Communication Types
class AgentDelegateRequest(BaseModel):
    """Request to delegate task to another agent."""
    
    task_id: str
    source_agent: str
    target_agent: str
    capability: str
    context: dict[str, Any] = {}


class AgentResult(BaseModel):
    """Result from an agent."""
    
    agent_id: str
    capability: str
    content: str
    quality_score: float = 0.0
    metadata: dict[str, Any] = {}