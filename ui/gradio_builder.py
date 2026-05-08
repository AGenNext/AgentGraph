"""
Gradio UI Builder - ACTUAL working code.
"""

import gradio as gr
from typing import List, Dict, Callable, Optional


class GradioBuilder:
    """Build Gradio interfaces for agents."""
    
    def __init__(self, agent_fn: Callable):
        self.agent_fn = agent_fn
        self.title = "AI Agent"
        self.description = ""
    
    def with_title(self, title: str):
        self.title = title
        return self
    
    def with_description(self, desc: str):
        self.description = desc
        return self
    
    def build_chat(self) -> gr.Interface:
        """Build chat interface."""
        return gr.ChatInterface(
            fn=self.agent_fn,
            title=self.title,
            description=self.description,
        )
    
    def build_blocks(self) -> gr.Blocks:
        """Build custom blocks."""
        with gr.Blocks(title=self.title) as demo:
            gr.Markdown(f"# {self.title}")
            if self.description:
                gr.Markdown(self.description)
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Message",
                    placeholder="Type your message...",
                    lines=3,
                )
            
            with gr.Row():
                submit = gr.Button("Submit")
                clear = gr.Button("Clear")
            
            output = gr.Chatbot(label="Chat")
            
            def respond(message, history):
                history = history or []
                response = self.agent_fn(message)
                history.append((message, response))
                return "", history
            
            submit.click(respond, [msg, output], [msg, output])
            msg.submit(respond, [msg, output], [msg, output])
            clear.click(lambda: ("", []), None, [msg, output])
        
        return demo
    
    def build_agent_card(self) -> gr.Blocks:
        """Build agent info card."""
        with gr.Blocks(title=self.title) as demo:
            gr.Markdown(f"# {self.title}")
            gr.Markdown(self.description or "AI Agent")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Configuration")
                    temp = gr.Slider(0, 2, 0.7, label="Temperature")
                    max_tokens = gr.Slider(100, 4000, 1000, label="Max Tokens")
            
            with gr.Row():
                input_msg = gr.Textbox(label="Input", lines=4)
            
            with gr.Row():
                run_btn = gr.Button("Run Agent")
            
            output = gr.JSON(label="Output")
                
        return demo


def create_chat(agent_fn: Callable, title: str = "AI Agent") -> gr.Interface:
    """Quick chat interface."""
    return gr.ChatInterface(
        fn=agent_fn,
        title=title,
    )
