"""
OpenAI UI Toolkit.

https://platform.openai.com/docs/guides/fine-tuning
"""

from typing import List, Dict, Any, Optional


class OpenAIUI:
    """OpenAI UI components."""
    
    @staticmethod
    def chat_component(model: str = "gpt-4o", temperature: float = 0.7):
        """Chat component."""
        return {
            "type": "chat",
            "model": model,
            "temperature": temperature,
            "component": "openai_chat"
        }
    
    @staticmethod
    def fine_tuning_component(training_file: str):
        """Fine-tuning component."""
        return {
            "type": "fine_tuning",
            "training_file": training_file,
            "component": "openai_ft"
        }
    
    @staticmethod
    def assistant_component(assistant_id: str = None):
        """AI Assistant component."""
        return {
            "type": "assistant",
            "assistant_id": assistant_id,
            "component": "openai_assistant"
        }
    
    @staticmethod
    def embeddings_component(model: str = "text-embedding-3-small"):
        """Embeddings component."""
        return {
            "type": "embeddings",
            "model": model,
            "component": "openai_embeddings"
        }
