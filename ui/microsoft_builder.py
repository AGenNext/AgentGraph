"""
Microsoft SDK UI Builder.
"""

import gradio as gr
from typing import Callable


class MicrosoftBuilder:
    """Build Microsoft Azure AI agent UIs."""
    
    def __init__(self, agent_fn: Callable):
        self.agent_fn = agent_fn
    
    def chat(self):
        """Chat interface."""
        return gr.ChatInterface(fn=self.agent_fn, title="Azure AI Chat")
    
    def ai_agent(self):
        """AI Agent Studio."""
        with gr.Blocks() as demo:
            gr.Markdown("# Azure AI Agent")
            
            # Agent selector
            gr.Dropdown(["agent-1", "agent-2"], label="Select Agent")
            gr.Textbox(label="Instruction", lines=2)
            gr.Button("Create Agent")
            
            # Chat
            gr.Chatbot(label="Chat")
            gr.Textbox(label="Message")
            gr.Button("Send")
        
        return demo
    
    def copilot(self):
        """Copilot Studio."""
        with gr.Blocks() as demo:
            gr.Markdown("# Copilot Studio")
            gr.Textbox(label="System Prompt", lines=3)
            gr.Textbox(label="User Query", lines=2)
            gr.Button("Generate")
            gr.Markdown("### Response")
            output = gr.Textbox(lines=5)
        
        return demo
    
    def foundry(self):
        """AI Foundry."""
        with gr.Blocks() as demo:
            gr.Markdown("# Azure AI Foundry")
            gr.File(label="Project File")
            gr.JSON(label="Configuration")
            gr.Button("Deploy")
        
        return demo
    
    def evaluation(self):
        """Evaluation Studio."""
        with gr.Blocks() as demo:
            gr.Markdown("# Evaluation")
            gr.File(label="Test Data")
            gr.Button("Run Evaluation")
            gr.DataFrame(label="Results")
        
        return demo
