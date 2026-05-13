"""JSON-RPC runtime for the Agent2Agent protocol.

This module turns the local A2A protocol models into a usable in-process
runtime that can be exposed through FastAPI or reused directly by tests.
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable

from a2a.card import get_agent_card, get_all_agent_cards
from a2a.messages import JSONRPCRequest, JSONRPCResponse, Message, MessageRole, Task, TaskStatus
from a2a.protocol import A2AProtocol

TaskHandler = Callable[[Task, Message], Awaitable[str] | str]


class A2ARuntime:
    """Small JSON-RPC router for A2A methods."""

    def __init__(self, agent_id: str = "team-coordinator", agent_url: str = "http://localhost:8000") -> None:
        self.protocol = A2AProtocol(agent_id=agent_id, agent_url=agent_url)
        self._handler: TaskHandler | None = None

    def set_task_handler(self, handler: TaskHandler) -> None:
        """Register a callable used to process submitted messages."""
        self._handler = handler

    async def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Handle a JSON-RPC request payload and return a JSON-RPC response dict."""
        try:
            request = JSONRPCRequest(**payload)
        except Exception as exc:
            return JSONRPCResponse(id=None, error={"code": -32600, "message": "Invalid Request", "data": str(exc)}).model_dump(exclude_none=True)

        try:
            result = await self.dispatch(request.method, request.params)
            return JSONRPCResponse(id=request.id, result=result).model_dump(exclude_none=True)
        except KeyError as exc:
            return JSONRPCResponse(id=request.id, error={"code": -32601, "message": "Method not found", "data": str(exc)}).model_dump(exclude_none=True)
        except ValueError as exc:
            return JSONRPCResponse(id=request.id, error={"code": -32602, "message": "Invalid params", "data": str(exc)}).model_dump(exclude_none=True)
        except Exception as exc:
            return JSONRPCResponse(id=request.id, error={"code": -32000, "message": "Server error", "data": str(exc)}).model_dump(exclude_none=True)

    async def dispatch(self, method: str, params: dict[str, Any]) -> Any:
        """Dispatch supported A2A JSON-RPC methods."""
        if method == "agents/list":
            return [card.model_dump() for card in get_all_agent_cards()]
        if method == "agents/get":
            agent_id = params.get("agentId") or params.get("agent_id")
            if not agent_id:
                raise ValueError("agentId is required")
            card = get_agent_card(agent_id)
            if not card:
                raise ValueError(f"Agent {agent_id} not found")
            return card.model_dump()
        if method == "tasks/submit":
            return await self._submit_task(params)
        if method == "tasks/sendMessage":
            return await self._send_message(params)
        if method == "tasks/get":
            task_id = params.get("taskId") or params.get("task_id")
            if not task_id:
                raise ValueError("taskId is required")
            task = self.protocol.get_task(task_id)
            if not task:
                raise ValueError(f"Task {task_id} not found")
            return task.model_dump()
        if method == "tasks/list":
            status = params.get("status")
            tasks = self.protocol.list_tasks(TaskStatus(status)) if status else self.protocol.list_tasks()
            return [task.model_dump() for task in tasks]
        raise KeyError(method)

    async def _submit_task(self, params: dict[str, Any]) -> dict[str, Any]:
        message = self._parse_message(params.get("message"))
        task_id = params.get("taskId") or params.get("task_id")
        task = Task(id=task_id, sessionId=params.get("sessionId"), status=TaskStatus.SUBMITTED) if task_id else self.protocol.create_task(params.get("sessionId"))
        self.protocol._tasks[task.id] = task
        task.history.append(message)
        task.status = TaskStatus.WORKING
        content = await self._run_handler(task, message)
        response = Message(role=MessageRole.AGENT, content=content)
        task.history.append(response)
        task.status = TaskStatus.COMPLETED
        return {"id": task.id, "status": task.status.value, "content": content, "history": [m.model_dump() for m in task.history]}

    async def _send_message(self, params: dict[str, Any]) -> dict[str, Any]:
        task_id = params.get("taskId") or params.get("task_id")
        if not task_id:
            raise ValueError("taskId is required")
        task = self.protocol.get_task(task_id) or Task(id=task_id, status=TaskStatus.SUBMITTED)
        self.protocol._tasks[task.id] = task
        message = self._parse_message(params.get("message"))
        task.history.append(message)
        task.status = TaskStatus.WORKING
        content = await self._run_handler(task, message)
        response = Message(role=MessageRole.AGENT, content=content)
        task.history.append(response)
        task.status = TaskStatus.COMPLETED
        return {"taskId": task.id, "status": task.status.value, "content": content}

    def _parse_message(self, value: Any) -> Message:
        if isinstance(value, Message):
            return value
        if isinstance(value, dict):
            return Message(**value)
        if isinstance(value, str):
            return Message(role=MessageRole.USER, content=value)
        raise ValueError("message is required")

    async def _run_handler(self, task: Task, message: Message) -> str:
        if not self._handler:
            return f"Processed by {self.protocol.agent_id}: {message.content}"
        result = self._handler(task, message)
        if hasattr(result, "__await__"):
            result = await result  # type: ignore[assignment]
        return str(result)


def create_default_runtime() -> A2ARuntime:
    """Create the default AgentGraph A2A runtime."""
    return A2ARuntime()
