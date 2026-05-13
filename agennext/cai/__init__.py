"""CAI agent integration primitives for AgentGraph.

This package provides a safe adapter surface for connecting Cybersecurity AI
agents into AgentGraph under trust, governance, and authorization controls.
"""

from .adapter import CAIAgentAdapter, CAITaskRequest, CAITaskResult

__all__ = ["CAIAgentAdapter", "CAITaskRequest", "CAITaskResult"]
