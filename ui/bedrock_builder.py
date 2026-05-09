"""
AWS Bedrock UI Builder.

https://aws.amazon.com/bedrock/
"""

import gradio as gr
from typing import Callable, List


class BedrockBuilder:
    """Build AWS Bedrock agent UIs."""
    
    def __init__(self, agent_fn: Callable):
        self.agent_fn = agent_fn
    
    def chat(self):
        """Chat interface."""
        return gr.ChatInterface(
            fn=self.agent_fn,
            title="Bedrock Agent"
        )
    
    def playground(self):
        """Bedrock Playground."""
        models = [
            "anthropic.claude-3-5-sonnet",
            "anthropic.claude-3-opus",
            "amazon.titan-text-express",
            "meta.llama3-70b",
            "ai21.j2-mid",
            "cohere.command-r"
        ]
        
        with gr.Blocks() as demo:
            gr.Markdown("# AWS Bedrock Playground")
            
            with gr.Row():
                model = gr.Dropdown(models, label="Model")
                region = gr.Dropdown(
                    ["us-east-1", "us-west-2", "eu-west-1"],
                    label="Region"
                )
            
            with gr.Row():
                temp = gr.Slider(0, 1, 0.7, label="Temperature")
                max_tokens = gr.Slider(1024, 4096, 4096, label="Max Tokens")
            
            msg = gr.Textbox(label="Message", lines=3)
            submit = gr.Button("Send")
            output = gr.Chatbot()
            
            submit.click(self.agent_fn, msg, output)
        
        return demo
    
    def knowledge_base(self):
        """Knowledge base integration."""
        with gr.Blocks() as demo:
            gr.Markdown("# Knowledge Base + Bedrock")
            
            kb = gr.Dropdown(
                ["documents", "faq", "product-catalog"],
                label="Knowledge Base"
            )
            
            msg = gr.Textbox(label="Query", lines=3)
            search = gr.Button("Search KB")
            
            results = gr.JSON(label="Results")
            sources = gr.JSON(label="Sources")
            
            search.click(
                lambda q, k: {"results": [q], "sources": [k]},
                [msg, kb],
                [results, sources]
            )
        
        return demo
    
    def agents(self):
        """Bedrock Agents."""
        with gr.Blocks() as demo:
            gr.Markdown("# Bedrock Agents")
            
            agent = gr.Dropdown(
                ["customer-support", "code-review", "data-analyst"],
                label="Select Agent"
            )
            
            msg = gr.Textbox(label="Task", lines=3)
            run = gr.Button("Run")
            
            output = gr.JSON(label="Output")
            trace = gr.JSON(label="Execution Trace")
        
        return demo
    
    def guardrails(self):
        """Guardrails config."""
        with gr.Blocks() as demo:
            gr.Markdown("# Guardrails Configuration")
            
            gr.Checkbox(label="Content Filter", value=True)
            gr.Checkbox(label="PII Filter", value=True)
            gr.Checkbox(label="Topic Guard")
            gr.Checkbox(label="Word Filter")
            
            gr.Number(label="Confidence Threshold", value=0.9)
            gr.Button("Save Configuration")
        
        return demo
