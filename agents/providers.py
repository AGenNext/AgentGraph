"""
AI Provider - Simple OpenAI-compatible endpoints.

Just provide base_url and API key - no transformations needed.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Iterator


class AIClient(ABC):
    """Base AI Client."""
    
    @abstractmethod
    def chat(self, messages: List[Dict], model: str, **kwargs) -> Dict:
        pass
    
    @abstractmethod
    def stream(self, messages: List[Dict], model: str, **kwargs) -> Iterator:
        pass


# === THE CLIENT ===

class LLMClient(AIClient):
    """
    OpenAI-compatible LLM client.
    Just provide base_url - works with any /v1/chat/completions endpoint.
    """
    
    def __init__(self, base_url: str, api_key: str = None, model: str = "default"):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "empty"
        self.model = model
    
    def _headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Dict:
        """Call /v1/chat/completions."""
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
        """List models at endpoint."""
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

PROVIDER_URLS = {
    "openai": "https://api.openai.com/v1",
    "anthropic": "https://api.anthropic.com",  # Exception (different API)
    "google": "https://generativelanguage.googleapis.com",
    "azure": None,  # Custom
    "bedrock": None,  # AWS-specific
    "ollama": "http://localhost:11434",
    "lmstudio": "http://localhost:1234",
    "vllm": "http://localhost:8000",
    "local": "http://localhost:11434",
}


def create_client(provider: str, config: Dict) -> AIClient:
    """
    Create LLM client - just needs base_url.
    
    Usage:
        client = create_client("openai", {"provider_api_key": "sk-..."})
        
        # Or any OpenAI-compatible:
        client = create_client("custom", {
            "provider_base_url": "https://my-llm.com/v1",
            "provider_api_key": "key",
            "model": "my-model",
        })
    """
    p = provider.lower()
    
    # Exceptions
    if p == "anthropic":
        return AnthropicClient(config.get("provider_api_key"))
    if p == "bedrock":
        return BedrockClient(config.get("aws_region"))
    
    # Get base_url
    base_url = config.get("provider_base_url") or PROVIDER_URLS.get(p)
    if not base_url:
        raise ValueError(f"base_url required for: {provider}")
    
    return LLMClient(
        base_url=base_url,
        api_key=config.get("provider_api_key"),
        model=config.get("model", p)
    )


# === EXCEPTIONS ===

class AnthropicClient(AIClient):
    """Anthropic - different API."""
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def chat(self, messages: List[Dict], model: str = "claude-3-5-sonnet-20241022", **kwargs) -> Dict:
        import requests
        url = "https://api.anthropic.com/v1/messages"
        resp = requests.post(url, json={
            "model": model, "messages": messages, **kwargs
        }, headers={
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }, timeout=60)
        resp.raise_for_status()
        return resp.json()
    def stream(self, messages, model, **kwargs):
        yield from []


class BedrockClient(AIClient):
    """AWS Bedrock."""
    def __init__(self, region: str = "us-east-1"):
        self.region = region
    
    def chat(self, messages: List[Dict], model: str = "anthropic.claude-3-sonnet-20240229-v1:0", **kwargs) -> Dict:
        import boto3
        client = boto3.client("bedrock-runtime", region_name=self.region)
        return client.converse(modelId=model, messages=messages, **kwargs)
    def stream(self, messages, model, **kwargs):
        yield from []


model_selector = None  # Keep simple
