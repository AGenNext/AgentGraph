"""HTTP client for the Agent-Graph API."""

from __future__ import annotations

from collections.abc import Mapping
import os
from typing import Any

import httpx

from .models import (
    AgentCreateRequest,
    AgentUpdateRequest,
    ChatMessageRequest,
    CredentialVerifyRequest,
    MemoryCreateRequest,
    ResearchCreateRequest,
    SearchRequest,
)


def _payload(data: Any | None) -> Any | None:
    if data is None:
        return None
    if hasattr(data, "model_dump"):
        return data.model_dump(exclude_none=True)
    if isinstance(data, Mapping):
        return dict(data)
    return data


class AgentGraphError(RuntimeError):
    """Base SDK error."""


class AgentGraphResponseError(AgentGraphError):
    """Raised when the API returns a non-success response."""

    def __init__(self, method: str, path: str, status_code: int, detail: str):
        super().__init__(f"{method} {path} failed with {status_code}: {detail}")
        self.method = method
        self.path = path
        self.status_code = status_code
        self.detail = detail


class _Namespace:
    def __init__(self, client: "AgentGraphClient") -> None:
        self._client = client


class AgentNamespace(_Namespace):
    def list(self, limit: int = 50, offset: int = 0, status: str | None = None, search: str | None = None):
        return self._client.get("/agents", params={"limit": limit, "offset": offset, "status": status, "search": search})

    def create(self, agent: AgentCreateRequest | Mapping[str, Any]):
        return self._client.post("/agents", json=_payload(agent))

    def get(self, agent_id: str):
        return self._client.get(f"/agents/{agent_id}")

    def update(self, agent_id: str, agent: AgentUpdateRequest | Mapping[str, Any]):
        return self._client.put(f"/agents/{agent_id}", json=_payload(agent))

    def delete(self, agent_id: str):
        return self._client.delete(f"/agents/{agent_id}")

    def versions(self, agent_id: str):
        return self._client.get(f"/agents/{agent_id}/versions")

    def restore(self, agent_id: str, version_id: str):
        return self._client.post(f"/agents/{agent_id}/versions/{version_id}/restore")


class FrameworkNamespace(_Namespace):
    def list(self):
        return self._client.get("/frameworks")


class ToolNamespace(_Namespace):
    def list(self, framework: str | None = None):
        return self._client.get("/tools", params={"framework": framework})

    def get(self, tool_id: str):
        return self._client.get(f"/tools/{tool_id}")


class CredentialNamespace(_Namespace):
    def list(self, status: str | None = None):
        return self._client.get("/credentials", params={"status": status})

    def get(self, credential_id: str):
        return self._client.get(f"/credentials/{credential_id}")

    def verify(self, credential: CredentialVerifyRequest | Mapping[str, Any]):
        return self._client.post("/credentials/verify", json=_payload(credential))


class EntityNamespace(_Namespace):
    def list(self):
        return self._client.get("/entities")

    def seed(self):
        return self._client.post("/entities/seed")

    def seed_schema_types(self):
        return self._client.post("/schema-types/seed")


class SchemaNamespace(_Namespace):
    def types(self):
        return self._client.get("/schema-types")

    def attributes(self):
        return self._client.get("/schema-attributes")

    def relations(self):
        return self._client.get("/schema-relations")


class MemoryNamespace(_Namespace):
    def list(self):
        return self._client.get("/memory")

    def create(self, memory: MemoryCreateRequest | Mapping[str, Any]):
        return self._client.post("/memory", json=_payload(memory))


class PromptNamespace(_Namespace):
    def list(self):
        return self._client.get("/prompts")

    def get(self, prompt_id: str):
        return self._client.get(f"/prompts/{prompt_id}")


class ChannelNamespace(_Namespace):
    def list(self):
        return self._client.get("/channels")


class SearchNamespace(_Namespace):
    def query(self, search: SearchRequest | Mapping[str, Any] | str, **params: Any):
        if isinstance(search, str):
            params = {"q": search, **params}
        else:
            params = {**_payload(search), **params}
        return self._client.get("/search", params=params)


class ResearchNamespace(_Namespace):
    def create(self, task: ResearchCreateRequest | Mapping[str, Any]):
        return self._client.post("/research", json=_payload(task))

    def get(self, task_id: str):
        return self._client.get(f"/research/{task_id}")


class TranscriptionNamespace(_Namespace):
    def create(self, payload: Mapping[str, Any] | Any):
        return self._client.post("/transcribe", json=_payload(payload))

    def get(self, transcript_id: str):
        return self._client.get(f"/transcribe/{transcript_id}")


class MediaNamespace(_Namespace):
    def tts(self, payload: Mapping[str, Any] | Any):
        return self._client.post("/tts", json=_payload(payload))

    def image(self, payload: Mapping[str, Any] | Any):
        return self._client.post("/generate/image", json=_payload(payload))


class ExecutionNamespace(_Namespace):
    def run(self, payload: Mapping[str, Any] | Any):
        return self._client.post("/execute", json=_payload(payload))

    def browser_navigate(self, payload: Mapping[str, Any] | Any):
        return self._client.post("/browser/navigate", json=_payload(payload))

    def browser_execute(self, payload: Mapping[str, Any] | Any):
        return self._client.post("/browser/execute", json=_payload(payload))

    def computer_action(self, payload: Mapping[str, Any] | Any):
        return self._client.post("/computer/action", json=_payload(payload))


class ArtifactNamespace(_Namespace):
    def list(self):
        return self._client.get("/artifacts")


class NotebookNamespace(_Namespace):
    def list(self):
        return self._client.get("/notebook/cells")


class ChatNamespace(_Namespace):
    def history(self):
        return self._client.get("/chat/history")

    def send(self, message: ChatMessageRequest | Mapping[str, Any]):
        return self._client.post("/chat", json=_payload(message))


class AgentGraphClient:
    """Sync SDK client for the Agent-Graph API."""

    def __init__(
        self,
        base_url: str | None = None,
        *,
        client: httpx.Client | None = None,
        timeout: float = 30.0,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self.base_url = base_url or os.getenv("AGENT_GRAPH_BASE_URL", "http://localhost:8000")
        self._owned_client = client is None
        self._client = client or httpx.Client(base_url=self.base_url, timeout=timeout, headers=dict(headers or {}))
        if headers and client is not None:
            self._client.headers.update(headers)

        self.agents = AgentNamespace(self)
        self.frameworks = FrameworkNamespace(self)
        self.tools = ToolNamespace(self)
        self.credentials = CredentialNamespace(self)
        self.entities = EntityNamespace(self)
        self.schema = SchemaNamespace(self)
        self.memory = MemoryNamespace(self)
        self.prompts = PromptNamespace(self)
        self.channels = ChannelNamespace(self)
        self.search = SearchNamespace(self)
        self.research = ResearchNamespace(self)
        self.transcribe = TranscriptionNamespace(self)
        self.media = MediaNamespace(self)
        self.execution = ExecutionNamespace(self)
        self.artifacts = ArtifactNamespace(self)
        self.notebook = NotebookNamespace(self)
        self.chat = ChatNamespace(self)

    def close(self) -> None:
        if self._owned_client:
            self._client.close()

    def __enter__(self) -> "AgentGraphClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def request(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, json: Any | None = None):
        response = self._client.request(method, path, params=params, json=_payload(json))
        if response.is_error:
            try:
                detail = response.json()
            except Exception:  # pragma: no cover - defensive
                detail = response.text
            raise AgentGraphResponseError(method, path, response.status_code, str(detail))
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return response.text

    def get(self, path: str, *, params: Mapping[str, Any] | None = None):
        return self.request("GET", path, params=params)

    def post(self, path: str, *, params: Mapping[str, Any] | None = None, json: Any | None = None):
        return self.request("POST", path, params=params, json=json)

    def put(self, path: str, *, params: Mapping[str, Any] | None = None, json: Any | None = None):
        return self.request("PUT", path, params=params, json=json)

    def delete(self, path: str, *, params: Mapping[str, Any] | None = None):
        return self.request("DELETE", path, params=params)

    def health(self):
        return self.get("/health")

    def list_agents(self, **kwargs: Any):
        return self.agents.list(**kwargs)

    def get_agent(self, agent_id: str):
        return self.agents.get(agent_id)

    def create_agent(self, agent: AgentCreateRequest | Mapping[str, Any]):
        return self.agents.create(agent)

    def update_agent(self, agent_id: str, agent: AgentUpdateRequest | Mapping[str, Any]):
        return self.agents.update(agent_id, agent)

    def delete_agent(self, agent_id: str):
        return self.agents.delete(agent_id)

    def list_frameworks(self):
        return self.frameworks.list()

    def list_tools(self, framework: str | None = None):
        return self.tools.list(framework=framework)

    def list_credentials(self, status: str | None = None):
        return self.credentials.list(status=status)
