# UI - Lazy imports with FULL builders

def GradioBuilder():
    from ui.gradio_builder import GradioBuilder as Builder
    return Builder

def create_chat():
    from ui.gradio_builder import create_chat as fn
    return fn

def chat_ui():
    from ui.streamlit_builder import chat_ui as fn
    return fn

def agent_card():
    from ui.streamlit_builder import agent_card as fn
    return fn

def config_form():
    from ui.streamlit_builder import config_form as fn
    return fn

def metrics_dashboard():
    from ui.streamlit_builder import metrics_dashboard as fn
    return fn

def file_uploader():
    from ui.streamlit_builder import file_uploader as fn
    return fn

def OpenAIBuilder():
    from ui.openai_builder import OpenAIBuilder as Builder
    return Builder

def GoogleBuilder():
    from ui.google_builder import GoogleBuilder as Builder
    return Builder

def MicrosoftBuilder():
    from ui.microsoft_builder import MicrosoftBuilder as Builder
    return Builder

def LangChainBuilder():
    from ui.langchain_builder import LangChainBuilder as Builder
    return Builder

# === FULL LangGraph Builder ===
def LangGraphBuilder():
    """LangGraph visual workflow builder with full canvas"""
    from langgraph.graph import StateGraph, END
    
    class FullLangGraphBuilder:
        def __init__(self):
            self.graph = None
            self.nodes = {}
            self.edges = []
            self.conditional_edges = []
        
        def node(self, name: str, func=None, **config):
            """Add node to graph"""
            self.nodes[name] = {"func": func, "config": config}
            return self
        
        def human_node(self, name: str, **config):
            """Add human-in-the-loop node"""
            self.nodes[name] = {
                "func": None,
                "config": config,
                "type": "human"
            }
            return self
        
        def edge(self, from_node: str, to_node: str):
            """Add direct edge"""
            self.edges.append({"from": from_node, "to": to_node})
            return self
        
        def conditional_edge(self, node: str, condition_func, mappings: dict):
            """Add conditional edge"""
            self.conditional_edges.append({
                "node": node,
                "func": condition_func,
                "mappings": mappings
            })
            return self
        
        def branch(self, node: str, condition: str, true_node: str, false_node: str):
            """Add branch (if/else)"""
            self.conditional_edges.append({
                "node": node,
                "condition": condition,
                "true": true_node,
                "false": false_node
            })
            return self
        
        def loop(self, node: str, max_iterations: int = 10):
            """Add loop with max iterations"""
            self.nodes[node]["loop"] = {
                "max_iterations": max_iterations
            }
            return self
        
        def entry_point(self, node: str):
            """Set entry point"""
            self.entry = node
            return self
        
        def compile(self):
            """Build and compile graph"""
            graph = StateGraph()
            for name, node_data in self.nodes.items():
                graph.add_node(name, node_data["func"])
            
            for edge in self.edges:
                graph.add_edge(edge["from"], edge["to"])
            
            for ce in self.conditional_edges:
                if "func" in ce:
                    graph.add_conditional_edges(
                        ce["node"],
                        ce["func"],
                        ce["mappings"]
                    )
            
            if hasattr(self, 'entry'):
                graph.set_entry_point(self.entry)
            
            return graph.compile()
        
        def visual_canvas(self, canvas_id: str = "main"):
            """Get visual canvas config"""
            return {
                "type": "visual_canvas",
                "canvas_id": canvas_id,
                "nodes": list(self.nodes.keys()),
                "edges": self.edges,
                "component": "langgraph_canvas"
            }
        
        def yaml_export(self):
            """Export as YAML"""
            import yaml
            data = {
                "nodes": self.nodes,
                "edges": self.edges,
                "conditional_edges": self.conditional_edges
            }
            return yaml.dump(data)
        
        def json_export(self):
            """Export as JSON"""
            import json
            data = {
                "nodes": {k: {"config": v["config"]} for k, v in self.nodes.items()},
                "edges": self.edges,
                "conditional_edges": self.conditional_edges
            }
            return json.dumps(data, indent=2)
    
    return FullLangGraphBuilder

__all__ = [
    "GradioBuilder",
    "create_chat",
    "chat_ui",
    "agent_card",
    "config_form",
    "metrics_dashboard",
    "file_uploader",
    "OpenAIBuilder",
    "GoogleBuilder",
    "MicrosoftBuilder",
    "LangChainBuilder",
    "LangGraphBuilder",
]