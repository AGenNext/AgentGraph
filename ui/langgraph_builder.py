"""
LangGraph SDK UI Builder.
"""

import gradio as gr
from typing import Callable


class LangGraphBuilder:
    """Build LangGraph workflow UIs."""
    
    def __init__(self, workflow_fn: Callable):
        self.workflow_fn = workflow_fn
    
    def workflow(self):
        """Workflow builder."""
        with gr.Blocks() as demo:
            gr.Markdown("# LangGraph Workflow")
            
            # Nodes
            gr.DataFrame(headers=["Node", "Type"], label="Graph Nodes")
            
            # Input
            msg = gr.Textbox(label="Input", lines=3)
            run = gr.Button("Run Workflow")
            output = gr.JSON()
            
            run.click(self.workflow_fn, msg, output)
        
        return demo
    
    def state(self):
        """State config."""
        with gr.Blocks() as demo:
            gr.Markdown("# State Schema")
            
            gr.Json(label="State", value={
                "messages": [],
                "documents": [],
                "context": {}
            })
            
            gr.Code(language="python", label="Schema Code")
        
        return demo
    
    def node_editor(self, node_types: list = None):
        """Node editor."""
        nodes = node_types or ["llm", "tool", "conditional", "start", "end"]
        
        with gr.Blocks() as demo:
            gr.Markdown("# Node Editor")
            
            gr.Dropdown(nodes, label="Node Type")
            gr.Textbox(label="Node Name")
            gr.Code(language="python", label="Code")
            gr.Button("Add Node")
        
        return demo
