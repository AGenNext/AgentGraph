"""
AI Provider - ALL OpenAI-Compatible endpoints.

Every provider uses /v1/chat/completions format.
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


class LLMClient(AIClient):
    """
    OpenAI-compatible LLM client.
    Works with ANY /v1/chat/completions endpoint.
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


# === DEFAULT BASE URLs (if not provided) ===

PROVIDER_URLS = {
    "openai": "https://api.openai.com/v1",
    "azure": "https://your-resource.openai.azure.com",
    "anthropic": "https://api.anthropic.com/v1",  # OpenAI-compatible
    "google": "https://generativelanguage.googleapis.com/v1",
    "bedrock": "https://bedrock-runtime.your-region.amazonaws.com",
    "ollama": "http://localhost:11434/v1",
    "lmstudio": "http://localhost:1234/v1",
    "vllm": "http://localhost:8000/v1",
    "local": "http://localhost:11434/v1",
}


def create_client(provider: str, config: Dict) -> AIClient:
    """
    Create LLM client - base_url is ALL that's needed.
    
    Usage:
        client = create_client("openai", {"provider_api_key": "sk-..."})
        client = create_client("ollama", {"model": "llama3"})
        client = create_client("my-custom", {
            "provider_base_url": "https://my-llm.com/v1",
            "provider_api_key": "key",
        })
    """
    p = provider.lower()
    
    # Get base_url - from config or provider alias
    base_url = config.get("provider_base_url") or PROVIDER_URLS.get(p)
    if not base_url:
        raise ValueError(f"provider_base_url required")
    
    return LLMClient(
        base_url=base_url,
        api_key=config.get("provider_api_key"),
        model=config.get("model", p)
    )
