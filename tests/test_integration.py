"""Production tests."""

import os
import pytest


class TestConfig:
    def test_appconfig_from_env(self):
        from config import AppConfig
        assert AppConfig.from_env() is not None
    
    def test_validate_config(self):
        from config import validate_config
        assert validate_config() is True


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


class TestA2A:
    def test_get_all_cards(self):
        from a2a import get_all_agent_cards
        assert len(get_all_agent_cards()) > 0


class TestAgents:
    def test_agents(self):
        from agents import OpenAIAgent, SalesforceAgent, MicrosoftAgent, GoogleAgent
        assert OpenAIAgent().agent_id
        assert SalesforceAgent().agent_id
        assert MicrosoftAgent().agent_id
        assert GoogleAgent().agent_id


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])