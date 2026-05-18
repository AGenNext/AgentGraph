"""Tests for the distributable Agent-Graph SDK."""

from __future__ import annotations

import json

import httpx

from agent_graph_sdk import AgentCreateRequest, AgentGraphClient, CredentialVerifyRequest


def test_sdk_exports_client():
    assert AgentGraphClient is not None


def test_sdk_can_create_and_list_agents():
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append((request.method, request.url.path, dict(request.url.params)))
        if request.url.path == "/agents" and request.method == "GET":
            return httpx.Response(200, json={"agents": [{"id": "1", "name": "Sales-AI"}], "total": 1})
        if request.url.path == "/agents" and request.method == "POST":
            body = json.loads(request.content.decode())
            return httpx.Response(200, json={"agent": {"id": "2", **body}, "message": "Agent created successfully"})
        if request.url.path == "/credentials/verify":
            body = json.loads(request.content.decode())
            return httpx.Response(200, json={"valid": body["credential_id"].startswith("did:"), "checked": body["credential_id"]})
        if request.url.path == "/health":
            return httpx.Response(200, json={"status": "ok"})
        return httpx.Response(404, json={"detail": "not found"})

    transport = httpx.MockTransport(handler)
    with AgentGraphClient(base_url="https://example.test", client=httpx.Client(base_url="https://example.test", transport=transport)) as sdk:
        assert sdk.health()["status"] == "ok"
        listing = sdk.agents.list(limit=1, offset=0)
        assert listing["total"] == 1
        created = sdk.agents.create(AgentCreateRequest(name="Support-AI"))
        assert created["agent"]["name"] == "Support-AI"
        verified = sdk.credentials.verify(CredentialVerifyRequest(credential_id="did:ebsi:zABC123DEF456"))
        assert verified["valid"] is True

    assert requests[0][0] == "GET"
    assert requests[0][1] == "/health"
    assert requests[1][1] == "/agents"
    assert requests[2][0] == "POST"
