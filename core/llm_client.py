"""Flexible LLM Client that supports any OpenAI-compatible API."""

import os
from typing import Optional, Any, List
from dataclasses import dataclass, field


@dataclass
class LLMProvider:
    """Definition of an LLM provider with its attributes."""
    
    name: str
    display_name: str
    base_url: str = "https://api.openai.com/v1"
    api_key_env: str = "LLM_API_KEY"
    default_model: str = "gpt-4"
    api_version: Optional[str] = None  # e.g., "2024-02-01"
    supports_streaming: bool = True
    supports_vision: bool = False
    supports_function_calling: bool = False
    supports_json_output: bool = False
    max_tokens: int = 4096
    context_window: int = 128000
    tools: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


# All LLM Providers with full capabilities
PROVIDERS = {
    # === Major Cloud Providers ===
    "openai": LLMProvider(
        name="openai",
        display_name="OpenAI",
        base_url="https://api.openai.com/v1",
        api_key_env="OPENAI_API_KEY",
        default_model="gpt-4o",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=16384,
        context_window=128000,
        tools=["code_interpreter", "file_search", "web_search", "structured_output"],
        skills=["reasoning", "coding", "creative_writing", "analysis", "instruction_following"],
        tags=["general", "premium"],
    ),
    "anthropic": LLMProvider(
        name="anthropic",
        display_name="Anthropic Claude",
        base_url="https://api.anthropic.com/v1",
        api_key_env="ANTHROPIC_API_KEY",
        default_model="claude-sonnet-4-20250514",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=200000,
        tools=["computer_use", "web_search", "pdf_vision"],
        skills=["reasoning", "analysis", "long_form_writing", "constitutional_ai"],
        tags=["premium", "long_context"],
    ),
    "google": LLMProvider(
        name="google",
        display_name="Google Gemini",
        base_url="https://generativelanguage.googleapis.com/v1",
        api_key_env="GOOGLE_API_KEY",
        default_model="gemini-2.0-flash",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=1000000,
        tools=["code_execution", "google_search", "google_maps", "youtube", "google_ads"],
        skills=["research", "multimodal", "factual", "grounded_generation"],
        tags=["free", "multimodal"],
    ),
    "mistral": LLMProvider(
        name="mistral",
        display_name="Mistral AI",
        base_url="https://api.mistral.ai/v1",
        api_key_env="MISTRAL_API_KEY",
        default_model="mistral-large-latest",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=32768,
        context_window=128000,
        tools=["code_runner", "function_calling"],
        skills=["coding", "reasoning", "multilingual", "math"],
        tags=["coding", "fast"],
    ),
    "cohere": LLMProvider(
        name="cohere",
        display_name="Cohere",
        base_url="https://api.cohere.ai/v1",
        api_key_env="COHERE_API_KEY",
        default_model="command-r-plus",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=4096,
        context_window=128000,
        tools=["web_search", "code", "classification"],
        skills=["enterprise", "retrieval", "classification", "summarization"],
        tags=["enterprise", "rag"],
    ),
    # === AWS ===
    "bedrock": LLMProvider(
        name="bedrock",
        display_name="AWS Bedrock",
        base_url="https://bedrock.{region}.amazonaws.com/model invoke",
        api_key_env="AWS_ACCESS_KEY_ID",
        default_model="anthropic.claude-3-sonnet-20240229-v1:0",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=200000,
        tools=["bedrock_knowledge_base", "code_interpreter", "guardrails"],
        skills=["enterprise_reasoning", "secure_processing", "guardrails"],
        tags=["enterprise", "secure", "aws"],
    ),
    "bedrock克劳迪娅": LLMProvider(
        name="bedrock-claude",
        display_name="AWS Bedrock Claude",
        base_url="https://bedrock.{region}.amazonaws.com/model invoke",
        api_key_env="AWS_ACCESS_KEY_ID",
        default_model="anthropic.claude-3-5-sonnet-20241022-v2:0",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=True,
        max_tokens=8192,
        context_window=200000,
        tools=["bedrock_knowledge_base", "code_interpreter"],
        skills=["enterprise_reasoning", "secure"],
        tags=["aws", "claude"],
    ),
    "bedrock-llama": LLMProvider(
        name="bedrock-llama",
        display_name="AWS Bedrock Llama",
        base_url="https://bedrock.{region}.amazonaws.com/model invoke",
        api_key_env="AWS_ACCESS_KEY_ID",
        default_model="meta.llama3-3-70b-instruct-v1:0",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=8192,
        context_window=128000,
        tools=[],
        skills=["open_weights", "coding"],
        tags=["aws", "llama"],
    ),
    # === Azure ===
    "azure": LLMProvider(
        name="azure",
        display_name="Azure OpenAI",
        base_url="https://{resource}.openai.azure.com/openai/deployments/{model}",
        api_key_env="AZURE_OPENAI_KEY",
        default_model="gpt-4",
        api_version="2024-02-01",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=128000,
        tools=["content_safety"],
        skills=["enterprise", "secure", "compliance"],
        tags=["azure", "enterprise"],
    ),
    # === Local ===
    "ollama": LLMProvider(
        name="ollama",
        display_name="Ollama (Local)",
        base_url="http://localhost:1141/v1",
        api_key_env="",
        default_model="llama3",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=["code_runner"],
        skills=["local", "privacy_focused", "offline"],
        tags=["local", "privacy"],
    ),
    "lmstudio": LLMProvider(
        name="lmstudio",
        display_name="LM Studio (Local)",
        base_url="http://localhost:1234/v1",
        api_key_env="",
        default_model="local-model",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["local", "privacy_focused"],
        tags=["local", "gui"],
    ),
    "llamafile": LLMProvider(
        name="llamafile",
        display_name="Llamafile",
        base_url="http://localhost:8080/v1",
        api_key_env="",
        default_model="model",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["local", "single_file"],
        tags=["local"],
    ),
    "koboldcpp": LLMProvider(
        name="koboldcpp",
        display_name="KoboldCPP",
        base_url="http://localhost:5001/v1",
        api_key_env="",
        default_model="model",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["local", "gaming"],
        tags=["local"],
    ),
    "vllm": LLMProvider(
        name="vllm",
        display_name="vLLM",
        base_url="http://localhost:8001/v1",
        api_key_env="",
        default_model="meta-llama/Llama-2-70b-hf",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=True,
        max_tokens=4096,
        context_window=128000,
        tools=["tensor_parallel"],
        skills=["high_throughput", "serverless"],
        tags=["inference_server"],
    ),
    "text_generation_webui": LLMProvider(
        name="text_generation_webui",
        display_name="text-generation-webui",
        base_url="http://localhost:5000/v1",
        api_key_env="",
        default_model="model",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["local", "extensions"],
        tags=["local"],
    ),
    # === Chinese ===
    "qwen": LLMProvider(
        name="qwen",
        display_name="Alibaba Qwen",
        base_url="https://dashscope.aliyuncs.com/api/v1",
        api_key_env="DASHSCOPE_API_KEY",
        default_model="qwen-turbo",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=1000000,
        tools=["code_interpreter", "qwen_apps"],
        skills=["multilingual", "coding", "math", "cantonese"],
        tags=["chinese", "multilingual"],
    ),
    "qwen-max": LLMProvider(
        name="qwen-max",
        display_name="Alibaba Qwen Max",
        base_url="https://dashscope.aliyuncs.com/api/v1",
        api_key_env="DASHSCOPE_API_KEY",
        default_model="qwen-max",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=128000,
        tools=["code_interpreter"],
        skills=["reasoning", "coding", "multilingual"],
        tags=["chinese", "premium"],
    ),
    "moonshot": LLMProvider(
        name="moonshot",
        display_name="Moonshot AI",
        base_url="https://api.moonshot.cn/v1",
        api_key_env="MOONSHOT_API_KEY",
        default_model="moonshot-v1-8k-chat",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=128000,
        tools=[],
        skills=["coding", "chinese", "reasoning"],
        tags=["chinese", "startup"],
    ),
    "minimax": LLMProvider(
        name="minimax",
        display_name="MiniMax",
        base_url="https://api.minimax.chat/v1",
        api_key_env="MINIMAX_API_KEY",
        default_model="abab6.5s-chat",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=245760,
        tools=[],
        skills=["multilingual", "long_context", "translation"],
        tags=["chinese", "long_context"],
    ),
    "deepseek": LLMProvider(
        name="deepseek",
        display_name="DeepSeek",
        base_url="https://api.deepseek.com/v1",
        api_key_env="DEEPSEEK_API_KEY",
        default_model="deepseek-chat",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=128000,
        tools=["deepseek_coder"],
        skills=["coding", "reasoning", "math", "成本效益"],
        tags=["coding", "affordable"],
    ),
    "01ai": LLMProvider(
        name="01ai",
        display_name="01.AI",
        base_url="https://api.01.ai/v1",
        api_key_env="ZEROONE_API_KEY",
        default_model="yi-large",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["coding", "english_chinese", "translation"],
        tags=["chinese", "open_weights"],
    ),
    # === Specialized ===
    "groq": LLMProvider(
        name="groq",
        display_name="Groq",
        base_url="https://api.groq.com/openai/v1",
        api_key_env="GROQ_API_KEY",
        default_model="llama-3.1-70b-versatile",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=128000,
        tools=["logprobs"],
        skills=["ultra_low_latency", "fast_inference", "meta_luama"],
        tags=["fast", "low_latency"],
    ),
    "perplexity": LLMProvider(
        name="perplexity",
        display_name="Perplexity AI",
        base_url="https://api.perplexity.ai/",
        api_key_env="PERPLEXITY_API_KEY",
        default_model="llama-3.1-sonar-large-128k-chat",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=128000,
        tools=["web_search", "research", "citations", "focus"],
        skills=["research", "web_search", "citations", "factual"],
        tags=["research", "search"],
    ),
    "together": LLMProvider(
        name="together",
        display_name="Together AI",
        base_url="https://api.together.xyz/v1",
        api_key_env="TOGETHER_API_KEY",
        default_model="meta-llama/Llama-3-70b-hf",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=128000,
        tools=["fine_tuning", "inference"],
        skills=["fine_tuning", "inference", "model_blending"],
        tags=["inference", "fine_tuning"],
    ),
    "fireworks": LLMProvider(
        name="fireworks",
        display_name="Fireworks AI",
        base_url="https://api.fireworks.ai/v1",
        api_key_env="FIREWORKS_API_KEY",
        default_model="accounts/fireworks/models/llama-3-70b",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=128000,
        tools=["function_calling"],
        skills=["fast_inference", "function_calling", "quality"],
        tags=["fast", "inference"],
    ),
    "anyscale": LLMProvider(
        name="anyscale",
        display_name="Anyscale Endpoints",
        base_url="https://api.endpoints.anyscale.com/v1",
        api_key_env="ANYSCALE_API_KEY",
        default_model="meta-llama/Llama-3-70b-chat",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["serverless", "cost_effective"],
        tags=["serverless"],
    ),
    "deepinfra": LLMProvider(
        name="deepinfra",
        display_name="DeepInfra",
        base_url="https://api.deepinfra.com/v1",
        api_key_env="DEEPINFRA_API_KEY",
        default_model="meta-llama/Llama-3-70b-instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=128000,
        tools=[],
        skills=["serverless", "inference", "competitive_pricing"],
        tags=["inference", "affordable"],
    ),
    # === NVIDIA & Enterprise ===
    "nvidia": LLMProvider(
        name="nvidia",
        display_name="NVIDIA NIM",
        base_url="https://integrate.api.nvidia.com/v1",
        api_key_env="NVIDIA_API_KEY",
        default_model="meta/llama-3.1-70b-instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=128000,
        tools=["nemo", "rag", "nmc"],
        skills=["gpu_accelerated", "enterprise", "secure"],
        tags=["enterprise", "gpu"],
    ),
    "vertex": LLMProvider(
        name="vertex",
        display_name="Google Vertex AI",
        base_url="https://{region}-aiplatform.googleapis.com/v1",
        api_key_env="GOOGLE_APPLICATION_CREDENTIALS",
        default_model="gemini-1.5-pro",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=2000000,
        tools=["vertex_search", "code_execution", "grounding", "speech"],
        skills=["enterprise", "secure_ml", "grounded_generation", "admin_control"],
        tags=["enterprise", "google_cloud"],
    ),
    "watsonx": LLMProvider(
        name="watsonx",
        display_name="IBM watsonx",
        base_url="https://{region}.ml.{domain}/ml/v4",
        api_key_env="WATSONX_API_KEY",
        default_model="ibm/granite-34b-code-instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=128000,
        tools=["watsonx_discovery", "rag", "watsonx_governance"],
        skills=["enterprise", "governance", "industry_specific", "compliance"],
        tags=["enterprise", "ibm"],
    ),
    # === More Providers ===
    "sambanova": LLMProvider(
        name="sambanova",
        display_name="SambaNova",
        base_url="https://api.sambanova.ai/v1",
        api_key_env="SAMBANOVA_API_KEY",
        default_model="Meta-Llama-3-70B-Instruct-AB",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=8192,
        context_window=128000,
        tools=[],
        skills=["fast_inference", "expert", "enterprise"],
        tags=["enterprise", "fast"],
    ),
    "novita": LLMProvider(
        name="novita",
        display_name="Novita AI",
        base_url="https://api.novita.ai/v3",
        api_key_env="NOVITA_API_KEY",
        default_model="meta-llama-3-70b-instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=128000,
        tools=["fine_tuning", "lora"],
        skills=["inference", "fine_tuning", "model_training"],
        tags=["inference", "fine_tuning"],
    ),
    "hyperbolic": LLMProvider(
        name="hyperbolic",
        display_name="Hyperbolic",
        base_url="https://api.hyperbolic.xyz/v1",
        api_key_env="HYPERBOLIC_API_KEY",
        default_model="meta-llama/Llama-3.1-70b-instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=128000,
        tools=[],
        skills=["serverless", "cost_effective", "diverse_models"],
        tags=["affordable", "inference"],
    ),
    "neptune": LLMProvider(
        name="neptune",
        display_name="Neptune.ai",
        base_url="https://api.neptune.ai/v1",
        api_key_env="NEPTUNE_API_KEY",
        default_model="Llama-3-70B-Instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=4096,
        context_window=128000,
        tools=["ml_tracking", "experiment_tracking"],
        skills=["model_tracking", "experiments", "mlops"],
        tags=["mlops", "tracking"],
    ),
    "volcengine": LLMProvider(
        name="volcengine",
        display_name="ByteDance Volcengine",
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key_env="VOLCENGINE_API_KEY",
        default_model="doubao-pro-32k",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=32000,
        tools=[],
        skills=["fast_inference", "low_latency", "cost_effective"],
        tags=["fast", "bytedance"],
    ),
    # === Custom/Open ===
    "custom": LLMProvider(
        name="custom",
        display_name="Custom Endpoint",
        base_url="https://api.openai.com/v1",
        api_key_env="CUSTOM_API_KEY",
        default_model="custom-model",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=[],
        tags=["custom", "user_defined"],
    ),
    
    # === Hugging Face ===
    "huggingface": LLMProvider(
        name="huggingface",
        display_name="Hugging Face Inference API",
        base_url="https://api-inference.huggingface.co/v1",
        api_key_env="HF_API_KEY",
        default_model="meta-llama/Meta-Llama-3-70B-Instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=4096,
        context_window=128000,
        tools=["zero_shot", "text_classification", "token_classification"],
        skills=["zero_shot", "text_classification", "named_entity_recognition", "question_answering", "summarization", "translation", "text_generation"],
        tags=["open_source", "inference", "nlp"],
    ),
    "huggingface_endpoint": LLMProvider(
        name="huggingface_endpoint",
        display_name="Hugging Face Inference Endpoints",
        base_url="https://{endpoint}.inference.huggingface.cloud/v1",
        api_key_env="HF_API_KEY",
        default_model="meta-llama/Meta-Llama-3-70B-Instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["text_generation", "custom_pipeline"],
        tags=["self_hosted", "inference"],
    ),
    
    # === Additional Providers ===
    "xai": LLMProvider(
        name="xai",
        display_name="X.AI Grok",
        base_url="https://api.x.ai/v1",
        api_key_env="XAI_API_KEY",
        default_model="grok-2-1212",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=False,
        supports_json_output=False,
        max_tokens=8192,
        context_window=131072,
        tools=[],
        skills=["reasoning", "humor", "real_time_data"],
        tags=["reasoning", "xai"],
    ),
    "lepton": LLMProvider(
        name="lepton",
        display_name="Lepton AI",
        base_url="https://api.lepton.ai/v1",
        api_key_env="LEPTON_API_KEY",
        default_model="llama3-70b",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["search_augmented"],
        tags=["search", "fast"],
    ),
    "openrouter": LLMProvider(
        name="openrouter",
        display_name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        api_key_env="OPENROUTER_API_KEY",
        default_model="anthropic/claude-3.5-sonnet",
        supports_streaming=True,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_output=True,
        max_tokens=4096,
        context_window=200000,
        tools=["route_selection"],
        skills=["multi_model", "route_selection"],
        tags=["aggregator", "multi_provider"],
    ),
    "cloudflare": LLMProvider(
        name="cloudflare",
        display_name="Cloudflare Workers AI",
        base_url="https://workers.ai/v1",
        api_key_env="CF_API_KEY",
        default_model="@cf/meta/llama-3.1-70b-instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["fast", "edge_computing"],
        tags=["edge", "fast"],
    ),
    "replicate": LLMProvider(
        name="replicate",
        display_name="Replicate",
        base_url="https://api.replicate.com/v1",
        api_key_env="REPLICATE_API_KEY",
        default_model="meta/llama-3-70b-instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["custom_models", "fine_tuning"],
        tags=["model_deployment", "fine_tuning"],
    ),
    "jina": LLMProvider(
        name="jina",
        display_name="Jina AI",
        base_url="https://api.jina.ai/v1",
        api_key_env="JINA_API_KEY",
        default_model="jinaai/jina-2",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_output=True,
        max_tokens=4096,
        context_window=128000,
        tools=["jina_reader"],
        skills=["reading", "extraction"],
        tags=["reader", "extraction"],
    ),
    "predibase": LLMProvider(
        name="predibase",
        display_name="Predibase",
        base_url="https://serve.predibase.com/v1",
        api_key_env="PREDIBASE_API_KEY",
        default_model="llama-3-70b",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["fine_tuned", "custom_models"],
        tags=["fine_tuning", "custom"],
    ),
    "fal": LLMProvider(
        name="fal",
        display_name="Fal.ai",
        base_url="https://queue.fal.services/fal-ai/v1",
        api_key_env="FAL_API_KEY",
        default_model="Llama-3.1-70B-Instruct",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["async", "image_generation"],
        tags=["async", "image"],
    ),
    "wordware": LLMProvider(
        name="wordware",
        display_name="Wordware",
        base_url="https://api.wordware.ai/v1",
        api_key_env="WORDWARE_API_KEY",
        default_model="gpt-4",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["character_ai", "persona"],
        tags=["character", "persona"],
    ),
    "abacus": LLMProvider(
        name="abacus",
        display_name="Abacus AI",
        base_url="https://api.abacus.ai/v1",
        api_key_env="ABACUS_API_KEY",
        default_model="sonnet-4",
        supports_streaming=True,
        supports_vision=False,
        supports_function_calling=False,
        max_tokens=4096,
        context_window=128000,
        tools=[],
        skills=["enterprise", "sftp"],
        tags=["enterprise"],
    ),
}


@dataclass
class LLMConfig:
    """Configuration for any LLM."""
    
    provider: str = "openai"
    api_key: Optional[str] = None
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 1.0
    
    # Provider-defined attributes
    tools: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    supports_streaming: bool = True
    supports_vision: bool = False
    context_window: int = 128000
    
    @classmethod
    def from_env(cls, provider: Optional[str] = None) -> "LLMConfig":
        """Create config from environment variables."""
        # Auto-detect provider
        if provider is None:
            provider = cls._detect_provider()
        
        provider_def = PROVIDERS.get(provider, PROVIDERS["openai"])
        
        # Get API key from provider's env var
        api_key = os.getenv(provider_def.api_key_env) or os.getenv("LLM_API_KEY")
        
        # Get base URL
        base_url = os.getenv("LLM_BASE_URL", provider_def.base_url)
        
        # Get model
        model = os.getenv("LLM_MODEL", provider_def.default_model)
        
        return cls(
            provider=provider,
            api_key=api_key,
            base_url=base_url,
            model=model,
            tools=provider_def.tools,
            skills=provider_def.skills,
            supports_streaming=provider_def.supports_streaming,
            supports_vision=provider_def.supports_vision,
            context_window=provider_def.context_window,
            max_tokens=provider_def.max_tokens,
        )
    
    @staticmethod
    def _detect_provider() -> str:
        """Auto-detect which LLM provider to use."""
        # Check environment variables in order
        if os.getenv("OPENAI_API_KEY"):
            return "openai"
        if os.getenv("ANTHROPIC_API_KEY"):
            return "anthropic"
        if os.getenv("GOOGLE_API_KEY"):
            return "google"
        if os.getenv("MISTRAL_API_KEY"):
            return "mistral"
        if os.getenv("COHERE_API_KEY"):
            return "cohere"
        if os.getenv("AWS_ACCESS_KEY_ID"):
            return "bedrock"
        if os.getenv("OLLAMA_HOST"):
            return "ollama"
        if os.getenv("LMSTUDIO_HOST"):
            return "lmstudio"
        return "openai"


class LLMClient:
    """Universal LLM client that works with any OpenAI-compatible API."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig.from_env()
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                kwargs = {"api_key": self.config.api_key, "base_url": self.config.base_url}
                kwargs = {k: v for k, v in kwargs.items() if v}
                self._client = OpenAI(**kwargs)
            except ImportError:
                self._client = None
        return self._client
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        client = self._get_client()
        if client:
            try:
                response = client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        *([{"role": "system", "content": system_prompt}] if system_prompt else []),
                        {"role": "user", "content": prompt}
                    ],
                    temperature=kwargs.get("temperature", self.config.temperature),
                    max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                    stream=False,
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"Error: {str(e)}"
        return f"[{self.config.provider}:{self.config.model}] {prompt[:50]}..."
    
    def generate_stream(self, prompt: str, system_prompt: Optional[str] = None):
        client = self._get_client()
        if client:
            try:
                response = client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        *([{"role": "system", "content": system_prompt}] if system_prompt else []),
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                    stream=True,
                )
                for chunk in response:
                    if chunk.choices:
                        delta = chunk.choices[0].delta
                        if delta.content:
                            yield delta.content
            except Exception as e:
                yield f"Error: {str(e)}"
        else:
            yield f"[No client]"
    
    @property
    def is_available(self) -> bool:
        return self._get_client() is not None and self.config.api_key is not None
    
    def __repr__(self):
        return f"<LLMClient {self.config.provider}/{self.config.model}>"


def create_llm_client(provider: str = "openai", **kwargs) -> LLMClient:
    """Factory to create an LLM client with provider defaults."""
    config = LLMConfig.from_env(provider)
    for k, v in kwargs.items():
        setattr(config, k, v)
    return LLMClient(config)


def get_provider_info(provider: str) -> Optional[LLMProvider]:
    """Get provider definition."""
    return PROVIDERS.get(provider)


def list_providers() -> dict:
    """List all available providers."""
    return PROVIDERS.copy()