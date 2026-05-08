"""A2A Client for inter-agent communication."""

import asyncio
import json
from typing import Any, Optional, AsyncIterator
import aiohttp

from .messages import (
    Message,
    MessageRole,
    Task,
    TaskStatus,
    AgentResult,
)
from .protocol import A2AProtocol
from .card import get_agent_card, AgentCard


class A2AClient:
    """Async HTTP client for A2A protocol communication."""
    
    def __init__(self, agent_id: str, base_url: Optional[str] = None):
        self.agent_id = agent_id
        self.base_url = base_url or f"http://localhost:8000"
        self.protocol = A2AProtocol(agent_id, self.base_url)
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
    
    async def _request(
        self,
        method: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Make an async HTTP request to another agent."""
        if not self._session:
            self._session = aiohttp.ClientSession()
        
        request = self.protocol.build_request(method, params)
        url = f"{self.base_url}/rpc"
        
        async with self._session.post(
            url, 
            data=self.protocol.serialize(request),
            headers={"Content-Type": "application/json"}
        ) as response:
            if response.status == 200:
                text = await response.text()
                return self.protocol.deserialize(text, dict)
            else:
                return {"error": {"code": response.status, "message": "Request failed"}}
    
    # Task operations
    async def send_message(
        self,
        target_url: str,
        content: str,
        session_id: Optional[str] = None,
    ) -> Message:
        """Send a message to another agent."""
        task = self.protocol.create_task(session_id)
        self.protocol.add_message(task.id, content, MessageRole.USER)
        
        result = await self._request(
            "tasks/sendMessage",
            {"taskId": task.id, "message": {"role": "user", "content": content}},
        )
        
        if result.get("result"):
            response_data = result["result"]
            return Message(
                role=MessageRole.AGENT,
                content=response_data.get("content", ""),
            )
        raise Exception("Failed to send message")
    
    async def submit_task(
        self,
        target_url: str,
        message: str,
        skill_ids: Optional[list[str]] = None,
    ) -> Task:
        """Submit a task to another agent."""
        task = self.protocol.create_task()
        self.protocol.add_message(task.id, message, MessageRole.USER)
        
        result = await self._request(
            "tasks/submit",
            {
                "taskId": task.id,
                "message": {"role": "user", "content": message},
                "skillIds": skill_ids or [],
            },
        )
        
        if result.get("result"):
            task_data = result["result"]
            task.status = TaskStatus(task_data.get("status", "submitted"))
            return task
        raise Exception("Failed to submit task")
    
    # A2A delegation
    async def delegate_to_agent(
        self,
        target_agent_id: str,
        capability: str,
        context: dict[str, Any],
    ) -> AgentResult:
        """Delegate a task to another agent via A2A."""
        target_card = get_agent_card(target_agent_id)
        if not target_card:
            raise ValueError(f"Agent {target_agent_id} not found")
        
        message = context.get("message", "")
        task = await self.submit_task(
            target_card.url,
            message,
            skill_ids=context.get("skill_ids", []),
        )
        
        # For demo, return a mock result
        # In production, this would poll/get the response from target agent
        return self.protocol.create_result(
            agent_id=target_agent_id,
            capability=capability,
            content=f"Processed by {target_agent_id}: {message[:100]}...",
            metadata={"task_id": task.id},
        )
    
    # Streaming
    async def stream_task(
        self,
        target_url: str,
        message: str,
    ) -> AsyncIterator[str]:
        """Stream content from another agent."""
        # For demo, yield a simple response
        yield f"Streaming from {self.agent_id}: {message}"
    
    # Discovery
    async def get_agent_card(self, target_agent_id: str) -> Optional[AgentCard]:
        """Get another agent's card."""
        try:
            result = await self._request(" agents/get", {"agentId": target_agent_id})
            if result.get("result"):
                return AgentCard(**result["result"])
        except Exception:
            pass
        return get_agent_card(target_agent_id)
    
    async def list_agents(self) -> list[AgentCard]:
        """List available agents."""
        try:
            result = await self._request("agents/list", {})
            if result.get("result"):
                return [AgentCard(**card) for card in result["result"]]
        except Exception:
            pass
        from .card import get_all_agent_cards
        return get_all_agent_cards()


# Convenience functions
async def send_to_agent(
    source_agent_id: str,
    target_agent_id: str,
    message: str,
) -> str:
    """Send a message from one agent to another."""
    source_card = get_agent_card(source_agent_id)
    target_card = get_agent_card(target_agent_id)
    
    if not source_card or not target_card:
        raise ValueError("Agent not found")
    
    async with A2AClient(source_agent_id, source_card.url) as client:
        response = await client.send_message(target_card.url, message)
        return response.content


async def delegate_task(
    from_agent_id: str,
    to_agent_id: str,
    capability: str,
    context: dict[str, Any],
) -> AgentResult:
    """Delegate a task from one agent to another."""
    from .card import get_agent_card
    
    from_card = get_agent_card(from_agent_id)
    if not from_card:
        raise ValueError(f"Agent {from_agent_id} not found")
    
    async with A2AClient(from_agent_id, from_card.url) as client:
        return await client.delegate_to_agent(to_agent_id, capability, context)