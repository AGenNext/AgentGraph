"""
Google AI Studio UI Toolkit.

https://aistudio.google.com/
"""

from typing import List, Dict, Optional


class GoogleUI:
    """Google AI Studio UI components."""
    
    @staticmethod
    def chat_component(model: str = "gemini-2.0-flash"):
        """Gemini chat."""
        return {
            "type": "chat",
            "model": model,
            "component": "google_chat"
        }
    
    @staticmethod
    def vision_component(model: str = "gemini-2.0-flash"):
        """Vision/image analysis."""
        return {
            "type": "vision",
            "model": model,
            "component": "google_vision"
        }
    
    @staticmethod
    def embedding_component(model: str = "text-embedding-004"):
        """Embedding component."""
        return {
            "type": "embeddings",
            "model": model,
            "component": "google_embeddings"
        }
    
    @staticmethod
    def grounded_generation_component():
        """Grounded generation (search)."""
        return {
            "type": "grounded",
            "component": "google_grounded"
        }
