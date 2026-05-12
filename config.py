"""
Configuration for Enterprise Multi-Agent Team.

Runtime settings via environment variables.
"""

import os
from typing import Optional


# RUNTIME CONFIGURATION
RUNTIME = os.getenv("RUNTIME", "langgraph")  # Set via RUNTIME=langgraph
RUNTIME_CONFIG = {
    "langgraph": {
        "workflow": "StateGraph",
        "state_manager": True,
    },
    # Add more runtimes here
    # "langchain": {...},
}


# LLM PROVIDER SETTINGS
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "openai")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o")

# AGENT SETTINGS
MAX_PARALLEL_AGENTS = int(os.getenv("MAX_PARALLEL_AGENTS", "5"))

# A2A SETTINGS
A2A_PORT = int(os.getenv("A2A_PORT", "8000"))


def get_runtime():
    """Get runtime from env."""
    return os.getenv("RUNTIME", "langgraph")


def get_workflow_config():
    """Get workflow configuration for current runtime."""
    return RUNTIME_CONFIG.get(get_runtime(), RUNTIME_CONFIG["langgraph"])


class AppConfig:
    """Application configuration."""

    def __init__(self):
        self.runtime = get_runtime()
        self.default_provider = DEFAULT_PROVIDER
        self.default_model = DEFAULT_MODEL
        self.max_parallel_agents = MAX_PARALLEL_AGENTS
        self.a2a_port = A2A_PORT

    @classmethod
    def from_env(cls):
        """Create config from environment."""
        return cls()

    def validate(self):
        """Validate configuration."""
        errors = []
        if self.max_parallel_agents < 1:
            errors.append("MAX_PARALLEL_AGENTS must be >= 1")
        if self.a2a_port < 1024 or self.a2a_port > 65535:
            errors.append("A2A_PORT must be 1024-65535")
        return errors


def validate_config():
    """Validate configuration."""
    errors = []
    if MAX_PARALLEL_AGENTS < 1:
        errors.append("MAX_PARALLEL_AGENTS must be >= 1")
    if A2A_PORT < 1024 or A2A_PORT > 65535:
        errors.append("A2A_PORT must be 1024-65535")
    return errors

