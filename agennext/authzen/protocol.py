"""AuthZen protocol."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AuthorizationDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass
class AuthorizationRequest:
    subject: str
    action: str
    resource: str


class AuthZenProtocol:
    def authorize(self, request: AuthorizationRequest) -> AuthorizationDecision:
        sensitive_actions = {"delete", "transfer_funds", "exfiltrate_data"}
        if request.action in sensitive_actions:
            return AuthorizationDecision.DENY
        return AuthorizationDecision.ALLOW
