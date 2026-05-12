"""
Framework Selector UI - Choose your agent framework
"""
from typing import Dict, Any


class FrameworkSelector:
    """Framework selector UI component."""

    FRAMEWORKS = {
        "openai": {"name": "OpenAI", "color": "#10A37F", "models": ["gpt-4o", "gpt-4o-mini", "o1", "o3-mini"]},
        "anthropic": {"name": "Anthropic", "color": "#D97757", "models": ["claude-sonnet-4", "claude-opus-4", "claude-3-5"]},
        "langgraph": {"name": "LangGraph", "color": "#6B47FF", "models": ["gpt-4o", "claude-3-5"]},
        "langchain": {"name": "LangChain", "color": "#6B47FF", "models": ["gpt-4o", "claude-3-5"]},
        "google": {"name": "Google ADK", "color": "#4285F4", "models": ["gemini-2.0-pro", "gemini-1.5-pro"]},
        "microsoft": {"name": "Microsoft AutoGen", "color": "#00A4EF", "models": ["gpt-4o", "claude-3"]},
        "crewai": {"name": "CrewAI", "color": "#F9C513", "models": ["gpt-4o", "claude-3"]},
        "autogen": {"name": "AutoGen", "color": "#00A4EF", "models": ["gpt-4o"]},
        "llamaindex": {"name": "LlamaIndex", "color": "#F5F5F5", "models": ["gpt-4o"]},
        "salesforce": {"name": "Salesforce Einstein", "color": "#00A1F2", "models": ["einstein-ai"]},
        "smolagents": {"name": "SmolAgents", "color": "#FF6B6B", "models": ["gpt-4o", "llama-3"]},
    }

    @staticmethod
    def selector():
        """Return framework selector config."""
        return {
            "type": "framework_selector",
            "frameworks": list(FrameworkSelector.FRAMEWORKS.keys()),
            "component": "framework_select"
        }

    @staticmethod
    def get_framework(name: str) -> Dict[str, Any]:
        """Get framework config by name."""
        return FrameworkSelector.FRAMEWORKS.get(name, {})

    @staticmethod
    def chat_component(framework: str, model: str = None):
        """Create chat component for framework."""
        fw = FrameworkSelector.FRAMEWORKS.get(framework, {})
        return {
            "type": "chat",
            "framework": framework,
            "model": model or fw.get("models", ["gpt-4o"])[0],
            "component": f"{framework}_chat"
        }

    @staticmethod
    def agent_builder(framework: str):
        """Create agent builder for framework."""
        return {
            "type": "agent_builder",
            "framework": framework,
            "component": f"{framework}_builder"
        }

    @staticmethod
    def tools_panel(framework: str):
        """Create tools panel for framework."""
        return {
            "type": "tools_panel",
            "framework": framework,
            "component": f"{framework}_tools"
        }

    @staticmethod
    def memory_panel(framework: str):
        """Create memory panel for framework."""
        return {
            "type": "memory_panel",
            "framework": framework,
            "component": f"{framework}_memory"
        }