"""
Streamlit UI Toolkit.

https://streamlit.io/
"""

from typing import List, Dict


class StreamlitUI:
    """Streamlit UI components."""
    
    @staticmethod
    def chat_component():
        """Chat component."""
        return {"type": "chat", "component": "st.chat_message"}
    
    @staticmethod
    def text_input(label: str = "Input"):
        """Text input."""
        return {"type": "text_input", "component": "st.text_input", "label": label}
    
    @staticmethod
    def text_area(label: str = "Text"):
        """Text area."""
        return {"type": "text_area", "component": "st.text_area", "label": label}
    
    @staticmethod
    def button(label: str = "Submit"):
        """Button."""
        return {"type": "button", "component": "st.button", "label": label}
    
    @staticmethod
    def selectbox(label: str, choices: List[str]):
        """Selectbox."""
        return {"type": "selectbox", "component": "st.selectbox", "label": label, "choices": choices}
    
    @staticmethod
    def slider(label: str, min_value: float = 0, max_value: float = 100):
        """Slider."""
        return {"type": "slider", "component": "st.slider", "label": label, "min": min_value, "max": max_value}
    
    @staticmethod
    def file_uploader(label: str = "Upload"):
        """File uploader."""
        return {"type": "file_uploader", "component": "st.file_uploader", "label": label}
    
    @staticmethod
    def columns(count: int):
        """Columns."""
        return {"type": "columns", "component": "st.columns", "count": count}
