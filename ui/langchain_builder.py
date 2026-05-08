"""
LangChain SDK UI Builder.
"""

import gradio as gr
from typing import Callable


class LangChainBuilder:
    """Build LangChain agent UIs."""
    
    def __init__(self, agent_fn: Callable):
        self.agent_fn = agent_fn
    
    def chat(self):
        """Chat interface."""
        return gr.ChatInterface(fn=self.agent_fn, title="LangChain Agent")
    
    def rag(self, kb_names: list = None):
        """RAG pipeline UI."""
        kbs = kb_names or ["default-kb"]
        
        with gr.Blocks() as demo:
            gr.Markdown("# RAG Pipeline")
            
            # Knowledge base selector
            gr.Dropdown(kbs, label="Knowledge Base")
            
            # Chat
            msg = gr.Textbox(label="Query", lines=3)
            submit = gr.Button("Search")
            output = gr.Chatbot()
            
            # Sources
            gr.Markdown("### Sources")
            sources = gr.JSON()
            
            submit.click(self.agent_fn, msg, [output, sources])
        
        return demo
    
    def agent_builder(self):
        """Agent builder."""
        with gr.Blocks() as demo:
            gr.Markdown("# Agent Builder")
            
            gr.Dropdown(["openai-tools", "openai-functions", "chat-conversational"], 
                     label="Agent Type")
            
            gr.Multiselect(["Calculator", "Search", "Python", "Wikipedia"], 
                        label="Tools")
            
            gr.Textbox(label="System Prompt", lines=3)
            gr.Button("Create Agent")
        
        return demo
    
    def memory(self):
        """Memory config."""
        with gr.Blocks() as demo:
            gr.Markdown("# Memory Settings")
            
            gr.Dropdown(["buffer", "summary", "entity"], label="Memory Type")
            gr.Slider(1, 10, 3, label="Window Size")
            gr.Button("Save")
        
        return demo
    
    def tools(self):
        """Tool builder."""
        with gr.Blocks() as demo:
            gr.Markdown("# Tools")
            
            name = gr.Textbox(label="Tool Name")
            desc = gr.Textbox(label="Description")
            code = gr.Code(language="python", label="Code")
            gr.Button("Add Tool")
        
        return demo
