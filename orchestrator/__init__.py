"""
LangGraph Runtime Engine for Multi-Agent Workflows.

Execute multi-agent workflows at runtime.
"""

# Usage: from orchestrator import execute_workflow
#        result = execute_workflow(task, agents)

def execute_workflow(task: str, agents: list = None, **config):
    """
    Execute a multi-agent workflow at runtime.
    
    Args:
        task: The task string
        agents: List of agent names (auto-select if None)
        **config: content_type, style, length
    
    Returns:
        dict with result, quality_score
    """
    from .langgraph_workflow import create_workflow, TeamCoordinator
    
    coordinator = TeamCoordinator()
    wf = create_workflow(coordinator)
    
    state = {
        "topic": task,
        "content_type": config.get("content_type", "general"),
        "style": config.get("style", "professional"),
        "length": config.get("length", "medium"),
    }
    
    return wf.invoke(state)


def create_workflow(agent_ids: list = None):
    """
    Create a workflow instance.
    """
    from .langgraph_workflow import create_workflow, TeamCoordinator
    coordinator = TeamCoordinator(agents=agent_ids)
    return create_workflow(coordinator)
