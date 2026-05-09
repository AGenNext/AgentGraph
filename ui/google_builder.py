"""
Google SDK UI Builder.
"""

import gradio as gr
from typing import Callable


class GoogleBuilder:
    """Build Google Gemini agent UIs."""
    
    def __init__(self, agent_fn: Callable):
        self.agent_fn = agent_fn
    
    def chat(self):
        """Chat interface."""
        return gr.ChatInterface(fn=self.agent_fn, title="Gemini Agent")
    
    def vision(self):
        """Vision analysis."""
        with gr.Blocks() as demo:
            gr.Markdown("# Gemini Vision")
            img = gr.Image(type="pil", label="Image")
            prompt = gr.Textbox(label="What to analyze")
            analyze = gr.Button("Analyze")
            output = gr.Textbox(lines=5)
            analyze.click(self.agent_fn, [img, prompt], output)
        return demo
    
    def grounded(self):
        """Grounded generation (with search)."""
        with gr.Blocks() as demo:
            gr.Markdown("# Grounded Generation")
            msg = gr.Textbox(label="Query")
            use_search = gr.Checkbox(label="Use search", value=True)
            search_btn = gr.Button("Search")
            output = gr.JSON()
            search_btn.click(self.agent_fn, [msg, use_search], output)
        return demo
    
    def gemini_api(self):
        """Gemini API playground."""
        with gr.Blocks() as demo:
            gr.Markdown("# Gemini API")
            gr.Dropdown(["gemini-2.0-flash", "gemini-2.5-pro"], label="Model")
            msg = gr.Textbox(label="Prompt", lines=3)
            temp = gr.Slider(0, 1, 0.9, label="Temperature")
            gr.Button("Generate")
            output = gr.Textbox(lines=5)
        return demo
