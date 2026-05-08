"""
AI Provider - Different APIs for different providers.

Built-in providers: proprietary APIs
Custom provider: OpenAI-compatible /v1/chat/completions
"""

from typing import List, Dict, Iterator


# === CUSTOM PROVIDER (OpenAI-compatible) ===

class CustomLLMClient:
    """Custom LLM - OpenAI-compatible /v1/chat/completions."""
    
    def __init__(self, base_url: str, api_key: str = None, model: str = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "empty"
        self.model = model
    
    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Dict:
        import requests
        url = f"{self.base_url}/v1/chat/completions"
        data = {"model": model or self.model, "messages": messages, **kwargs}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        resp = requests.post(url, json=data, headers=headers, timeout=120)
        resp.raise_for_status()
        return resp.json()


# === BUILT-IN PROVIDERS (proprietary APIs) ===

class OpenAIClient:
    """OpenAI API."""
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def chat(self, messages: List[Dict], model: str = "gpt-4o", **kwargs) -> Dict:
        import requests
        resp = requests.post("https://api.openai.com/v1/chat/completions", json={
            "model": model, "messages": messages, **kwargs
        }, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=60)
        resp.raise_for_status()
        return resp.json()


class AnthropicClient:
    """Anthropic API."""
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def chat(self, messages: List[Dict], model: str = "claude-3-5-sonnet-20241022", **kwargs) -> Dict:
        import requests
        resp = requests.post("https://api.anthropic.com/v1/messages", json={
            "model": model, "messages": messages, **kwargs
        }, headers={
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }, timeout=60)
        resp.raise_for_status()
        return resp.json()


class GoogleClient:
    """Google Gemini API."""
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def chat(self, messages: List[Dict], model: str = "gemini-2.0-flash", **kwargs) -> Dict:
        import requests
        # Convert to Gemini format
        contents = []
        for msg in messages:
            contents.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        resp = requests.post(url, json={"contents": contents, **kwargs}, timeout=60)
        resp.raise_for_status()
        return resp.json()


class AzureClient:
    """Azure OpenAI API."""
    def __init__(self, api_key: str, endpoint: str, api_version: str = "2024-02-01"):
        self.api_key = api_key
        self.endpoint = endpoint
        self.api_version = api_version
    
    def chat(self, messages: List[Dict], deployment: str = "gpt-4o", **kwargs) -> Dict:
        import requests
        url = f"{self.endpoint}/openai/deployments/{deployment}/chat/completions?api-version={self.api_version}"
        resp = requests.post(url, json={"messages": messages, **kwargs}, headers={"api-key": self.api_key}, timeout=60)
        resp.raise_for_status()
        return resp.json()


class BedrockClient:
    """AWS Bedrock API."""
    def __init__(self, region: str = "us-east-1", credentials: dict = None):
        self.region = region
        self.credentials = credentials or {}
    
    def chat(self, messages: List[Dict], model: str = "anthropic.claude-3-sonnet-20240229-v1:0", **kwargs) -> Dict:
        import boto3
        client = boto3.client("bedrock-runtime", region_name=self.region, **self.credentials)
        resp = client.converse(modelId=model, messages=messages, **kwargs)
        return resp


# === FACTORY ===

def create_client(provider: str, config: Dict):
    """Create client by provider name."""
    p = provider.lower()
    
    if p == "openai":
        return OpenAIClient(config["provider_api_key"])
    
    if p == "anthropic":
        return AnthropicClient(config["provider_api_key"])
    
    if p == "google":
        return GoogleClient(config["provider_api_key"])
    
    if p == "azure":
        return AzureClient(
            config["provider_api_key"],
            config["provider_base_url"],  # endpoint required
            config.get("api_version", "2024-02-01")
        )
    
    if p == "bedrock":
        return BedrockClient(
            config.get("aws_region", "us-east-1"),
            config.get("credentials", {})
        )
    
    # CUSTOM = OpenAI-compatible
    base_url = config.get("provider_base_url")
    if not base_url:
        raise ValueError("provider_base_url required for custom provider")
    
    return CustomLLMClient(
        base_url=base_url,
        api_key=config.get("provider_api_key"),
        model=config.get("model")
    )
