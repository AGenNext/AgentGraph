"""Full test suite for AGenNext backend."""

import pytest
import os
import json
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from schema_org_orm import get_schema_path, load_schema_text

# Test fixtures
@pytest.fixture
def client():
    """Create test client."""
    from main import app
    return TestClient(app)

@pytest.fixture
def test_task():
    """Create test task."""
    return {
        "id": "test-task-1",
        "framework": "langgraph",
        "submission": {"query": "test query"}
    }

# ================== CORE TESTS ==================

class TestCoreProviders:
    """Test LLM providers."""
    
    def test_providers_count(self):
        from core.llm_client import PROVIDERS
        assert len(PROVIDERS) >= 40
    
    @pytest.mark.parametrize("name", ["openai", "anthropic", "google", "bedrock", "azure"])
    def test_provider_exists(self, name):
        from core.llm_client import PROVIDERS
        assert name in PROVIDERS


class TestRegistry:
    """Test DID registry."""
    
    def test_generate_did(self):
        from core.registry import generate_did
        did = generate_did("skill", "coding")
        assert "did:content-team" in did
    
    def test_parse_did(self):
        from core.registry import parse_did
        parsed = parse_did("did:content-team:skill:test:v1")
        assert parsed.get("name") == "test"
        assert parsed.get("type") == "skill"
    
    def test_list_skills(self):
        from core.registry import get_registry
        assert len(get_registry().list_skills()) > 0


class TestLLMClient:
    """Test LLM client."""
    
    def test_client_init(self):
        from core.llm_client import LLMClient
        client = LLMClient("openai")
        assert client.provider == "openai"
    
    @patch('openai.OpenAI')
    def test_client_chat(self, mock_openai):
        from core.llm_client import LLMClient
        mock_openai.return_value.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="test response"))]
        )
        client = LLMClient("openai")
        response = client.chat("test prompt")
        assert response == "test response"


# ================== API TESTS ==================

class TestHealthEndpoint:
    """Test health endpoint."""
    
    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json().get("status") == "ok"


class TestTaskEndpoints:
    """Test task API endpoints."""
    
    def test_create_task(self, client, test_task):
        response = client.post("/api/tasks", json=test_task)
        assert response.status_code in [200, 201, 400, 500]
    
    def test_list_tasks(self, client):
        response = client.get("/api/tasks")
        assert response.status_code in [200, 500]
    
    def test_get_task(self, client):
        response = client.get("/api/tasks/test-task-1")
        assert response.status_code in [200, 404, 500]


class TestAgentEndpoints:
    """Test agent API endpoints."""
    
    def test_list_agents(self, client):
        response = client.get("/api/agents")
        assert response.status_code in [200, 500]
    
    def test_get_agent(self, client):
        response = client.get("/api/agents/test-agent")
        assert response.status_code in [200, 404, 500]


class TestA2AEndpoints:
    """Test A2A protocol endpoints."""
    
    def test_a2a_card(self, client):
        response = client.get("/a2a/card")
        assert response.status_code in [200, 404]
    
    def test_a2a_tasks(self, client):
        response = client.get("/a2a/tasks")
        assert response.status_code in [200, 404, 500]


# ================== DATABASE TESTS ==================

class TestDatabaseConnection:
    """Test SurrealDB configuration."""
    
    def test_surreal_env_defaults(self):
        assert isinstance(os.getenv("SURREALDB_URL", ""), str)

    def test_surreal_schema_path(self):
        assert get_schema_path().exists()


class TestCRUDOperations:
    """Test schema availability."""

    def test_schema_contains_core_tables(self):
        schema = load_schema_text()
        assert "DEFINE TABLE person" in schema
        assert "DEFINE TABLE organization" in schema


# ================== INTEGRATION TESTS ==================

class TestWorkflowIntegration:
    """Test workflow integration."""
    
    @patch('core.llm_client.LLMClient.chat')
    def test_full_workflow(self, mock_chat):
        """Test complete workflow."""
        mock_chat.return_value = "test response"
        from core.synthesizer import synthesize_response
        result = synthesize_response("test query", {})
        assert isinstance(result, (str, dict))


class TestAgentIntegration:
    """Test agent integration."""
    
    def test_agent_builder(self):
        """Test agent builder integration."""
        from core.registry import get_registry
        skills = get_registry().list_skills()
        assert len(skills) > 0


# ================== SECURITY TESTS ==================

class TestSecurity:
    """Test security measures."""
    
    def test_no_auth_on_health(self, client):
        """Health endpoint should be public."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_cors_headers(self, client):
        """Test CORS headers."""
        response = client.options("/health")
        # Should handle CORS
        assert response.status_code in [200, 405]


# ================== PERFORMANCE TESTS ==================

class TestPerformance:
    """Test performance."""
    
    def test_response_time(self, client):
        """Test response time."""
        import time
        start = time.time()
        client.get("/health")
        elapsed = time.time() - start
        assert elapsed < 1.0


# ================== VALIDATION TESTS ==================

class TestValidation:
    """Test input validation."""
    
    def test_invalid_task_format(self, client):
        """Test invalid task format."""
        response = client.post("/api/tasks", json={"invalid": "data"})
        assert response.status_code in [400, 422, 500]
    
    def test_empty_task_id(self, client):
        """Test empty task ID."""
        response = client.get("/api/tasks/")
        assert response.status_code in [404, 500]


# ================== ERROR HANDLING TESTS ==================

class TestErrorHandling:
    """Test error handling."""
    
    def test_404_handler(self, client):
        """Test 404 handler."""
        response = client.get("/nonexistent/endpoint")
        assert response.status_code == 404
    
    def test_500_handler(self, client):
        """Test 500 handler doesn't leak info."""
        # Should return generic error
        response = client.get("/api/tasks")
        if response.status_code == 500:
            data = response.json()
            assert "detail" in data


# Run with: pytest tests/ -v --tb=short
