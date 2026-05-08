"""
LangGraph Runtime Engine.

Initiate agents using runtime from config.
"""

def initiate_agents(task: str, agents: list = None, config: dict = None, **kwargs):
    """
    Initiate agents at runtime using configured runtime.
    
    Args:
        task: Task to execute
        agents: List of agent names (auto-select if None)
        config: Agent configuration dict
        **kwargs: Additional runtime options
    
    Returns:
        dict with result, quality_score
    """
    from config import get_runtime
    
    runtime = get_runtime()  # Set via RUNTIME= env var
    agent_config = config or {}
    
    if runtime == "langgraph":
        from .langgraph_workflow import create_workflow, TeamCoordinator
        
        coordinator = TeamCoordinator(
            agents=agents,
            max_agents=agent_config.get("max_agents", 5),
        )
        workflow = create_workflow(coordinator)
        
        state = {
            "topic": task,
            "content_type": agent_config.get("content_type", "general"),
            "style": agent_config.get("style", "professional"),
            "length": agent_config.get("length", "medium"),
        }
        state.update(kwargs)
        
        return workflow.invoke(state)
    
    raise ValueError(f"Unknown runtime: {runtime}")


def create_workflow(agent_ids: list = None):
    """Create workflow instance."""
    from .langgraph_workflow import create_workflow, TeamCoordinator
    return create_workflow(TeamCoordinator(agents=agent_ids))
