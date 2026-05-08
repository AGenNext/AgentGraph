"""
LangGraph SDK Client.

https://langchain.dev/langgraph
"""

from typing import Optional, List, Dict, Any, Callable
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from dataclasses import dataclass, field


# Define state schema
class AgentState(BaseModel):
    """Agent state schema."""
    messages: List[Dict] = []
    documents: List[str] = []
    context: Dict = {}
    next_step: str = ""


class LangGraphClient:
    """LangGraph SDK client."""
    
    def __init__(
        self,
        llm,
        state_schema: Optional[type] = None,
        **kwargs
    ):
        self.llm = llm
        self.state_schema = state_schema or AgentState
        self.graph = StateGraph(self.state_schema)
        self.nodes = {}
        self.edges = []
    
    def add_node(self, name: str, func: Callable):
        """Add a node."""
        self.nodes[name] = func
        self.graph.add_node(name, func)
    
    def add_edge(self, from_node: str, to_node: str):
        """Add an edge."""
        self.graph.add_edge(from_node, to_node)
    
    def set_entry(self, node: str):
        """Set entry point."""
        self.graph.set_entry_point(node)
    
    def set_finish(self, node: str):
        """Set finish point."""
        self.graph.add_edge(node, END)
    
    def compile(self):
        """Compile the graph."""
        return self.graph.compile()
    
    def run(self, input_state: Dict) -> Dict:
        """Run the graph."""
        app = self.compile()
        return app.invoke(input_state)
    
    def create_workflow(self, name: str):
        """Create workflow."""
        self.graph = StateGraph(self.state_schema)
        return self.graph
    
    def add_conditional_edges(
        self,
        source: str,
        condition_fn: Callable,
        paths: Dict[str, str]
    ):
        """Add conditional edges."""
        self.graph.add_conditional_edges(source, condition_fn, paths)


def create_client(llm, **kwargs) -> LangGraphClient:
    """Create LangGraph client."""
    return LangGraphClient(llm=llm, **kwargs)
