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


# === LOCAL / CUSTOM LLM SUPPORT ===

class LocalLLMClient(AIClient):
    """Local/custom LLM (Ollama, LM Studio, llama.cpp, etc.)."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
    
    def _headers(self) -> Dict:
        return {"Content-Type": "application/json"}
    
    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Dict:
        """Ollama /local chat."""
        import requests
        model = model or self.model
        url = f"{self.base_url}/api/chat"
        data = {"model": model, "messages": messages, **kwargs}
        resp = requests.post(url, json=data, timeout=120)
        resp.raise_for_status()
        return resp.json()
    
    def stream(self, messages: List[Dict], model: str = None, **kwargs) -> Iterator:
        """Streaming."""
        import requests
        model = model or self.model
        url = f"{self.base_url}/api/chat"
        data = {"model": model, "messages": messages, "stream": True, **kwargs}
        resp = requests.post(url, json=data, stream=True, timeout=120)
        for line in resp.iter_lines():
            if line:
                yield line.decode("utf-8")
    
    def list_models(self) -> List[str]:
        """List available models."""
        import requests
        url = f"{self.base_url}/api/tags"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return [m["name"] for m in data.get("models", [])]


class LMStudioClient(LocalLLMClient):
    """LM Studio client."""
    
    def __init__(self, base_url: str = "http://localhost:1234", model: str = None):
        super().__init__(base_url, model)
    
    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Dict:
        """LM Studio v1 chat."""
        import requests
        model = model or self.model
        url = f"{self.base_url}/v1/chat/completions"
        data = {"model": model, "messages": messages, **kwargs}
        resp = requests.post(url, json=data, timeout=120)
        resp.raise_for_status()
        return resp.json()


class OllamaClient(LocalLLMClient):
    """Ollama client."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        super().__init__(base_url, model)
    
    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Dict:
        """Ollama chat."""
        import requests
        model = model or self.model
        url = f"{self.base_url}/api/chat"
        data = {"model": model, "messages": messages, **kwargs}
        resp = requests.post(url, json=data, timeout=120)
        resp.raise_for_status()
        return resp.json()
    
    def pull(self, model: str):
        """Pull a model."""
        import requests
        url = f"{self.base_url}/api/pull"
        resp = requests.post(url, json={"name": model}, stream=True)
        for line in resp.iter_lines():
            print(line.decode("utf-8"))


class VLLMClient(AIClient):
    """vLLM server client."""
    
    def __init__(self, base_url: str = "http://localhost:8000", model: str = None):
        self.base_url = base_url
        self.model = model
    
    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Dict:
        """vLLM chat."""
        import requests
        model = model or self.model
        url = f"{self.base_url}/v1/chat/completions"
        data = {"model": model, "messages": messages, **kwargs}
        resp = requests.post(url, json=data, timeout=120)
        resp.raise_for_status()
        return resp.json()
    
    def stream(self, messages: List[Dict], model: str = None, **kwargs) -> Iterator:
        """Streaming vLLM."""
        import requests
        model = model or self.model
        url = f"{self.base_url}/v1/chat/completions"
        data = {"model": model, "messages": messages, "stream": True, **kwargs}
        resp = requests.post(url, json=data, stream=True, timeout=120)
        for line in resp.iter_lines():
            if line:
                yield line.decode("utf-8")


# Updated factory to include local
def create_client(provider: str, config: Dict) -> AIClient:
    """Create AI client - updated."""
    
    provider = provider.lower()
    
    if provider == "openai":
        return OpenAIClient(config["provider_api_key"], config.get("provider_base_url"))
    
    elif provider == "anthropic":
        return AnthropicClient(config["provider_api_key"], config.get("provider_base_url"))
    
    elif provider == "google":
        return GoogleClient(config["provider_api_key"], config.get("provider_base_url"))
    
    elif provider == "azure":
        return AzureOpenAIClient(
            config["provider_api_key"],
            config["provider_base_url"],
            config.get("api_version", "2024-02-01")
        )
    
    elif provider == "bedrock":
        return BedrockClient(
            config.get("aws_region", "us-east-1"),
            credentials={
                "aws_access_key_id": config.get("aws_access_key_id"),
                "aws_secret_access_key": config.get("aws_secret_access_key"),
            }
        )
    
    # Local / Custom
    elif provider == "ollama":
        return OllamaClient(
            base_url=config.get("provider_base_url", "http://localhost:11434"),
            model=config.get("model", "llama3")
        )
    
    elif provider == "lmstudio":
        return LMStudioClient(
            base_url=config.get("provider_base_url", "http://localhost:1234"),
            model=config.get("model")
        )
    
    elif provider == "vllm":
        return VLLMClient(
            base_url=config.get("provider_base_url", "http://localhost:8000"),
            model=config.get("model")
        )
    
    elif provider == "local":
        return LocalLLMClient(
            base_url=config.get("provider_base_url", "http://localhost:11434"),
            model=config.get("model", "llama2")
        )
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


# === CUSTOM PROVIDER / CUSTOM LLM ===

class CustomLLMClient(AIClient):
    """Custom LLM - user-defined provider."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.base_url = config.get("provider_base_url")
        self.model = config.get("model")
        self.api_key = config.get("provider_api_key")
        self.extra_headers = config.get("extra_headers", {})
        
        # Custom request/response handlers
        self.request_transformer = config.get("request_transformer")
        self.response_transformer = config.get("response_transformer")
    
    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Dict:
        """Custom chat with transformer hooks."""
        import requests
        model = model or self.model
        
        # Build request
        data = {"model": model, "messages": messages, **kwargs}
        
        # Transform request if provided
        if self.request_transformer:
            data = self.request_transformer(data)
        
        # Headers
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        headers.update(self.extra_headers)
        
        # Call API
        resp = requests.post(self.base_url, json=data, headers=headers, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        
        # Transform response if provided
        if self.response_transformer:
            result = self.response_transformer(result)
        
        return result
    
    def stream(self, messages: List[Dict], model: str = None, **kwargs) -> Iterator:
        """Streaming."""
        import requests
        model = model or self.model
        data = {"model": model, "messages": messages, "stream": True, **kwargs}
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        headers.update(self.extra_headers)
        
        resp = requests.post(self.base_url, json=data, headers=headers, stream=True, timeout=60)
        for line in resp.iter_lines():
            if line:
                yield line.decode("utf-8")


class CustomProviderRegistry:
    """Registry for custom providers."""
    
    def __init__(self):
        self._providers = {}
        self._auth = {}
    
    def register(self, name: str, config: Dict):
        """Register custom provider."""
        self._providers[name] = config
    
    def get(self, name: str) -> Optional[Dict]:
        """Get provider config."""
        return self._providers.get(name)
    
    def list(self) -> List[str]:
        """List providers."""
        return list(self._providers.keys())
    
    def register_auth(self, name: str, auth_config: Dict):
        """Register auth for provider."""
        self._auth[name] = auth_config
    
    def get_auth(self, name: str) -> Optional[Dict]:
        """Get auth config."""
        return self._auth.get(name)


class CustomModelRegistry:
    """Registry for custom models."""
    
    def __init__(self):
        self._models = {}
    
    def register(self, model_name: str, model_config: Dict):
        """Register custom model."""
        self._models[model_name] = model_config
    
    def get(self, model_name: str) -> Optional[Dict]:
        """Get model config."""
        return self._models.get(model_name)
    
    def list(self) -> List[str]:
        """List models."""
        return list(self._models.keys())


# Global registries
custom_provider_registry = CustomProviderRegistry()
custom_model_registry = CustomModelRegistry()


# Updated factory
def create_client(provider: str, config: Dict) -> AIClient:
    """Create AI client - with custom support."""
    
    p = provider.lower()
    
    if p == "openai":
        return OpenAIClient(config.get("provider_api_key"), config.get("provider_base_url"))
    if p == "anthropic":
        return AnthropicClient(config.get("provider_api_key"), config.get("provider_base_url"))
    if p == "google":
        return GoogleClient(config.get("provider_api_key"), config.get("provider_base_url"))
    if p == "azure":
        return AzureOpenAIClient(config["provider_api_key"], config["provider_base_url"], config.get("api_version"))
    if p == "bedrock":
        return BedrockClient(config.get("aws_region"), config.get("credentials"))
    if p == "ollama":
        return OllamaClient(config.get("provider_base_url"), config.get("model"))
    if p == "lmstudio":
        return LMStudioClient(config.get("provider_base_url"), config.get("model"))
    if p == "vllm":
        return VLLMClient(config.get("provider_base_url"), config.get("model"))
    if p == "local":
        return LocalLLMClient(config.get("provider_base_url"), config.get("model"))
    
    # Custom provider
    if p == "custom":
        return CustomLLMClient(config)
    
    # Check custom registry
    custom = custom_provider_registry.get(p)
    if custom:
        return CustomLLMClient({**custom, **config})
    
    raise ValueError(f"Unknown provider: {provider}")
