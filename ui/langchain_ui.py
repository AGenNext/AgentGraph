"""
LangChain UI Toolkit.

https://python.langchain.com/
"""

from typing import List, Dict, Optional


class LangChainUI:
    """LangChain UI components."""
    
    @staticmethod
    def chat_component(llm: str = "openai"):
        """Chat component."""
        return {
            "type": "chat",
            "llm": llm,
            "component": "langchain_chat"
        }
    
    @staticmethod
    def vectorstore_component(store: str = "faiss"):
        """Vector store component."""
        return {
            "type": "vectorstore",
            "store": store,
            "component": "langchain_vs"
        }
    
    @staticmethod
    def rag_component():
        """RAG pipeline."""
        return {
            "type": "rag",
            "component": "langchain_rag"
        }
    
    @staticmethod
    def agent_component(agent_type: str = "openai-tools"):
        """Agent component."""
        return {
            "type": "agent",
            "agent_type": agent_type,
            "component": "langchain_agent"
        }
    
    @staticmethod
    def tool_component():
        """Tool/component."""
        return {
            "type": "tool",
            "component": "langchain_tool"
        }
    
    @staticmethod
    def memory_component(memory_type: str = "buffer"):
        """Memory component."""
        return {
            "type": "memory",
            "memory_type": memory_type,
            "component": "langchain_mem"
        }


class LangGraphUI:
    """LangGraph specific."""
    
    @staticmethod
    def workflow_component():
        """Workflow/graph."""
        return {
            "type": "workflow",
            "component": "langgraph_wf"
        }
    
    @staticmethod
    def node_component(node_type: str):
        """Graph node."""
        return {
            "type": "node",
            "node_type": node_type,
            "component": "langgraph_node"
        }
    
    @staticmethod
    def state_component():
        """Graph state."""
        return {
            "type": "state",
            "component": "langgraph_state"
        }
