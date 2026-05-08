"""
AI Provider API Integration with Custom Provider Support.

Custom provider = OpenAI-compatible endpoint (any LLM).
"""

import json
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Iterator


class AIClient(ABC):
    """Base AI Client."""
    
    @abstractmethod
    def chat(self, messages: List[Dict], model: str, **kwargs) -> Dict:
        pass
    
    @abstractmethod
    def stream(self, messages: List[Dict], model: str, **kwargs) -> Iterator:
        pass


# === CUSTOM (OPENAI COMPATIBLE) - THE DEFAULT ===

class CustomLLMClient(AIClient):
    """
    Custom LLM with OpenAI-compatible API.
    This is the PRIMARY client - accepts ANY /v1/chat/completions endpoint.
    """
    
    def __init__(self, base_url: str, api_key: str = None, model: str = "default"):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "dummy"
        self.model = model
    
    def _headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Dict:
        """OpenAI-compatible /chat/completions."""
        import requests
        model = model or self.model
        url = f"{self.base_url}/v1/chat/completions"
        data = {"model": model, "messages": messages, **kwargs}
        resp = requests.post(url, json=data, headers=self._headers(), timeout=120)
        resp.raise_for_status()
        return resp.json()
    
    def stream(self, messages: List[Dict], model: str = None, **kwargs) -> Iterator:
        """Streaming."""
        import requests
        model = model or self.model
        url = f"{self.base_url}/v1/chat/completions"
        data = {"model": model, "messages": messages, "stream": True, **kwargs}
        resp = requests.post(url, json=data, headers=self._headers(), stream=True, timeout=120)
        for line in resp.iter_lines():
            if line:
                yield line.decode("utf-8")
    
    def list_models(self) -> List[str]:
        """List models."""
        import requests
        url = f"{self.base_url}/v1/models"
        try:
            resp = requests.get(url, headers=self._headers(), timeout=10)
            if resp.status_code == 200:
                return [m["id"] for m in resp.json().get("data", [])]
        except:
            pass
        return [self.model]
    
    def embeddings(self, text: str) -> List[float]:
        """Get embeddings."""
        import requests
        url = f"{self.base_url}/v1/embeddings"
        data = {"model": self.model, "input": text}
        resp = requests.post(url, json=data, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]


# === PROVIDER ALIASES ===

PROVIDER_ALIASES = {
    # Cloud providers
    "openai": "https://api.openai.com/v1",
    "anthropic": "https://api.anthropic.com",  # Different API
    "google": "https://generativelanguage.googleapis.com",
    "azure": None,  # Has custom endpoint format
    "bedrock": None,  # AWS-specific
    
    # Local
    "ollama": "http://localhost:11434",
    "lmstudio": "http://localhost:1234",
    "vllm": "http://localhost:8000",
    "local": "http://localhost:11434",
}


def create_client(provider: str, config: Dict) -> AIClient:
    """
    Create AI client - custom provider is PRIMARY.
    
    Usage:
      config = {
          "provider_base_url": "https://my-llm.com/v1",  # Required for custom
          "provider_api_key": "sk-...",
          "model": "my-model",
      }
      client = create_client("custom", config)
    """
    
    p = provider.lower()
    
    # Special providers (non-OpenAI compatible)
    if p == "anthropic":
        return AnthropicClient(config.get("provider_api_key"), config.get("provider_base_url"))
    if p == "bedrock":
        return BedrockClient(config.get("aws_region"), config.get("credentials"))
    
    # DEFAULT: Custom LLM (OpenAI compatible)
    # This works for: openai, google, azure, ollama, lmstudio, vllm, local, and ANY custom
    base_url = config.get("provider_base_url")
    
    # Try provider alias if no base_url
    if not base_url and p in PROVIDER_ALIASES:
        base_url = PROVIDER_ALIASES[p]
    
    if not base_url:
        raise ValueError(f"provider_base_url required for: {provider}")
    
    return CustomLLMClient(
        base_url=base_url,
        api_key=config.get("provider_api_key"),
        model=config.get("model", p)
    )


# === ADDITIONAL SPECIAL CLIENTS ===

class AnthropicClient(AIClient):
    """Anthropic (different API)."""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.anthropic.com"
    
    def chat(self, messages: List[Dict], model: str = "claude-3-5-sonnet-20241022", **kwargs) -> Dict:
        import requests
        url = f"{self.base_url}/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        data = {"model": model, "messages": messages, **kwargs}
        resp = requests.post(url, json=data, headers=headers, timeout=60)
        resp.raise_for_status()
        return resp.json()
    
    def stream(self, messages: List[Dict], model: str = "claude-3-5-sonnet-20241022", **kwargs) -> Iterator:
        yield from []


class BedrockClient(AIClient):
    """AWS Bedrock."""
    
    def __init__(self, region: str = "us-east-1", credentials: Dict = None):
        self.region = region
        self.credentials = credentials or {}
    
    def chat(self, messages: List[Dict], model: str = "anthropic.claude-3-sonnet-20240229-v1:0", **kwargs) -> Dict:
        import boto3
        client = boto3.client("bedrock-runtime", region_name=self.region, **self.credentials)
        resp = client.converse(modelId=model, messages=messages, **kwargs)
        return resp
    
    def stream(self, messages: List[Dict], model: str = None, **kwargs) -> Iterator:
        yield from []


# === MODEL SELECTION ===

class ModelSelector:
    """Select best model based on requirements."""
    
    CAPABILITY_REQUIREMENTS = {
        "vision": ["gpt-4o", "claude-3-5-sonnet", "gemini-2.0-flash"],
        "thinking": ["gpt-4o", "claude-3-5-sonnet", "o1", "gemini-2.5-pro"],
        "fast": ["gpt-4o-mini", "claude-3-haiku"],
        "code": ["gpt-4o", "o1", "claude-3-5-sonnet"],
    }
    
    def select(self, required_capabilities: List[str]) -> str:
        for cap in required_capabilities:
            models = self.CAPABILITY_REQUIREMENTS.get(cap, [])
            if models:
                return models[0]
        return "gpt-4o"


model_selector = ModelSelector()
