"""Agent Governance Protocol.

Provides simple approval and policy enforcement primitives for agent actions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GovernanceDecision(str, Enum):
    ALLOW = "allow"
    REVIEW = "review"
    DENY = "deny"


@dataclass
class GovernanceRequest:
    actor_id: str
    action: str
    resource: str
    risk: RiskLevel = RiskLevel.LOW
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GovernancePolicy:
    review_actions: list[str] = field(default_factory=lambda: ["deploy", "delete", "transfer_funds"])
    denied_actions: list[str] = field(default_factory=lambda: ["exfiltrate_data"])
    high_risk_requires_review: bool = True


@dataclass
class GovernanceResult:
    decision: GovernanceDecision
    reason: str


class AgentGovernanceProtocol:
    def __init__(self, policy: GovernancePolicy | None = None) -> None:
        self.policy = policy or GovernancePolicy()

    def evaluate(self, request: GovernanceRequest) -> GovernanceResult:
        if request.action in self.policy.denied_actions:
            return GovernanceResult(GovernanceDecision.DENY, "Action explicitly denied by policy")

        if request.action in self.policy.review_actions:
            return GovernanceResult(GovernanceDecision.REVIEW, "Action requires approval")

        if self.policy.high_risk_requires_review and request.risk in {RiskLevel.HIGH, RiskLevel.CRITICAL}:
            return GovernanceResult(GovernanceDecision.REVIEW, "High-risk action requires review")

        return GovernanceResult(GovernanceDecision.ALLOW, "Action allowed by policy")
