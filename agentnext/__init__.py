"""
AGenNext - Multi-Framework Agent Backend
Built with: LangGraph, OpenAI, Anthropic, Google ADK, AutoGen, CrewAI, LangChain, LlamaIndex
"""
from .a2a import A2AClient, AgentCard, Task, TaskStatus
from .agents import (
    BaseAgent,
    OpenAIAgent,
    LangGraphClient,
    LangChainAgent,
    CrewAIAgent,
    AutoGenAgent,
    GoogleAgent,
    MicrosoftAgent,
    LlamaIndexAgent,
)
from .ui import (
    GradioBuilder,
    create_chat,
    chat_ui,
    agent_card,
    config_form,
    metrics_dashboard,
    file_uploader,
    OpenAIBuilder,
    GoogleBuilder,
    MicrosoftBuilder,
    LangChainBuilder,
    LangGraphBuilder,
)
from .ui_framework import FrameworkSelector
from .ui_agents import (
    OpenAIUI,
    AnthropicUI,
    LangGraphUI,
    LangChainUI,
    GoogleUI,
    MicrosoftUI,
    CrewAIUI,
    LlamaIndexUI,
    SalesforceUI,
    AutoGenUI,
    SmolAgentsUI,
)
from .adk_ui import (
    ADKUI,
    ADKAgent,
    ADKSequentialAgent,
    ADKParallelAgent,
    ADKLoopAgent,
    ADKSession,
    ADKTool,
    ADKState,
    ADKArtifact,
    ADKMemory,
)
from .providers import get_provider

__version__ = "0.1.0"
__all__ = [
    # A2A Protocol
    "A2AClient",
    "AgentCard", 
    "Task",
    "TaskStatus",
    # Agents
    "BaseAgent",
    "OpenAIAgent",
    "LangGraphClient",
    "LangChainAgent",
    "CrewAIAgent",
    "AutoGenAgent",
    "GoogleAgent",
    "MicrosoftAgent",
    "LlamaIndexAgent",
    # UI
    "GradioBuilder",
    "create_chat",
    "chat_ui",
    "agent_card",
    "config_form",
    "metrics_dashboard",
    "file_uploader",
    "OpenAIBuilder",
    "GoogleBuilder",
    "MicrosoftBuilder",
    "LangChainBuilder",
    "LangGraphBuilder",
    # Providers
    "get_provider",
    # UI Frameworks
    "FrameworkSelector",
    "OpenAIUI",
    "AnthropicUI",
    "LangGraphUI",
    "LangChainUI",
    "GoogleUI",
    "MicrosoftUI",
    "CrewAIUI",
    "LlamaIndexUI",
    "SalesforceUI",
    "AutoGenUI",
    "SmolAgentsUI",
    # ADK
    "ADKUI",
    "ADKAgent",
    "ADKSequentialAgent",
    "ADKParallelAgent",
    "ADKLoopAgent",
    "ADKSession",
    "ADKTool",
    "ADKState",
    "ADKArtifact",
    "ADKMemory",
]