"""Autonomous Governance Protocol.

A lightweight implementation inspired by AAGFE (Agentic Automation Governance
For Every Entity): relationship checks, policy signals, behavioral signals,
and fail-secure decisions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ReBACRelation:
    subject: str
    relation: str
    resource: str


@dataclass
class PolicySignal:
    allowed: bool = True
    reason: str = "policy allow"


@dataclass
class CognitiveGuardSignal:
    drift_score: float = 0.0
    anomaly_score: float = 0.0
    sycophancy_score: float = 0.0
    planner_iterations: int = 0


@dataclass
class AutonomousGovernanceRequest:
    subject: str
    action: str
    resource: str
    relations: list[ReBACRelation] = field(default_factory=list)
    policy_signal: PolicySignal = field(default_factory=PolicySignal)
    cognitive_guard: CognitiveGuardSignal = field(default_factory=CognitiveGuardSignal)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AutonomousGovernanceResult:
    decision: str
    reason: str
    evidence: dict[str, Any] = field(default_factory=dict)


class AutonomousGovernanceProtocol:
    def evaluate(self, request: AutonomousGovernanceRequest) -> AutonomousGovernanceResult:
        if not request.policy_signal.allowed:
            return AutonomousGovernanceResult(
                decision="deny",
                reason=request.policy_signal.reason,
                evidence={"layer": "policy"},
            )

        if request.cognitive_guard.anomaly_score > 0.9:
            return AutonomousGovernanceResult(
                decision="deny",
                reason="anomaly score exceeds threshold",
                evidence={"layer": "cognitive_guard"},
            )

        if request.cognitive_guard.drift_score > 0.7:
            return AutonomousGovernanceResult(
                decision="review",
                reason="goal drift requires human review",
                evidence={"layer": "cognitive_guard"},
            )

        if request.cognitive_guard.sycophancy_score > 0.8:
            return AutonomousGovernanceResult(
                decision="review",
                reason="constraint erosion detected",
                evidence={"layer": "cognitive_guard"},
            )

        if request.cognitive_guard.planner_iterations > 20:
            return AutonomousGovernanceResult(
                decision="review",
                reason="planner iteration threshold exceeded",
                evidence={"layer": "cognitive_guard"},
            )

        has_relation = any(
            relation.subject == request.subject and relation.resource == request.resource
            for relation in request.relations
        )
        if request.relations and not has_relation:
            return AutonomousGovernanceResult(
                decision="deny",
                reason="required relationship not found",
                evidence={"layer": "rebac"},
            )

        return AutonomousGovernanceResult(
            decision="allow",
            reason="all governance layers passed",
            evidence={"layers": ["rebac", "policy", "cognitive_guard"]},
        )
