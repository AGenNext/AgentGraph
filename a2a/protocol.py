"""A2A Protocol for agent-to-agent communication."""

import json
import uuid
from typing import Any, Optional, Callable, AsyncIterator
from datetime import datetime

from .messages import (
    Task,
    TaskStatus,
    Message,
    MessageRole,
    JSONRPCRequest,
    JSONRPCResponse,
    AgentDelegateRequest,
    AgentResult,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
)


class A2AProtocol:
    """A2A Protocol handler for JSON-RPC 2.0 based agent communication."""
    
    def __init__(self, agent_id: str, agent_url: str):
        self.agent_id = agent_id
        self.agent_url = agent_url
        self._tasks: dict[str, Task] = {}
    
    def create_task(self, session_id: Optional[str] = None) -> Task:
        """Create a new A2A task."""
        task = Task(
            id=str(uuid.uuid4()),
            sessionId=session_id,
            status=TaskStatus.SUBMITTED,
        )
        self._tasks[task.id] = task
        return task
    
    def add_message(
        self, 
        task_id: str, 
        content: str, 
        role: MessageRole = MessageRole.USER
    ) -> Message:
        """Add a message to task history."""
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        message = Message(
            messageId=str(uuid.uuid4()),
            role=role,
            content=content,
        )
        task.history.append(message)
        return message
    
    def update_status(self, task_id: str, status: TaskStatus) -> None:
        """Update task status."""
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        task.status = status
    
    def build_request(
        self,
        method: str,
        params: dict[str, Any],
        request_id: Optional[str] = None
    ) -> JSONRPCRequest:
        """Build a JSON-RPC request."""
        return JSONRPCRequest(
            id=request_id or str(uuid.uuid4()),
            method=method,
            params=params,
        )
    
    def build_response(
        self,
        request_id: str,
        result: Any
    ) -> JSONRPCResponse:
        """Build a JSON-RPC response."""
        return JSONRPCResponse(
            id=request_id,
            result=result,
        )
    
    def build_error_response(
        self,
        request_id: str,
        code: int,
        message: str,
        data: Optional[Any] = None
    ) -> JSONRPCResponse:
        """Build a JSON-RPC error response."""
        error = {
            "code": code,
            "message": message,
        }
        if data:
            error["data"] = data
        return JSONRPCResponse(
            id=request_id,
            error=error,
        )
    
    def serialize(self, obj: Any) -> str:
        """Serialize object to JSON."""
        # Handle Pydantic models
        if hasattr(obj, 'model_dump'):
            return json.dumps(obj.model_dump(exclude_none=True), default=str)
        if hasattr(obj, 'dict'):
            return json.dumps(obj.dict(), default=str)
        return json.dumps(obj, default=str)
    
    def deserialize(self, data: str, type_: type) -> Any:
        """Deserialize JSON to object."""
        parsed = json.loads(data)
        if isinstance(parsed, dict):
            return type_(**parsed)
        return parsed
    
    # Task delegation methods
    def create_delegate_request(
        self,
        source_agent: str,
        target_agent: str,
        capability: str,
        context: dict[str, Any],
    ) -> AgentDelegateRequest:
        """Create a delegate request for A2A communication."""
        return AgentDelegateRequest(
            task_id=str(uuid.uuid4()),
            source_agent=source_agent,
            target_agent=target_agent,
            capability=capability,
            context=context,
        )
    
    def create_result(
        self,
        agent_id: str,
        capability: str,
        content: str,
        quality_score: float = 0.0,
        metadata: Optional[dict[str, Any]] = None,
    ) -> AgentResult:
        """Create an agent result."""
        return AgentResult(
            agent_id=agent_id,
            capability=capability,
            content=content,
            quality_score=quality_score,
            metadata=metadata or {},
        )
    
    # Streaming support
    async def stream_task_updates(
        self,
        task_id: str,
    ) -> AsyncIterator[TaskStatusUpdateEvent]:
        """Stream task status updates."""
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Emit current status
        yield TaskStatusUpdateEvent(
            id=task.id,
            status=task.status,
            metadata=task.metadata,
        )
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)
    
    def list_tasks(self, status: Optional[TaskStatus] = None) -> list[Task]:
        """List tasks, optionally filtered by status."""
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return tasks