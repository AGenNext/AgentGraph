"""Agent DID protocol."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentDIDDocument:
    did: str
    controller: str
    verification_methods: list[str] = field(default_factory=list)


class AgentDIDProtocol:
    def create(self, agent_id: str) -> AgentDIDDocument:
        did = f"did:agennext:{agent_id}"
        return AgentDIDDocument(did=did, controller=agent_id)

    def resolve(self, did: str) -> AgentDIDDocument:
        agent_id = did.split(':')[-1]
        return AgentDIDDocument(did=did, controller=agent_id)
