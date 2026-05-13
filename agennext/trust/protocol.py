"""Agent Trust Protocol.

Provides lightweight trust scoring for agent selection and delegation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TrustDecision(str, Enum):
    ALLOW = "allow"
    REVIEW = "review"
    DENY = "deny"


@dataclass
class AgentTrustProfile:
    agent_id: str
    score: float = 0.5
    successful_interactions: int = 0
    failed_interactions: int = 0
    endorsements: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class TrustPolicy:
    allow_threshold: float = 0.8
    review_threshold: float = 0.5


class TrustProtocol:
    def __init__(self, policy: TrustPolicy | None = None) -> None:
        self.policy = policy or TrustPolicy()
        self._profiles: dict[str, AgentTrustProfile] = {}

    def get_profile(self, agent_id: str) -> AgentTrustProfile:
        if agent_id not in self._profiles:
            self._profiles[agent_id] = AgentTrustProfile(agent_id=agent_id)
        return self._profiles[agent_id]

    def record_success(self, agent_id: str) -> AgentTrustProfile:
        profile = self.get_profile(agent_id)
        profile.successful_interactions += 1
        profile.score = min(1.0, profile.score + 0.05)
        return profile

    def record_failure(self, agent_id: str, warning: str | None = None) -> AgentTrustProfile:
        profile = self.get_profile(agent_id)
        profile.failed_interactions += 1
        profile.score = max(0.0, profile.score - 0.1)
        if warning:
            profile.warnings.append(warning)
        return profile

    def endorse(self, agent_id: str, endorsed_by: str) -> AgentTrustProfile:
        profile = self.get_profile(agent_id)
        if endorsed_by not in profile.endorsements:
            profile.endorsements.append(endorsed_by)
            profile.score = min(1.0, profile.score + 0.02)
        return profile

    def evaluate(self, agent_id: str) -> TrustDecision:
        profile = self.get_profile(agent_id)
        if profile.score >= self.policy.allow_threshold:
            return TrustDecision.ALLOW
        if profile.score >= self.policy.review_threshold:
            return TrustDecision.REVIEW
        return TrustDecision.DENY
