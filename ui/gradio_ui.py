"""
Gradio UI Toolkit.

https://gradio.app/
"""

from typing import List, Dict, Optional


class GradioUI:
    """Gradio UI components."""
    
    @staticmethod
    def chat_interface(model: str = None):
        """Chat interface."""
        return {
            "type": "chat",
            "component": "gradio.ChatInterface",
            "model": model,
        }
    
    @staticmethod
    def textbox_component(label: str = "Input"):
        """Text input."""
        return {
            "type": "textbox",
            "component": "gradio.Textbox",
            "label": label,
        }
    
    @staticmethod
    def chatbot_component():
        """Chatbot display."""
        return {
            "type": "chatbot",
            "component": "gradio.Chatbot",
        }
    
    @staticmethod
    def button_component(label: str = "Submit"):
        """Button."""
        return {
            "type": "button",
            "component": "gradio.Button",
            "label": label,
        }
    
    @staticmethod
    def slider_component(min: float = 0, max: float = 1):
        """Slider."""
        return {
            "type": "slider",
            "component": "gradio.Slider",
            "minimum": min,
            "maximum": max,
        }
    
    @staticmethod
    def dropdown_component(choices: List[str]):
        """Dropdown."""
        return {
            "type": "dropdown",
            "component": "gradio.Dropdown",
            "choices": choices,
        }
    
    @staticmethod
    def file_component():
        """File upload."""
        return {
            "type": "file",
            "component": "gradio.File",
        }
    
    @staticmethod
    def image_component():
        """Image upload."""
        return {
            "type": "image",
            "component": "gradio.Image",
        }
    
    @staticmethod
    def audio_component():
        """Audio component."""
        return {
            "type": "audio",
            "component": "gradio.Audio",
        }
    
    @staticmethod
    def plot_component():
        """Plot/chart."""
        return {
            "type": "plot",
            "component": "gradio.Plot",
        }
