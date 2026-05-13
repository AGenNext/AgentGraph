"""Autonomous Governance Protocol primitives for AgentGraph.

Inspired by AAGFE: ReBAC + policy gates + behavioral drift controls.
"""

from .protocol import (
    AutonomousGovernanceProtocol,
    AutonomousGovernanceRequest,
    AutonomousGovernanceResult,
    CognitiveGuardSignal,
    PolicySignal,
    ReBACRelation,
)

__all__ = [
    "AutonomousGovernanceProtocol",
    "AutonomousGovernanceRequest",
    "AutonomousGovernanceResult",
    "CognitiveGuardSignal",
    "PolicySignal",
    "ReBACRelation",
]
