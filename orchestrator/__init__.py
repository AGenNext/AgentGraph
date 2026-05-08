"""
LangGraph Runtime Engine.

Workflow execution using runtime from config.
"""

def execute_workflow(task: str, agents: list = None, **config):
    """Execute workflow using configured runtime."""
    from config import get_runtime
    
    runtime = get_runtime()  # Set via RUNTIME= env var
    
    if runtime == "langgraph":
        from .langgraph_workflow import create_workflow, TeamCoordinator
        coordinator = TeamCoordinator()
        wf = create_workflow(coordinator)
        return wf.invoke({"topic": task})
    
    raise ValueError(f"Unknown runtime: {runtime}")


def create_workflow(agent_ids: list = None):
    """Create workflow instance."""
    from .langgraph_workflow import create_workflow, TeamCoordinator
    return create_workflow(TeamCoordinator(agents=agent_ids))
