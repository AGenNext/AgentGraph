"""
AI Provider API Integration.

Real API clients for each provider.
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


class OpenAIClient(AIClient):
    """OpenAI API client."""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.openai.com/v1"
    
    def _headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def chat(self, messages: List[Dict], model: str = "gpt-4o", **kwargs) -> Dict:
        """Non-streaming chat."""
        import requests
        url = f"{self.base_url}/chat/completions"
        data = {"model": model, "messages": messages, **kwargs}
        resp = requests.post(url, json=data, headers=self._headers(), timeout=60)
        resp.raise_for_status()
        return resp.json()
    
    def stream(self, messages: List[Dict], model: str = "gpt-4o", **kwargs) -> Iterator:
        """Streaming chat."""
        import requests
        url = f"{self.base_url}/chat/completions"
        data = {"model": model, "messages": messages, "stream": True, **kwargs}
        resp = requests.post(url, json=data, headers=self._headers(), stream=True, timeout=60)
        for line in resp.iter_lines():
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    yield line[6:]


class AnthropicClient(AIClient):
    """Anthropic API client."""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.anthropic.com"
    
    def _headers(self) -> Dict:
        return {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
    
    def chat(self, messages: List[Dict], model: str = "claude-3-5-sonnet-20241022", **kwargs) -> Dict:
        """Anthropic messages API."""
        import requests
        url = f"{self.base_url}/v1/messages"
        data = {"model": model, "messages": messages, **kwargs}
        resp = requests.post(url, json=data, headers=self._headers(), timeout=60)
        resp.raise_for_status()
        return resp.json()
    
    def stream(self, messages: List[Dict], model: str = "claude-3-5-sonnet-20241022", **kwargs) -> Iterator:
        """Streaming."""
        import requests
        url = f"{self.base_url}/v1/messages"
        data = {"model": model, "messages": messages, "stream": True, **kwargs}
        resp = requests.post(url, json=data, headers=self._headers(), stream=True, timeout=60)
        for line in resp.iter_lines():
            if line:
                yield line.decode("utf-8")


class GoogleClient(AIClient):
    """Google Gemini API client."""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://generativelanguage.googleapis.com"
    
    def chat(self, messages: List[Dict], model: str = "gemini-2.0-flash", **kwargs) -> Dict:
        """Gemini generateContent."""
        import requests
        url = f"{self.base_url}/v1beta/models/{model}:generateContent?key={self.api_key}"
        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            contents.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [{"text": msg["content"]}]
            })
        data = {"contents": contents, **kwargs}
        resp = requests.post(url, json=data, timeout=60)
        resp.raise_for_status()
        return resp.json()
    
    def stream(self, messages: List[Dict], model: str = "gemini-2.0-flash", **kwargs) -> Iterator:
        """Streaming."""
        import requests
        url = f"{self.base_url}/v1beta/models/{model}:streamGenerateContent?key={self.api_key}"
        contents = []
        for msg in messages:
            contents.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})
        data = {"contents": contents, **kwargs}
        resp = requests.post(url, json=data, stream=True, timeout=60)
        for line in resp.iter_lines():
            if line:
                yield line.decode("utf-8")


class AzureOpenAIClient(AIClient):
    """Azure OpenAI client."""
    
    def __init__(self, api_key: str, endpoint: str, api_version: str = "2024-02-01"):
        self.api_key = api_key
        self.endpoint = endpoint  # https://resource.openai.azure.com
        self.api_version = api_version
    
    def _headers(self) -> Dict:
        return {
            "api-key": self.api_key,
            "Content-Type": "application/json",
        }
    
    def chat(self, messages: List[Dict], deployment_name: str = "gpt-4o", **kwargs) -> Dict:
        """Azure chat."""
        import requests
        url = f"{self.endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={self.api_version}"
        data = {"messages": messages, **kwargs}
        resp = requests.post(url, json=data, headers=self._headers(), timeout=60)
        resp.raise_for_status()
        return resp.json()


class BedrockClient(AIClient):
    """AWS Bedrock client."""
    
    def __init__(self, region: str = "us-east-1", credentials: Dict = None):
        self.region = region
        self.credentials = credentials or {}
    
    def chat(self, messages: List[Dict], model: str = "anthropic.claude-3-sonnet-20240229-v1:0", **kwargs) -> Dict:
        """Bedrock converse."""
        import boto3
        client = boto3.client("bedrock-runtime", region_name=self.region, **self.credentials)
        # Convert to Claude format
        system = [{"text": "You are a helpful assistant."}]
        resp = client.converse(
            modelId=model,
            messages=messages,
            system=system,
            **kwargs
        )
        return resp
    
    def stream(self, messages: List[Dict], model: str = "anthropic.claude-3-sonnet-20240229-v1:0", **kwargs) -> Iterator:
        """Streaming."""
        import boto3
        client = boto3.client("bedrock-runtime", region_name=self.region, **self.credentials)
        resp = client.converse_stream(
            modelId=model,
            messages=messages,
            **kwargs
        )
        for chunk in resp.get("stream"):
            yield chunk


# === FACTORY ===

def create_client(provider: str, config: Dict) -> AIClient:
    """Create AI client from config."""
    
    auth_method = config.get("auth_method", "api_key")
    
    if provider == "openai":
        return OpenAIClient(
            api_key=config["provider_api_key"],
            base_url=config.get("provider_base_url")
        )
    
    elif provider == "anthropic":
        return AnthropicClient(
            api_key=config["provider_api_key"],
            base_url=config.get("provider_base_url")
        )
    
    elif provider == "google":
        return GoogleClient(
            api_key=config["provider_api_key"],
            base_url=config.get("provider_base_url")
        )
    
    elif provider == "azure":
        return AzureOpenAIClient(
            api_key=config["provider_api_key"],
            endpoint=config["provider_base_url"],
            api_version=config.get("api_version", "2024-02-01")
        )
    
    elif provider == "bedrock":
        return BedrockClient(
            region=config.get("aws_region", "us-east-1"),
            credentials={
                "aws_access_key_id": config.get("aws_access_key_id"),
                "aws_secret_access_key": config.get("aws_secret_access_key"),
            }
        )
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


# === MODEL SELECTION ===

class ModelSelector:
    """Select best model based on requirements."""
    
    CAPABILITY_REQUIREMENTS = {
        "vision": ["gpt-4o", "claude-3-5-sonnet", "gemini-2.0-flash"],
        "thinking": ["gpt-4o", "claude-3-5-sonnet", "o1", "gemini-2.5-pro"],
        "fast": ["gpt-4o-mini", "claude-3-haiku", "groq-mixtral"],
        "code": ["gpt-4o", "o1", "claude-3-5-sonnet", "gemini-2.5-pro"],
        "math": ["o1", "o3-mini", "claude-3-opus"],
    }
    
    def select(self, required_capabilities: List[str], preferred_provider: str = None) -> str:
        """Select model based on required capabilities."""
        for cap in required_capabilities:
            models = self.CAPABILITY_REQUIREMENTS.get(cap, [])
            if models:
                return models[0]
        return "gpt-4o"


# === TOKEN MANAGEMENT ===

class TokenManager:
    """Manage tokens (rate limits, quotas)."""
    
    def __init__(self):
        self._tokens = {}  # provider -> token info
    
    def set_token(self, provider: str, token: str, expires_at: str = None):
        self._tokens[provider] = {"token": token, "expires_at": expires_at}
    
    def get_token(self, provider: str) -> Optional[str]:
        info = self._tokens.get(provider, {})
        return info.get("token")
    
    def is_expired(self, provider: str) -> bool:
        from datetime import datetime
        info = self._tokens.get(provider, {})
        if info.get("expires_at"):
            exp = datetime.fromisoformat(info["expires_at"])
            return datetime.now() > exp
        return False


# === BILLING ===

class BillingClient:
    """Billing/reporting client for providers."""
    
    def __init__(self, provider: str, config: Dict):
        self.provider = provider
        self.config = config
    
    def get_usage(self, start_date: str, end_date: str) -> Dict:
        """Get token usage for date range."""
        # Placeholder - real implementation per provider
        return {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_cost": 0.0,
            "requests": 0,
        }
    
    def get_quota(self) -> Dict:
        """Get quota limits."""
        return {
            "rpm": 500,  # requests per minute
            "tpm": 30000,  # tokens per minute
            "daily_limit": 1000000,
        }
    
    def get_costs(self, period: str = "monthly") -> Dict:
        """Get costs for period."""
        return {
            "total": 0.0,
            "by_model": {},
            "currency": "USD",
        }


# === REPORTING ===

class ReportingClient:
    """Usage reporting and analytics."""
    
    def __init__(self):
        self._logs = []
    
    def log_request(self, provider: str, model: str, tokens: int, latency_ms: float):
        self._logs.append({
            "timestamp": str(datetime.now()),
            "provider": provider,
            "model": model,
            "tokens": tokens,
            "latency_ms": latency_ms,
        })
    
    def get_report(self, start_date: str = None, end_date: str = None) -> Dict:
        """Generate usage report."""
        logs = self._logs
        if start_date:
            logs = [l for l in logs if l["timestamp"] >= start_date]
        if end_date:
            logs = [l for l in logs if l["timestamp"] <= end_date]
        
        total_tokens = sum(l["tokens"] for l in logs)
        avg_latency = sum(l["latency_ms"] for l in logs) / max(len(logs), 1)
        
        return {
            "total_requests": len(logs),
            "total_tokens": total_tokens,
            "avg_latency_ms": avg_latency,
            "by_provider": {},
        }


# === GLOBAL INSTANCES ===
model_selector = ModelSelector()
token_manager = TokenManager()
reporting_client = ReportingClient()
from datetime import datetime
