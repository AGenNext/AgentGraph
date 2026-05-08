"""
Microsoft AI Studio UI Toolkit.

https://ai.azure.com/
"""

from typing import List, Dict, Optional


class MicrosoftUI:
    """Microsoft AI Studio UI components."""
    
    @staticmethod
    def chat_component(deployment: str = "gpt-4"):
        """Azure AI Studio chat."""
        return {
            "type": "chat",
            "deployment": deployment,
            "component": "microsoft_chat"
        }
    
    @staticmethod
    def azure_ai_agent_component(agent_id: str = None):
        """Azure AI Agent components."""
        return {
            "type": "agent",
            "agent_id": agent_id,
            "component": "microsoft_ai_agent"
        }
    
    @staticmethod
    def copilot_studio_component(copilot_id: str = None):
        """Copilot Studio component."""
        return {
            "type": "copilot",
            "copilot_id": copilot_id,
            "component": "microsoft_copilot"
        }


class AzureAIStudioUI:
    """Azure AI Studio specific."""
    
    @staticmethod
    def playground_component(model: str):
        """Model playground."""
        return {
            "type": "playground",
            "model": model,
            "component": "azure_playground"
        }
    
    @staticmethod
    def evaluation_component():
        """Evaluation component."""
        return {
            "type": "evaluation",
            "component": "azure_eval"
        }
    
    @staticmethod
    def foundry_component(project: str):
        """Foundry project."""
        return {
            "type": "foundry",
            "project": project,
            "component": "azure_foundry"
        }
