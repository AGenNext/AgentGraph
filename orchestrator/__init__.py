"""
LangChain Deep Agent Orchestrator - Runtime Engine.

Provides multi-agent workflow execution at runtime.
"""

# Direct runtime usage:
#   from orchestrator import run_workflow
#   result = run_workflow(task, agents)

def run_workflow(task: str, agents: list = None, **config):
    """
    Run multi-agent workflow at runtime.
    
    Args:
        task: The task to execute
        agents: List of agent names to use (auto-select if None)
        **config: Additional config
    
    Returns:
        Workflow result with synthesized content
    """
    from .langgraph_workflow import create_workflow, TeamCoordinator
    
    coordinator = TeamCoordinator()
    workflow = create_workflow(coordinator)
    
    initial_state = {
        "topic": task,
        "content_type": config.get("content_type", "general"),
        "style": config.get("style", "professional"),
        "length": config.get("length", "medium"),
    }
    
    result = workflow.invoke(initial_state)
    return result


def create_team_workflow(agent_ids: list = None):
    """
    Create a workflow for specific agents at runtime.
    """
    from .langgraph_workflow import create_workflow, TeamCoordinator
    
    coordinator = TeamCoordinator(agents=agent_ids)
    return create_workflow(coordinator)
