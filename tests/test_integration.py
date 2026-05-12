"""Production tests."""

import os
import pytest


class TestConfig:
    def test_appconfig_from_env(self):
        from config import AppConfig
        assert AppConfig.from_env() is not None
    
    def test_validate_config(self):
        from config import validate_config
        assert validate_config() == []


class TestCore:
    def test_providers_count(self):
        from core.llm_client import PROVIDERS
        assert len(PROVIDERS) >= 40
    
    def test_registry(self):
        from core.registry import get_registry
        assert len(get_registry().list_skills()) > 0
    
    def test_schema(self):
        from core.schema import STANDARD_SKILLS, STANDARD_CAPABILITIES
        assert STANDARD_SKILLS
        assert STANDARD_CAPABILITIES
    
    def test_all_agents(self):
        from agents import __all__
        assert len(__all__) >= 10


class TestA2A:
    def test_get_all_cards(self):
        from a2a import get_all_agent_cards
        assert len(get_all_agent_cards()) > 0
    
    def test_agent_card_import(self):
        from a2a import AgentCard
        assert AgentCard is not None


class TestAgents:
    def test_agents(self):
        from agents.base_agent import BaseAgent
        assert BaseAgent is not None


class TestDockerfile:
    def test_exists(self):
        assert os.path.exists("Dockerfile")
    
    def test_has_healthcheck(self):
        with open("Dockerfile") as f:
            assert "HEALTHCHECK" in f.read()


class TestStructure:
    def test_dirs(self):
        for d in ["agents", "core", "a2a", "orchestrator"]:
            assert os.path.isdir(d)
    
    def test_files(self):
        for f in ["main.py", "config.py", "Dockerfile"]:
            assert os.path.exists(f)


class TestSchema:
    @pytest.mark.parametrize("skill", ["coding", "research", "creative_writing"])
    def test_standard_skills(self, skill):
        from core.schema import STANDARD_SKILLS
        assert skill in STANDARD_SKILLS
    
    @pytest.mark.parametrize("cap", ["text_generation", "code_generation", "image_understanding"])
    def test_standard_capabilities(self, cap):
        from core.schema import STANDARD_CAPABILITIES
        assert cap in STANDARD_CAPABILITIES
    
    def test_all_providers(self):
        from core.llm_client import PROVIDERS
        assert "openai" in PROVIDERS
        assert "anthropic" in PROVIDERS
        assert "google" in PROVIDERS


class TestRegistryFuncs:
    def test_generate_did(self):
        from core.registry import generate_did
        did = generate_did("skill", "test")
        assert did.startswith("did:")
    
    def test_parse_did(self):
        from core.registry import parse_did
        parsed = parse_did("did:content-team:skill:test:v1")
        assert parsed.get("authority") == "content-team"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])