"""Multi-agent team package."""

from .base_agent import BaseAgent, ContentRequest, ContentResult
from .openai_agent import OpenAIAgent
from .salesforce_client import EinsteinAgent as SalesforceAgent
from .microsoft_agent import MicrosoftAgent
from .google_agent import GoogleAgent
from .docker_agent import DockerAgent
from .github_agent import GitHubAgent
from .openhands_agent import OpenHandsAgent
from .llamaindex_agent import LlamaIndexAgent
from .langchain_agent import LangChainAgent
from .snowflake_agent import SnowflakeAgent
from .azure_ai_foundry_agent import AzureAIFoundryAgent
from .autogen_agent import AutoGenAgent
from .crewai_agent import CrewAIAgent
from .coordinator import TeamCoordinator

__all__ = [
    "BaseAgent", "ContentRequest", "ContentResult",
    "OpenAIAgent", "SalesforceAgent", "MicrosoftAgent", "GoogleAgent",
    "DockerAgent", "GitHubAgent", "OpenHandsAgent",
    "LlamaIndexAgent", "LangChainAgent", "SnowflakeAgent",
    "AzureAIFoundryAgent", "AutoGenAgent", "CrewAIAgent",
    "TeamCoordinator",
]