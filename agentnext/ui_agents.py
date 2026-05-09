"""Agent UI Components - UI for each agent framework"""

# OpenAI UI
class OpenAIUI:
    @staticmethod
    def chat_component(model: str = "gpt-4o"):
        return {"type": "chat", "model": model, "component": "openai_chat"}

    @staticmethod
    def assistant_component():
        return {"type": "assistant", "component": "openai_assistant"}

    @staticmethod
    def embeddings_component():
        return {"type": "embeddings", "component": "openai_embeddings"}


# Anthropic UI
class AnthropicUI:
    @staticmethod
    def chat_component(model: str = "claude-sonnet-4"):
        return {"type": "chat", "model": model, "component": "anthropic_chat"}

    @staticmethod
    def artifacts_component():
        return {"type": "artifacts", "component": "anthropic_artifacts"}

    @staticmethod
    def node_palette():
        return {"type": "node_palette", "nodes": [
            {"id": "claude", "name": "Claude", "icon": "🤖"},
            {"id": "haiku", "name": "Haiku", "icon": "📝"},
            {"id": "tool", "name": "Tool", "icon": "🔧"},
        ], "component": "anthropic_node_palette"}

    @staticmethod
    def visual_canvas():
        return {"type": "visual_canvas", "component": "anthropic_canvas"}

    @staticmethod
    def model_selector():
        return {"type": "model_selector", "models": ["claude-3-5-opus", "claude-3-5-sonnet", "claude-3-haiku"], "component": "anthropic_models"}


# LangGraph UI
class LangGraphUI:
    @staticmethod
    def workflow_builder():
        return {"type": "workflow", "component": "langgraph_workflow"}

    @staticmethod
    def checkpoint_viewer():
        return {"type": "checkpoints", "component": "langgraph_checkpoints"}

    @staticmethod
    def store_viewer():
        return {"type": "store", "component": "langgraph_store"}

    @staticmethod
    def node_palette():
        return {"type": "node_palette", "nodes": [
            {"id": "agent", "name": "Agent", "icon": "🤖"},
            {"id": "llm", "name": "LLM", "icon": "💬"},
            {"id": "tool", "name": "Tool", "icon": "🔧"},
            {"id": "condition", "name": "Condition", "icon": "❓"},
            {"id": "loop", "name": "Loop", "icon": "🔄"},
            {"id": "map", "name": "Map", "icon": "📂"},
            {"id": "reduce", "name": "Reduce", "icon": "📥"},
            {"id": "human", "name": "Human", "icon": "👤"},
        ], "component": "langgraph_node_palette"}

    @staticmethod
    def human_in_loop():
        return {"type": "human_in_loop", "actions": ["approve", "reject", "input", "choose"], "timeout": 300, "component": "langgraph_human"}

    @staticmethod
    def approval_gate():
        return {"type": "approval_gate", "states": ["pending", "approved", "rejected"], "notify": True, "component": "langgraph_approval"}

    @staticmethod
    def branch_editor():
        return {"type": "branch_editor", "conditions": ["equals", "greater_than", "contains", "regex"], "component": "langgraph_branch_editor"}

    @staticmethod
    def edge_editor():
        return {"type": "edge_editor", "modes": ["direct", "conditional"], "component": "langgraph_edge_editor"}

    @staticmethod
    def loop_editor():
        return {"type": "loop_editor", "options": ["while", "until", "count"], "max_iterations": 10, "component": "langgraph_loop_editor"}

    @staticmethod
    def visual_canvas():
        return {"type": "visual_canvas", "component": "langgraph_canvas"}

    @staticmethod
    def yaml_editor():
        return {"type": "yaml_editor", "syntax": "yaml", "component": "langgraph_yaml"}

    @staticmethod
    def hybrid_editor():
        return {"type": "hybrid", "modes": ["visual", "code", "preview"], "sync": True, "component": "langgraph_hybrid"}

    @staticmethod
    def both_editors():
        """3 ways to build: Visual, Declarative (YAML), Code"""
        return {"visual": {"name": "Visual Editor", "type": "visual_canvas", "drag_drop": True, "component": "langgraph_canvas"}, "declarative": {"name": "Declarative (YAML)", "type": "yaml_editor", "syntax": "yaml", "component": "langgraph_yaml"}, "code": {"name": "Code (Python)", "type": "code_editor", "syntax": "python", "component": "langgraph_code"}}

    @staticmethod
    def workflow_builder():
        """Build workflow 3 ways"""
        return {"type": "workflow_builder", "ways": ["visual", "declarative", "code"], "switch": "one_click", "component": "langgraph_workflow"}

    @staticmethod
    def checkpoint_table():
        return {"type": "checkpoint_table", "component": "langgraph_checkpoints"}

    @staticmethod
    def store_browser():
        return {"type": "store_browser", "actions": ["get", "put", "delete", "search"], "component": "langgraph_store"}

    @staticmethod
    def human_feedback():
        return {"type": "human_feedback", "rating": True, "comment": True, "rewind": True, "component": "langgraph_feedback"}


# LangChain UI
class LangChainUI:
    @staticmethod
    def chain_builder():
        return {"type": "chain", "component": "langchain_chain"}

    @staticmethod
    def tool_registry():
        return {"type": "tools", "component": "langchain_tools"}

    @staticmethod
    def memory_viewer():
        return {"type": "memory", "component": "langchain_memory"}


# Google ADK UI
class GoogleUI:
    @staticmethod
    def agent_builder():
        return {"type": "agent", "component": "google_agent"}

    @staticmethod
    def session_manager():
        return {"type": "session", "component": "google_session"}

    @staticmethod
    def node_palette():
        return {"type": "node_palette", "nodes": [
            {"id": "gemini", "name": "Gemini", "icon": "💎"},
            {"id": "agent", "name": "Agent", "icon": "🤖"},
            {"id": "tool", "name": "Tool", "icon": "🔧"},
        ], "component": "google_node_palette"}

    @staticmethod
    def visual_canvas():
        return {"type": "visual_canvas", "component": "google_canvas"}


# Microsoft AutoGen UI
class MicrosoftUI:
    @staticmethod
    def group_chat():
        return {"type": "group_chat", "component": "microsoft_groupchat"}

    @staticmethod
    def studio():
        return {"type": "studio", "component": "microsoft_studio"}

    @staticmethod
    def node_palette():
        return {"type": "node_palette", "nodes": [
            {"id": "assistant", "name": "Assistant", "icon": "🤖"},
            {"id": "user", "name": "User", "icon": "👤"},
            {"id": "group_chat", "name": "Group Chat", "icon": "👥"},
        ], "component": "microsoft_node_palette"}

    @staticmethod
    def visual_canvas():
        return {"type": "visual_canvas", "component": "microsoft_canvas"}

    @staticmethod
    def human_in_loop():
        return {"type": "human_in_loop", "actions": ["approve", "reject", "input"], "component": "microsoft_human"}


# CrewAI UI
class CrewAIUI:
    @staticmethod
    def crew_builder():
        return {"type": "crew", "component": "crewai_crew"}

    @staticmethod
    def process_flow():
        return {"type": "process", "modes": ["sequential", "hierarchical"], "component": "crewai_process"}

    @staticmethod
    def agent_palette():
        return {"type": "agent_palette", "agents": [
            {"id": "researcher", "name": "Researcher", "role": "Research"},
            {"id": "writer", "name": "Writer", "role": "Writing"},
            {"id": "analyst", "name": "Analyst", "role": "Analysis"},
        ], "component": "crewai_agents"}

    @staticmethod
    def task_manager():
        return {"type": "task_manager", "actions": ["assign", "queue", "complete"], "component": "crewai_tasks"}


# LlamaIndex UI
class LlamaIndexUI:
    @staticmethod
    def index_builder():
        return {"type": "index", "component": "llamaindex_index"}

    @staticmethod
    def query_engine():
        return {"type": "query", "component": "llamaindex_query"}

    @staticmethod
    def document_loader():
        return {"type": "document", "component": "llamaindex_documents"}

    @staticmethod
    def vector_store():
        return {"type": "vector", "component": "llamaindex_vector"}


# Salesforce UI
class SalesforceUI:
    @staticmethod
    def einstein_agent():
        return {"type": "einstein", "component": "salesforce_einstein"}

    @staticmethod
    def crm_integration():
        return {"type": "crm", "component": "salesforce_crm"}

    @staticmethod
    def node_palette():
        return {"type": "node_palette", "nodes": [
            {"id": "einstein", "name": "Einstein", "icon": "⚡"},
            {"id": "crm", "name": "CRM", "icon": "📊"},
            {"id": "case", "name": "Case", "icon": "📁"},
        ], "component": "salesforce_node_palette"}

    @staticmethod
    def visual_canvas():
        return {"type": "visual_canvas", "component": "salesforce_canvas"}

    @staticmethod
    def einstein_plus():
        return {"type": "einstein_plus", "features": ["predictions", "recommendations"], "component": "salesforce_einstein_plus"}


# AutoGen UI
class AutoGenUI:
    @staticmethod
    def studio():
        return {"type": "studio", "component": "autogen_studio"}

    @staticmethod
    def group_chat():
        return {"type": "group_chat", "component": "autogen_groupchat"}

    @staticmethod
    def code_executor():
        return {"type": "code_executor", "language": "python", "component": "autogen_code"}

    @staticmethod
    def node_palette():
        return {"type": "node_palette", "nodes": [
            {"id": "assistant", "name": "Assistant", "icon": "🤖"},
            {"id": "user_proxy", "name": "User Proxy", "icon": "👤"},
            {"id": "code_executor", "name": "Code Executor", "icon": "💻"},
            {"id": "function", "name": "Function", "icon": "🔧"},
            {"id": "group_chat", "name": "Group Chat", "icon": "👥"},
        ], "component": "autogen_node_palette"}

    @staticmethod
    def human_in_loop():
        return {"type": "human_in_loop", "actions": ["approve", "reject", "input", "choose"], "component": "autogen_human"}

    @staticmethod
    def approval_gate():
        return {"type": "approval_gate", "states": ["pending", "approved", "rejected"], "component": "autogen_approval"}

    @staticmethod
    def visual_canvas():
        return {"type": "visual_canvas", "component": "autogen_canvas"}

    @staticmethod
    def checkpoint_viewer():
        return {"type": "checkpoints", "component": "autogen_checkpoints"}

    @staticmethod
    def store_viewer():
        return {"type": "store", "component": "autogen_store"}


# SmolAgents UI
class SmolAgentsUI:
    @staticmethod
    def agent_builder():
        return {"type": "agent", "component": "smolagents_agent"}

    @staticmethod
    def code_agent():
        return {"type": "code_agent", "component": "smolagents_code"}

    @staticmethod
    def tools_registry():
        return {"type": "tools", "component": "smolagents_tools"}