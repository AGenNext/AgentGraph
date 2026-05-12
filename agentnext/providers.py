# LLM Providers - factory functions
from agents.providers import create_client

def get_provider(name: str, config: dict):
    """Get LLM client by name."""
    return create_client(name, config)

__all__ = ["get_provider"]