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
    
    def test_parse_agent(self):
        parsed = parse_did("did:content-team:agent:microsoft:v1")
        assert parsed.get("name") == "microsoft"
    
    def test_parse_tool(self):
        parsed = parse_did("did:content-team:tool:search:v1")
        assert parsed.get("name") == "search"
    
    def test_did_suffix(self):
        did = generate_did("capability", "swarm")
        assert did.endswith(":v1")
    
    def test_did_parts(self):
        did = generate_did("framework", "hooks")
        parts = did.split(":")
        assert len(parts) == 5


class TestHooks:
    """Test middleware hooks."""
    
    def test_microsoft_hooks(self):
        from agents.microsoft_agent import MicrosoftAgent
        agent = MicrosoftAgent(enable_middleware=True)
        assert agent._middleware is not None
    
    def test_openai_hooks(self):
        from agents.openai_agent import OpenAIAgent
        agent = OpenAIAgent(enable_hooks=True)
        assert agent._hooks is not None
    
    def test_crewai_hooks(self):
        from agents.crewai_agent import CrewAIAgent
        agent = CrewAIAgent(enable_hooks=True)
        assert agent._hooks is not None
    
    def test_hooks_pre_property(self):
        from agents.openai_agent import OpenAIAgent
        agent = OpenAIAgent(enable_hooks=True)
        assert agent.pre_tool_call_hook is not None
    
    def test_hooks_post_property(self):
        from agents.openai_agent import OpenAIAgent
        agent = OpenAIAgent(enable_hooks=True)
        assert agent.post_tool_call_hook is not None


class TestSwarm:
    """Test Swarm mode."""
    
    def test_swarm_enabled(self):
        from agents.openai_agent import OpenAIAgent
        agent = OpenAIAgent(enable_swarm=True)
        assert agent.swarm is not None
    
    def test_swarm_add_agent(self):
        from agents.openai_agent import OpenAIAgent
        agent = OpenAIAgent(enable_swarm=True)
        agent.swarm.add_agent("test", "TestAgent")
        assert "test" in agent.swarm.agents
    
    def test_swarm_transfer(self):
        from agents.openai_agent import OpenAIAgent
        agent = OpenAIAgent(enable_swarm=True)
        agent.swarm.add_agent("a1", "A1")
        agent.swarm.add_agent("a2", "A2")
        agent.swarm.transfer_to("a2")
        assert agent.swarm.current_agent == "a2"


class TestProduct:
    """Test product variants."""
    
    @pytest.mark.parametrize("product", ["chatgpt", "codex", "o1", "o3", "gpt4"])
    def test_product_variant(self, product):
        from agents.openai_agent import OpenAIAgent
        agent = OpenAIAgent(product=product)
        assert agent.product == product