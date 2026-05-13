"""Minimal Agent Registry Server for Demo.

FastAPI server with agent CRUD operations.
"""

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Agent Registry API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (Supabase in production)
_in_memory_agents: dict[str, dict] = {}


def _init_fallback_data():
    """Initialize fallback data for development."""
    global _in_memory_agents
    if not _in_memory_agents:
        _in_memory_agents.update({
            "1": {
                "id": "1",
                "name": "Sales-AI",
                "description": "AI assistant for sales automation and CRM integration",
                "provider": "openai",
                "model": "gpt-4o",
                "temperature": 0.7,
                "max_tokens": 2000,
                "system_prompt": "You are a helpful sales assistant.",
                "status": "active",
                "version": "2.1",
                "is_default": True,
                "auth_method": "api_key",
                "enable_chat": True,
                "enable_rag": False,
                "tools": ["calculator", "search"],
                "created_at": "2026-03-01T10:00:00Z",
                "updated_at": "2026-03-01T10:00:00Z",
            },
            "2": {
                "id": "2",
                "name": "Support-AI",
                "description": "Customer support agent with knowledge base integration",
                "provider": "google",
                "model": "gemini-2.0-flash",
                "temperature": 0.5,
                "max_tokens": 4000,
                "system_prompt": "You are a helpful customer support agent.",
                "status": "inactive",
                "version": "1.0",
                "is_default": False,
                "auth_method": "api_key",
                "enable_chat": True,
                "enable_rag": True,
                "tools": ["calculator", "search", "database"],
                "created_at": "2026-01-15T14:30:00Z",
                "updated_at": "2026-01-15T14:30:00Z",
            },
            "3": {
                "id": "3",
                "name": "Lead-Gen-AI",
                "description": "Lead generation and qualification agent",
                "provider": "langchain",
                "model": "gpt-4o",
                "temperature": 0.8,
                "max_tokens": 3000,
                "system_prompt": "You are a lead generation specialist.",
                "status": "active",
                "version": "1.2",
                "is_default": False,
                "auth_method": "env",
                "enable_chat": True,
                "enable_rag": False,
                "tools": ["calculator", "search"],
                "created_at": "2026-02-20T09:15:00Z",
                "updated_at": "2026-02-20T09:15:00Z",
            },
        })


def _get_fallback_versions(agent_id: str):
    """Get version history for an agent."""
    if agent_id == "1":
        return [
            {
                "id": "v3",
                "agent_id": "1",
                "version": "2.1",
                "changes": "Updated model → gpt-4o, Updated temperature → 0.8",
                "created_at": "2026-03-01T10:00:00Z",
                "is_current": True,
            },
            {
                "id": "v2",
                "agent_id": "1",
                "version": "2.0",
                "changes": "Created from v1",
                "created_at": "2026-01-10T10:15:00Z",
                "is_current": False,
            },
            {
                "id": "v1",
                "agent_id": "1",
                "version": "1.0",
                "changes": "Initial version",
                "created_at": "2025-12-01T16:45:00Z",
                "is_current": False,
            },
        ]
    return []


# Initialize data
_init_fallback_data()


# ─── Agent API Endpoints ─────────────────────────────────────────────────────

@app.get("/agents")
async def list_agents(limit: int = 50, offset: int = 0, status: str = None, search: str = None):
    """List registered agents with filtering and search."""
    agents = list(_in_memory_agents.values())
    
    if status:
        agents = [a for a in agents if a.get("status") == status]
    
    if search:
        search_lower = search.lower()
        agents = [a for a in agents if search_lower in a.get("name", "").lower() or search_lower in a.get("description", "").lower()]
    
    return {
        "agents": agents[offset:offset + limit],
        "total": len(agents),
    }


@app.post("/agents")
async def create_agent(agent_data: dict):
    """Create a new agent."""
    if not agent_data.get("name"):
        raise HTTPException(status_code=400, detail="Agent name is required")
    
    agent_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    agent = {
        "id": agent_id,
        "name": agent_data.get("name", ""),
        "description": agent_data.get("description", ""),
        "provider": agent_data.get("provider", "openai"),
        "model": agent_data.get("model", "gpt-4o"),
        "temperature": agent_data.get("temperature", 0.7),
        "max_tokens": agent_data.get("max_tokens", 2000),
        "system_prompt": agent_data.get("system_prompt", ""),
        "status": agent_data.get("status", "active"),
        "version": "1.0",
        "is_default": agent_data.get("is_default", False),
        "auth_method": agent_data.get("auth_method", "api_key"),
        "enable_chat": agent_data.get("enable_chat", True),
        "enable_rag": agent_data.get("enable_rag", False),
        "tools": agent_data.get("tools", ["calculator", "search"]),
        "created_at": now,
        "updated_at": now,
    }
    
    _in_memory_agents[agent_id] = agent
    return {"agent": agent, "message": "Agent created successfully"}


@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details."""
    agent = _in_memory_agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"agent": agent}


@app.put("/agents/{agent_id}")
async def update_agent(agent_id: str, agent_data: dict):
    """Update an agent."""
    existing = _in_memory_agents.get(agent_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Bump version on update
    current_version = existing.get("version", "1.0")
    major, minor = current_version.split(".")
    new_version = f"{major}.{int(minor) + 1}"
    
    now = datetime.now(timezone.utc).isoformat()
    updated = {
        **existing,
        "name": agent_data.get("name", existing["name"]),
        "description": agent_data.get("description", existing["description"]),
        "provider": agent_data.get("provider", existing["provider"]),
        "model": agent_data.get("model", existing["model"]),
        "temperature": agent_data.get("temperature", existing["temperature"]),
        "max_tokens": agent_data.get("max_tokens", existing["max_tokens"]),
        "system_prompt": agent_data.get("system_prompt", existing["system_prompt"]),
        "status": agent_data.get("status", existing["status"]),
        "version": new_version,
        "updated_at": now,
    }
    
    _in_memory_agents[agent_id] = updated
    return {"agent": updated, "message": "Agent updated successfully"}


@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent."""
    if agent_id not in _in_memory_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    del _in_memory_agents[agent_id]
    return {"message": "Agent deleted successfully"}


@app.get("/agents/{agent_id}/versions")
async def list_agent_versions(agent_id: str):
    """Get version history for an agent."""
    versions = _get_fallback_versions(agent_id)
    return {"versions": versions}


@app.post("/agents/{agent_id}/versions/{version_id}/restore")
async def restore_agent_version(agent_id: str, version_id: str):
    """Restore an agent to a previous version."""
    return {"message": f"Restored agent {agent_id} to version {version_id}"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# Framework Types
FRAMEWORKS = [
    {"id": "langgraph", "name": "LangGraph", "description": "State-based agent workflows"},
    {"id": "langchain", "name": "LangChain", "description": "LLM chain composition"},
    {"id": "autogen", "name": "AutoGen", "description": "Multi-agent systems"},
    {"id": "crewai", "name": "CrewAI", "description": "Agent crew orchestration"},
]

# Tool Registry Data
TOOLS = [
    {"id": "1", "name": "StateGraph", "framework": "langgraph", "description": "State-based graph for agent workflows"},
    {"id": "2", "name": "AgentExecutor", "framework": "langchain", "description": "Execute agent chains"},
    {"id": "3", "name": "CodeExecutor", "framework": "autogen", "description": "Execute code in containers"},
    {"id": "4", "name": "Crew", "framework": "crewai", "description": "Crew of agents"},
    {"id": "5", "name": "ChatModel", "framework": "langchain", "description": "Chat model wrapper"},
    {"id": "6", "name": "StateManager", "framework": "langgraph", "description": "Manage agent state"},
]

@app.get("/frameworks")
async def list_frameworks():
    return {"frameworks": FRAMEWORKS}

@app.get("/tools")
async def list_tools(framework: str = None, search: str = None):
    result = TOOLS
    if framework:
        result = [t for t in result if t["framework"] == framework]
    if search:
        result = [t for t in result if search.lower() in t["name"].lower()]
    return {"tools": result, "total": len(result)}

@app.get("/tools/{tool_id}")
async def get_tool(tool_id: str):
    for t in TOOLS:
        if t["id"] == tool_id or t["framework"] + ":" + t["id"] == tool_id:
            return {"tool": t}
    raise HTTPException(status_code=404, detail="Tool not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)