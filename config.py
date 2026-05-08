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
