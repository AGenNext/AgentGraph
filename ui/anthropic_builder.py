"""
Anthropic SDK UI Builder.

https://console.anthropic.com/
"""

import gradio as gr
from typing import Callable, List


class AnthropicBuilder:
    """Build Anthropic Claude agent UIs."""
    
    def __init__(self, agent_fn: Callable):
        self.agent_fn = agent_fn
    
    def chat(self):
        """Chat interface."""
        return gr.ChatInterface(
            fn=self.agent_fn,
            title="Claude Agent"
        )
    
    def playground(self, models: List[str] = None):
        """Model playground."""
        models = models or ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229"]
        
        with gr.Blocks() as demo:
            gr.Markdown("# Anthropic Claude Playground")
            
            with gr.Row():
                model = gr.Dropdown(models, label="Model")
                temp = gr.Slider(0, 1, 0.7, label="Temperature")
                max_tokens = gr.Slider(1024, 4096, 4096, label="Max Tokens")
            
            msg = gr.Textbox(label="Message", lines=3)
            submit = gr.Button("Send")
            output = gr.Chatbot()
            
            submit.click(
                lambda m, md, t, mt: self.agent_fn(m, md, t, mt),
                [msg, model, temp, max_tokens],
                output
            )
        
        return demo
    
    def workbench(self):
        """Claude Workbench."""
        with gr.Blocks() as demo:
            gr.Markdown("# Claude Workbench")
            
            with gr.Row():
                system = gr.Textbox(
                    label="System Prompt",
                    lines=3,
                    value="You are a helpful AI assistant."
                )
            
            with gr.Row():
                msg = gr.Textbox(label="Prompt", lines=4)
                analyze = gr.Button("Analyze")
            
            output = gr.JSON(label="Output")
            tokens = gr.Number(label="Tokens Used")
            
            analyze.click(
                lambda m, s: {"output": m, "tokens": len(m.split())},
                [msg, system],
                [output, tokens]
            )
        
        return demo
    
    def comparison(self):
        """Compare models."""
        models = ["claude-3-5-sonnet", "claude-3-opus", "claude-3-haiku"]
        
        with gr.Blocks() as demo:
            gr.Markdown("# Model Comparison")
            
            msg = gr.Textbox(label="Test Prompt", lines=3)
            compare = gr.Button("Compare")
            
            for model in models:
                gr.Markdown(f"### {model}")
                gr.Textbox(label=f"Output ({model})", lines=3)
        
        return demo
