"""
Example: Runnable UIs for each SDK.

Run any of these to start a UI.
"""

# ==== OPENAI ====
def run_openai_ui():
    """Run OpenAI playground."""
    from ui import OpenAIBuilder
    
    def agent_fn(msg, model):
        return f"Processed: {msg} with {model}"
    
    builder = OpenAIBuilder(agent_fn)
    demo = builder.playground()
    demo.launch()


# ==== GOOGLE ====
def run_google_ui():
    """Run Google Vision UI."""
    from ui import GoogleBuilder
    
    def agent_fn(img, prompt):
        return {"analysis": f"Analyzed: {prompt}"}
    
    builder = GoogleBuilder(agent_fn)
    demo = builder.vision()
    demo.launch()


def run_google_grounded():
    """Run Google Grounded Generation."""
    from ui import GoogleBuilder
    
    def agent_fn(query, use_search):
        return {"result": query, "grounded": use_search}
    
    builder = GoogleBuilder(agent_fn)
    demo = builder.grounded()
    demo.launch()


# ==== MICROSOFT ====
def run_microsoft_ui():
    """Run Microsoft AI Agent UI."""
    from ui import MicrosoftBuilder
    
    def agent_fn(msg):
        return f"Azure AI: {msg}"
    
    builder = MicrosoftBuilder(agent_fn)
    demo = builder.chat()
    demo.launch()


def run_copilot_ui():
    """Run Copilot Studio UI."""
    from ui import MicrosoftBuilder
    
    builder = MicrosoftBuilder(lambda x: x)
    demo = builder.copilot()
    demo.launch()


# ==== LANGCHAIN ====
def run_langchain_rag():
    """Run LangChain RAG UI."""
    from ui import LangChainBuilder
    
    def agent_fn(query):
        return {"documents": [f"Doc about: {query}"], "sources": []}
    
    builder = LangChainBuilder(agent_fn)
    demo = builder.rag()
    demo.launch()


def run_agent_builder():
    """Run LangChain Agent Builder."""
    from ui import LangChainBuilder
    
    builder = LangChainBuilder(lambda x: x)
    demo = builder.agent_builder()
    demo.launch()


# ==== LANGGRAPH ====
def run_langgraph_workflow():
    """Run LangGraph Workflow UI."""
    from ui import LangGraphBuilder
    
    def workflow_fn(input_data):
        return {"result": input_data, "nodes_executed": ["start", "llm"]}
    
    builder = LangGraphBuilder(workflow_fn)
    demo = builder.workflow()
    demo.launch()


# ==== GRADIO ====
def run_basic_chat():
    """Run basic chat UI."""
    from ui import create_chat
    
    def chat_fn(msg):
        return f"Echo: {msg}"
    
    demo = create_chat(chat_fn, "Basic Chat")
    demo.launch()


# ==== RUN ALL ====
if __name__ == "__main__":
    import sys
    
    examples = {
        "openai": run_openai_ui,
        "google": run_google_ui,
        "google-grounded": run_google_grounded,
        "microsoft": run_microsoft_ui,
        "copilot": run_copilot_ui,
        "langchain-rag": run_langchain_rag,
        "langchain-agent": run_agent_builder,
        "langgraph": run_langgraph_workflow,
        "chat": run_basic_chat,
    }
    
    if len(sys.argv) > 1:
        name = sys.argv[1]
        if name in examples:
            print(f"Running: {name}")
            examples[name]()
        else:
            print(f"Available: {list(examples.keys())}")
    else:
        print("Usage: python ui/examples.py <example>")
        print(f"Examples: {list(examples.keys())}")
