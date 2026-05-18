"""Pydantic models for the Agent-Graph SDK."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SDKModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AgentCreateRequest(SDKModel):
    name: str
    description: str = ""
    provider: str = "openai"
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 2000
    system_prompt: str = ""
    status: str = "active"
    is_default: bool = False
    auth_method: str = "api_key"
    enable_chat: bool = True
    enable_rag: bool = False
    tools: list[str] = Field(default_factory=lambda: ["calculator", "search"])


class AgentUpdateRequest(SDKModel):
    name: str | None = None
    description: str | None = None
    provider: str | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    system_prompt: str | None = None
    status: str | None = None
    is_default: bool | None = None
    auth_method: str | None = None
    enable_chat: bool | None = None
    enable_rag: bool | None = None
    tools: list[str] | None = None


class CredentialVerifyRequest(SDKModel):
    credential_id: str


class MemoryCreateRequest(SDKModel):
    title: str | None = None
    content: dict[str, Any]
    content_text: str | None = None
    memory_type: str
    modality: str = "text"
    status: str = "active"
    source_kind: str | None = None
    source_ref: str | None = None
    created_by: str | None = None
    owner_ref: str | None = None
    importance: float | None = None


class ResearchCreateRequest(SDKModel):
    task: str
    topic: str | None = None
    depth: str | None = None


class SearchRequest(SDKModel):
    q: str
    framework: str | None = None
    limit: int | None = None


class ChatMessagePart(SDKModel):
    type: str
    text: str | None = None


class ChatMessageRequest(SDKModel):
    role: str
    parts: list[ChatMessagePart]
