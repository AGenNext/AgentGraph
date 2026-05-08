"""
Enterprise Agent Orchestrator.

Create and manage enterprise agents with specific roles.
"""

from agents.roles import AgentRole, AgentRoleConfig, ROLE_BEHAVIORS


def create_agent(
    name: str,
    role: str = "assistant",
    config: dict = None,
    **options
):
    """
    Create an enterprise agent with a specific role.
    
    Args:
        name: Agent name/id
        role: project_driver | product_lead | assistant
        config: Role configuration
        **options: Additional options
    
    Returns:
        Configured agent instance
    """
    from config import get_runtime
    from .langgraph_workflow import TeamCoordinator
    
    # Map role string to enum
    role_enum = AgentRole(role)
    behavior = ROLE_BEHAVIORS[role_enum]
    
    agent_config = AgentRoleConfig(
        role=role_enum,
        reports_to=config.get("reports_to") if config else None,
        team_size=config.get("team_size", 0) if config else 0,
        priority=config.get("priority", 1) if config else 1,
        owns=config.get("owns", []) if config else [],
    )
    
    runtime = get_runtime()
    
    if runtime == "langgraph":
        coordinator = TeamCoordinator(agents=[name])
        return {
            "agent": name,
            "role": role,
            "behavior": behavior,
            "config": agent_config,
            "coordinator": coordinator,
        }
    
    raise ValueError(f"Unknown runtime: {runtime}")


def initiate_agents(task: str = None, agents: list = None, config: dict = None, **kwargs):
    """
    Initiate agents (legacy - for task-based workflows).
    
    For enterprise use, use create_agent() instead.
    """
    from config import get_runtime
    
    runtime = get_runtime()
    
    if runtime == "langgraph":
        from .langgraph_workflow import create_workflow, TeamCoordinator
        coordinator = TeamCoordinator(agents=agents)
        wf = create_workflow(coordinator)
        return wf.invoke({"topic": task or ""})
    
    raise ValueError(f"Unknown runtime: {runtime}")
