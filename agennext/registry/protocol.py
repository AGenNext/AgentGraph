"""Agent Registry Protocol.

Provides in-memory registration and discovery of agents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RegistryEntry:
    agent_id: str
    name: str
    endpoint: str
    capabilities: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class AgentRegistry:
    def __init__(self) -> None:
        self._entries: dict[str, RegistryEntry] = {}

    def register(self, entry: RegistryEntry) -> RegistryEntry:
        self._entries[entry.agent_id] = entry
        return entry

    def get(self, agent_id: str) -> RegistryEntry | None:
        return self._entries.get(agent_id)

    def list(self) -> list[RegistryEntry]:
        return list(self._entries.values())

    def discover(self, capability: str | None = None, skill: str | None = None) -> list[RegistryEntry]:
        results = self.list()
        if capability:
            results = [entry for entry in results if capability in entry.capabilities]
        if skill:
            results = [entry for entry in results if skill in entry.skills]
        return results
