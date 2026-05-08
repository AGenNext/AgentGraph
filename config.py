"""Configuration for Multi-SDK Content Writing Agent."""

import os
from typing import Optional
from dataclasses import dataclass


# ============================================================
# WaltID Integration (separate repo)
# https://github.com/content-team/waltid-issuer
# ============================================================
WALTID_API_URL = os.getenv("WALTID_API_URL", "")  # e.g., https://your-waltid.com
WALTID_API_KEY = os.getenv("WALTID_API_KEY", "")
WALTID_ISSUER_DID = os.getenv("WALTID_ISSUER_DID", "")  # Your issuer DID


@dataclass
class AgentConfig:
    """Configuration for an individual SDK agent."""
    
    name: str
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000


@dataclass
class A2AConfig:
    """Configuration for A2A protocol."""
    
    host: str = "localhost"
    port: int = 8000
    agent_card_path: str = "/.well-known/agent.json"


@dataclass
class AppConfig:
    """Main application configuration."""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    
    # Salesforce Configuration
    salesforce_client_id: Optional[str] = None
    salesforce_client_secret: Optional[str] = None
    salesforce_instance_url: Optional[str] = None
    
    # Microsoft Azure Configuration
    azure_openai_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_deployment: str = "gpt-4"
    
    # Google ADK Configuration
    google_api_key: Optional[str] = None
    google_model: str = "gemini-2.0-flash"
    
    # A2A Configuration
    a2a_host: str = "localhost"
    a2a_port: int = 8000
    
    # LangGraph Configuration
    enable_parallel: bool = True
    parallel_timeout: int = 60
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables."""
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            salesforce_client_id=os.getenv("SALESFORCE_CLIENT_ID"),
            salesforce_client_secret=os.getenv("SALESFORCE_CLIENT_SECRET"),
            salesforce_instance_url=os.getenv("SALESFORCE_INSTANCE_URL"),
            azure_openai_key=os.getenv("AZURE_OPENAI_KEY"),
            azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_openai_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4"),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            google_model=os.getenv("GOOGLE_MODEL", "gemini-2.0-flash"),
            a2a_host=os.getenv("A2A_HOST", "localhost"),
            a2a_port=int(os.getenv("A2A_PORT", "8000")),
            enable_parallel=os.getenv("ENABLE_PARALLEL", "true").lower() == "true",
            parallel_timeout=int(os.getenv("PARALLEL_TIMEOUT", "60")),
        )


# Global configuration instance
config = AppConfig.from_env()

def validate_config() -> bool:
    """Validate required configuration."""
    required = []
    for var in required:
        if not os.getenv(var):
            print(f"Warning: {var} not set")
    return True


# Chatwoot Configuration
CHATWOOT_ACCOUNT_ID = os.getenv("CHATWOOT_ACCOUNT_ID")
CHATWOOT_APP_URL = os.getenv("CHATWOOT_APP_URL")
CHATWOOT_TOKEN = os.getenv("CHATWOOT_TOKEN")
