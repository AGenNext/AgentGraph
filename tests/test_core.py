"""Core unit tests."""

import pytest
from core.llm_client import PROVIDERS
from core.registry import generate_did, parse_did, get_registry


class TestProviders:
    """Test LLM providers."""
    
    def test_count(self):
        assert len(PROVIDERS) >= 40
    
    @pytest.mark.parametrize("name", ["openai", "anthropic", "google"])
    def test_has(self, name):
        assert name in PROVIDERS


class TestRegistry:
    """Test registry."""
    
    def test_did(self):
        did = generate_did("skill", "coding")
        assert "did:content-team" in did
    
    def test_parse(self):
        parsed = parse_did("did:content-team:skill:test:v1")
        assert parsed.get("name") == "test"
    
    def test_list(self):
        assert len(get_registry().list_skills()) > 0