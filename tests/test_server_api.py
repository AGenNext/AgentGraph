"""Unit tests for server.py API endpoints."""

import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


class TestFrameworks:
    """Test /frameworks endpoint."""
    
    def test_list_frameworks(self):
        response = client.get("/frameworks")
        assert response.status_code == 200
        data = response.json()
        assert "frameworks" in data
        assert len(data["frameworks"]) >= 4
    
    def test_frameworks_have_required_fields(self):
        response = client.get("/frameworks")
        data = response.json()
        for fw in data["frameworks"]:
            assert "id" in fw
            assert "name" in fw
            assert "description" in fw


class TestTools:
    """Test /tools endpoint."""
    
    def test_list_tools(self):
        response = client.get("/tools")
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert "total" in data
        assert len(data["tools"]) >= 6
    
    def test_filter_by_framework(self):
        response = client.get("/tools?framework=langgraph")
        data = response.json()
        for tool in data["tools"]:
            assert tool["framework"] == "langgraph"
    
    def test_tool_by_id(self):
        response = client.get("/tools/1")
        assert response.status_code == 200
    
    def test_tool_not_found(self):
        response = client.get("/tools/999")
        assert response.status_code == 404


class TestCredentials:
    """Test /credentials endpoint (WaltID)."""
    
    def test_list_credentials(self):
        response = client.get("/credentials")
        assert response.status_code == 200
        data = response.json()
        assert "credentials" in data
        assert "total" in data
    
    def test_filter_by_status(self):
        response = client.get("/credentials?status=valid")
        data = response.json()
        for cred in data["credentials"]:
            assert cred["status"] == "valid"
    
    def test_credential_has_did(self):
        response = client.get("/credentials")
        data = response.json()
        for cred in data["credentials"]:
            assert "did:ebsi:" in cred["id"]
    
    def test_credential_has_signature(self):
        response = client.get("/credentials")
        data = response.json()
        for cred in data["credentials"]:
            assert "signature" in cred
            assert len(cred["signature"]) > 10
    
    def test_verify_credential(self):
        response = client.post("/credentials/verify", json={"credential_id": "did:ebsi:zABC123DEF456"})
        assert response.status_code == 200
        data = response.json()
        assert "valid" in data
    
    def test_verify_invalid_credential(self):
        response = client.post("/credentials/verify", json={"credential_id": "invalid"})
        data = response.json()
        assert data["valid"] is False


class TestHealth:
    """Test /health endpoint."""
    
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestRegistry:
    """Test /registry endpoint."""
    
    def test_registry_structure(self):
        # Registry returns various agent types
        response = client.get("/registry")
        # May return 200 or redirect - just check it's handled
        assert response.status_code in [200, 404]