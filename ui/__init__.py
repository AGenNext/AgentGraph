"""
UI Toolkits + Builders for every SDK.
"""

# Toolkits (component configs)
from .openai_ui import OpenAIUI
from .microsoft_ui import MicrosoftUI, AzureAIStudioUI
from .google_ui import GoogleUI
from .langchain_ui import LangChainUI, LangGraphUI
from .gradio_ui import GradioUI
from .streamlit_ui import StreamlitUI
from .salesforce_ui import SalesforceUI

# Builders (actual working code)
from .gradio_builder import GradioBuilder, create_chat
from .streamlit_builder import chat_ui, agent_card, config_form, metrics_dashboard, file_uploader
from .openai_builder import OpenAIBuilder
from .google_builder import GoogleBuilder
from .microsoft_builder import MicrosoftBuilder
from .langchain_builder import LangChainBuilder
from .langgraph_builder import LangGraphBuilder

__all__ = [
    # Toolkits
    "OpenAIUI",
    "MicrosoftUI", 
    "AzureAIStudioUI",
    "GoogleUI",
    "LangChainUI",
    "LangGraphUI",
    "GradioUI",
    "StreamlitUI",
    "SalesforceUI",
    # Builders
    "GradioBuilder",
    "create_chat",
    "chat_ui",
    "agent_card",
    "config_form",
    "metrics_dashboard",
    "file_uploader",
    # SDK Builders
    "OpenAIBuilder",
    "GoogleBuilder",
    "MicrosoftBuilder",
    "LangChainBuilder",
    "LangGraphBuilder",
]
