"""
LangChain Deep Agent Orchestrator Module.

Runtime execution engine for multi-agent workflows.
"""

from .langgraph_workflow import (
    TeamState,
    create_workflow,
    route_agent,
    aggregate_results,
    synthesize_team_results,
)

__all__ = [
    "TeamState",
    "create_workflow",
    "route_agent",
    "aggregate_results", 
    "synthesize_team_results",
]

# Lazy-loaded workflow factory
def get_orchestrator(coordinator=None, **config):
    """Get orchestrator instance at runtime."""
    from .langgraph_workflow import create_workflow
    return create_workflow(coordinator)
