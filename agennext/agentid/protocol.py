"""Agent ID protocol.

Lightweight identity and token issuance for agents.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


@dataclass
class AgentIdentity:
    agent_id: str
    name: str
    issuer: str = "agennext"


@dataclass
class AgentToken:
    token: str
    subject: str
    issuer: str = "agennext"


class AgentIdentityProtocol:
    def issue_token(self, identity: AgentIdentity) -> AgentToken:
        return AgentToken(token=str(uuid4()), subject=identity.agent_id, issuer=identity.issuer)

    def validate_token(self, token: AgentToken) -> bool:
        return bool(token.token and token.subject)
