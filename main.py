# Agent Backend - Multi-Framework A2A Server
# Supports: LangGraph, LangChain, AutoGen, CrewAI, OpenAI Agents, Anthropic, Custom

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime
from enum import Enum
import uuid
import asyncio

app = FastAPI(title="A2A Agent Multi-Framework Backend")

# ─── Models ─────────────────────────────────────────────────────────────────────────────

class FrameworkType(str, Enum):
    """Supported agent frameworks"""
    LANGGRAPH = "langgraph"       # LangGraph
    LANGCHAIN = "langchain"     # LangChain 
    AUTOGEN = "autogen"        # Microsoft AutoGen
    CREWAI = "crewai"         # CrewAI
    OPENAI = "openai"         # OpenAI Agents SDK
    ANTHROPIC = "anthropic"    # Anthropic CLI
    CUSTOM = "custom"         # Custom agent

class TaskStatus(str, Enum):
    PENDING_CONTEXT = "pending-context"
    RUNNING = "running"
    COMPLETED = "completed"
    STOPPED = "stopped"
    FAILED = "failed"

class TaskSubmission(BaseModel):
    agentUrl: str
    message: str
    framework: FrameworkType = FrameworkType.CUSTOM
    preFlightRequired: bool = False
    runToCompletion: bool = True
    requiredContext: list[str] = []
    useCheckpoints: bool = False
    checkpoints: list[dict] = []

class TaskContext(BaseModel):
    goal: str
    credentials: dict[str, str] = {}
    repo: dict[str, Any] = {}
    imports: list[str] = []
    exports: list[str] = []
    uiClarifications: dict[str, Any] = {}
    details: dict[str, Any] = {}

class CheckpointState(BaseModel):
    step: int
    learnings: list[str] = []
    decisions: list[dict] = []
    mistakesFixed: list[dict] = []
    context: dict[str, Any] = {}
    filesModified: list[str] = []
    knowledgeBase: dict[str, Any] = {}
    savedAt: str = ""

# ─── Framework Adapter Interface ───────────────────────────────────────────

class FrameworkAdapter:
    """Base adapter - implement for your framework"""
    
    async def run(self, task_id: str, context: dict, checkpoints: list) -> dict:
        """Execute the agent"""
        raise NotImplementedError

# ─── Framework Implementations ──────────────────────────────────────────────

class LangGraphAdapter(FrameworkAdapter):
    """LangGraph adapter"""
    
    async def run(self, task_id: str, context: dict, checkpoints: list) -> dict:
        return {"status": "completed", "result": "LangGraph placeholder"}


class LangChainAdapter(FrameworkAdapter):
    """LangChain adapter"""
    
    async def run(self, task_id: str, context: dict, checkpoints: list) -> dict:
        return {"status": "completed", "result": "LangChain placeholder"}


class AutoGenAdapter(FrameworkAdapter):
    """Microsoft AutoGen adapter"""
    
    async def run(self, task_id: str, context: dict, checkpoints: list) -> dict:
        return {"status": "completed", "result": "AutoGen placeholder"}


class CrewAIAdapter(FrameworkAdapter):
    """CrewAI adapter"""
    
    async def run(self, task_id: str, context: dict, checkpoints: list) -> dict:
        return {"status": "completed", "result": "CrewAI placeholder"}


class OpenAIAdapter(FrameworkAdapter):
    """OpenAI Agents SDK adapter"""
    
    async def run(self, task_id: str, context: dict, checkpoints: list) -> dict:
        return {"status": "completed", "result": "OpenAI Agents SDK placeholder"}


class AnthropicAdapter(FrameworkAdapter):
    """Anthropic Claude adapter"""
    
    async def run(self, task_id: str, context: dict, checkpoints: list) -> dict:
        return {"status": "completed", "result": "Anthropic Claude placeholder"}


class CustomAdapter(FrameworkAdapter):
    """Custom agent adapter"""
    
    async def run(self, task_id: str, context: dict, checkpoints: list) -> dict:
        return {"status": "completed", "result": "Custom agent execution"}

# ─── Main Backend ────────────────────────────────────────────────────────────────

class AgentBackend:
    """Multi-framework agent backend"""
    
    FRAMEWORK_ADAPTERS = {
        FrameworkType.LANGGRAPH: LangGraphAdapter(),
        FrameworkType.LANGCHAIN: LangChainAdapter(),
        FrameworkType.AUTOGEN: AutoGenAdapter(),
        FrameworkType.CREWAI: CrewAIAdapter(),
        FrameworkType.OPENAI: OpenAIAdapter(),
        FrameworkType.ANTHROPIC: AnthropicAdapter(),
        FrameworkType.CUSTOM: CustomAdapter(),
    }
    
    def __init__(self):
        self.tasks: dict[str, dict] = {}
        self.checkpoints: dict[str, list[CheckpointState]] = {}
        self.learnings: dict[str, list[str]] = {}
    
    async def create_task(self, submission: TaskSubmission) -> dict:
        task_id = str(uuid.uuid4())
        
        self.tasks[task_id] = {
            "id": task_id,
            "status": TaskStatus.PENDING_CONTEXT.value if submission.preFlightRequired else TaskStatus.RUNNING.value,
            "submission": submission.model_dump(),
            "framework": submission.framework,
            "context": {},
            "requiredContext": submission.requiredContext or ["credentials", "repoDetails", "importsExports", "uiClarifications"],
            "runToCompletion": submission.runToCompletion,
            "checkpoints": submission.checkpoints,
            "currentCheckpoint": 0,
        }
        
        self.checkpoints[task_id] = []
        self.learnings[task_id] = []
        
        return {"taskId": task_id, "status": self.tasks[task_id]["status"]}
    
    async def get_task(self, task_id: str) -> dict:
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        return self.tasks[task_id]
    
    async def provide_context(self, task_id: str, context: TaskContext) -> dict:
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task = self.tasks[task_id]
        ctx = context.model_dump()
        
        pending = []
        for field in task["requiredContext"]:
            if field == "credentials" and not ctx.get("credentials"):
                pending.append("credentials")
            elif field == "repoDetails" and not ctx.get("repo"):
                pending.append("repoDetails")
            elif field == "importsExports" and not ctx.get("imports"):
                pending.append("importsExports")
            elif field == "uiClarifications" and not ctx.get("uiClarifications"):
                pending.append("uiClarifications")
        
        if pending:
            return {"pendingFields": pending, "status": "pending-context"}
        
        task["status"] = TaskStatus.RUNNING.value
        task["context"] = ctx
        
        adapter = self.FRAMEWORK_ADAPTERS.get(task["framework"])
        if adapter:
            result = await adapter.run(task_id, ctx, task.get("checkpoints", []))
            task["result"] = result
            task["status"] = TaskStatus.COMPLETED.value
        
        return {"status": "running"}
    
    async def save_checkpoint(self, task_id: str, state: CheckpointState) -> dict:
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if task_id not in self.checkpoints:
            self.checkpoints[task_id] = []
        
        self.checkpoints[task_id].append(state)
        self.learnings[task_id].extend(state.learnings)
        self.learnings[task_id].extend([m["fix"] for m in state.mistakesFixed])
        
        return {"checkpointIndex": len(self.checkpoints[task_id]) - 1}
    
    async def get_checkpoint_history(self, task_id: str) -> list:
        return [s.model_dump() for s in self.checkpoints.get(task_id, [])]
    
    async def get_learnings(self, task_id: str) -> dict:
        learnings = self.learnings.get(task_id, [])
        return {"totalMistakesFixed": len([l for l in learnings if "fix" in str(l)]), "learnings": learnings}

backend = AgentBackend()

# ─── API Routes ────────────────────────────────────────────────────────────────

@app.post("/tasks")
async def create_task(submission: TaskSubmission):
    return await backend.create_task(submission)

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    return await backend.get_task(task_id)

@app.post("/tasks/{task_id}/context")
async def provide_context(task_id: str, context: TaskContext):
    return await backend.provide_context(task_id, context)

@app.post("/tasks/{task_id}/checkpoint/state")
async def save_checkpoint(task_id: str, state: CheckpointState):
    return await backend.save_checkpoint(task_id, state)

@app.get("/tasks/{task_id}/checkpoint/history")
async def get_checkpoint_history(task_id: str):
    return await backend.get_checkpoint_history(task_id)

@app.get("/tasks/{task_id}/learnings")
async def get_learnings(task_id: str):
    return await backend.get_learnings(task_id)

@app.get("/health")
async def health():
    return {"status": "ok", "frameworks": [f.value for f in FrameworkType]}

# ─── Pre-Flight Context Endpoints ─────────────────────────────────────────────────

@app.post("/tasks/preflight")
async def submit_with_preflight(submission: TaskSubmission):
    """Submit with pre-flight check - gather all context first, run to completion"""
    submission.preFlightRequired = True
    submission.runToCompletion = True
    return await backend.create_task(submission)

@app.post("/tasks/{task_id}/stop")
async def stop_task(task_id: str, reason: dict):
    """External intervention - stop a running task"""
    if task_id not in backend.tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = backend.tasks[task_id]
    task["status"] = TaskStatus.STOPPED.value
    task["stopReason"] = {"type": "external-intervention", "reason": reason.get("reason", "Stopped by user")}
    
    return {"status": "stopped", "reason": reason.get("reason")}

# ─── Checkpoint Endpoints ─────────────────────────────────────────────────

@app.post("/tasks/checkpoints")
async def submit_with_checkpoints(submission: TaskSubmission, checkpoints: list[dict]):
    """Submit task with checkpoints - saves state at each stop"""
    submission.useCheckpoints = True
    submission.checkpoints = checkpoints
    submission.runToCompletion = True
    return await backend.create_task(submission)

@app.get("/tasks/{task_id}/checkpoint/state")
async def get_checkpoint_state(task_id: str):
    """Get current checkpoint state"""
    if task_id not in backend.checkpoints:
        raise HTTPException(status_code=404, detail="No checkpoints found")
    
    checkpoints = backend.checkpoints[task_id]
    if not checkpoints:
        raise HTTPException(status_code=404, detail="No checkpoint saved")
    
    return checkpoints[-1].model_dump()

@app.post("/tasks/{task_id}/checkpoint/{index}/resume")
async def resume_from_checkpoint(task_id: str, index: int):
    """Resume from a specific checkpoint"""
    if task_id not in backend.checkpoints:
        raise HTTPException(status_code=404, detail="No checkpoints found")
    
    checkpoints = backend.checkpoints[task_id]
    if index < 0 or index >= len(checkpoints):
        raise HTTPException(status_code=400, detail="Invalid checkpoint index")
    
    task = backend.tasks.get(task_id)
    if task:
        task["status"] = TaskStatus.RUNNING.value
        task["currentCheckpoint"] = index
    
    return {"taskId": task_id, "resumedFrom": index}

@app.get("/tasks/{task_id}/learnings")
async def get_all_learnings(task_id: str):
    """Get all learnings accumulated across all runs"""
    learnings = backend.learnings.get(task_id, [])
    checkpoints = backend.checkpoints.get(task_id, [])
    
    all_learnings = []
    total_mistakes = 0
    
    for cp in checkpoints:
        all_learnings.extend(cp.learnings)
        total_mistakes += len(cp.mistakesFixed)
    
    knowledge_base = {}
    for cp in checkpoints:
        knowledge_base.update(cp.knowledgeBase)
    
    return {
        "totalMistakesFixed": total_mistakes,
        "totalCheckpoints": len(checkpoints),
        "learnings": all_learnings,
        "knowledgeBase": knowledge_base,
    }

# ─── Task Management Endpoints ───────────────────────────────────────────

@app.get("/tasks")
async def list_tasks(limit: int = 10, offset: int = 0):
    """List all tasks"""
    tasks = list(backend.tasks.values())[offset:offset + limit]
    return {"tasks": tasks, "total": len(backend.tasks)}

@app.post("/tasks/{task_id}/cancel")
async def cancel_task(task_id: str):
    """Cancel a task"""
    if task_id not in backend.tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = backend.tasks[task_id]
    task["status"] = TaskStatus.STOPPED.value
    task["stopReason"] = {"type": "external-intervention", "reason": "Cancelled"}
    
    return {"status": "cancelled"}

@app.get("/agents")
async def list_agents():
    """List registered agents"""
    return {"agents": [], "message": "Implement agent registry here"}

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details"""
    raise HTTPException(status_code=404, detail="Agent not found")

# ─── Legacy Endpoints (for backward compat) ──────────────────────────────

@app.get("/approvals")
async def list_pending_approvals():
    """List pending approval requests"""
    pending = [t for t in backend.tasks.values() if t.get("status") == TaskStatus.PENDING_CONTEXT.value]
    return {"approvals": pending}

@app.post("/approvals/{task_id}")
async def respond_to_approval(task_id: str, response: dict):
    """Respond to approval request"""
    return await backend.provide_context(task_id, TaskContext(
        goal=response.get("response", ""),
        credentials={},
        repo={},
    ))