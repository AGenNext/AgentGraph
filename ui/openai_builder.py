"""
OpenAI SDK UI Builder.
"""

import gradio as gr
from typing import Callable, Optional


class OpenAIBuilder:
    """Build OpenAI agent UIs."""
    
    def __init__(self, agent_fn: Callable):
        self.agent_fn = agent_fn
    
    def chat(self):
        """Chat interface."""
        return gr.ChatInterface(fn=self.agent_fn, title="OpenAI Agent")
    
    def playground(self, models: list = None):
        """Model playground."""
        models = models or ["gpt-4o", "gpt-4o-mini", "o1"]
        
        with gr.Blocks() as demo:
            gr.Markdown("# OpenAI Playground")
            
            with gr.Row():
                model = gr.Dropdown(models, label="Model")
                temp = gr.Slider(0, 2, 0.7, label="Temperature")
            
            msg = gr.Textbox(label="Message", lines=3)
            submit = gr.Button("Send")
            output = gr.Chatbot()
            
            def run(msg, model):
                return self.agent_fn(msg, model)
            
            submit.click(run, [msg, model], output)
        
        return demo
    
    def finetune(self, data_file: str):
        """Fine-tuning interface."""
        with gr.Blocks() as demo:
            gr.Markdown("# Fine-Tuning")
            gr.File(label="Training Data")
            gr.Dropdown(["gpt-4o", "gpt-4o-mini"], label="Base Model")
            gr.Button("Start Training")
            gr.JSON(label="Results")
        return demo
    
    def assistant(self, assistants: list = None):
        """Assistant builder."""
        with gr.Blocks() as demo:
            gr.Markdown("# AI Assistant")
            
            assistant = gr.Dropdown(assistants or [], label="Assistant")
            msg = gr.Textbox(label="Message")
            send = gr.Button("Send")
            chat = gr.Chatbot()
            
            send.click(lambda m: self.agent_fn(m, assistant), [msg, assistant], chat)
        
        return demo
