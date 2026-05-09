# LangGraph Workflow - Nodes, Edges, Branches, Loops

## Build Workflow Components

```python
from agentnext import *
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import tools_condition
from langgraph.func import entrypoint

# === Step 1: Select Framework ===
fw = FrameworkSelector.get_framework('langgraph')
# {'name': 'LangGraph', 'color': '#6B47FF', 'models': ['gpt-4o', 'claude-3-5']}

# === Step 2: Get UI Component ===
ui = LangGraphUI.workflow_builder()
# {'type': 'workflow', 'component': 'langgraph_workflow'}

# === Step 3: Build Graph with Nodes, Edges, Branches, Loops ===

# Define State
class GraphState(dict):
    messages: list
    result: str
    count: int

# Create Graph
graph = StateGraph(GraphState)

# ----- NODES -----
@graph.node
defResearcher(state):
    """Research agent node"""
    # Use OpenAI
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=state["messages"]
    )
    return {"result": response.choices[0].message.content}

@graph.node
def Writer(state):
    """Writer agent node"""
    return {"result": f"Written: {state.get('result', '')}"}

@graph.node  
def Reviewer(state):
    """Reviewer agent node"""
    return {"result": f"Reviewed: {state.get('result', '')}"}

@graph.node
def Incrementer(state):
    """Increment loop counter"""
    return {"count": state.get("count", 0) + 1}

# Add nodes to graph
graph.add_node("research", Researcher)
graph.add_node("write", Writer)
graph.add_node("review", Reviewer)
graph.add_node("increment", Incrementer)

# ----- EDGES -----
# Edge: research -> write -> review
graph.add_edge("research", "write")
graph.add_edge("write", "review")

# ----- CONDITIONAL EDGES (Branches) -----
def should_continue(state):
    """Branch: continue or end?"""
    if state.get("count", 0) < 3:  # Loop 3 times
        return "increment"
    return END

graph.add_conditional_edges(
    "review",
    should_continue,
    {
        "increment": "increment",  # Loop back
        END: END                    # End
    }
)

# Loop: increment -> research
graph.add_edge("increment", "research")

# ----- SET ENTRY POINT -----
graph.set_entry_point("research")

# === Step 4: Compile & Run ===

app = graph.compile()

# Run workflow
result = app.invoke({
    "messages": [{"role": "user", "content": "Write about AI"}],
    "count": 0
})
```

## Visual Flow

```
LangGraph Workflow:

  +-----------+     +-----------+     +-----------+
  |  Node 1   | --> |  Node 2   | --> |  Node 3   │
  |Researcher |     |  Writer   |     | Reviewer  │
  └-----------+     └-----------+     └-----------+
                                             |
                                             v (conditional)
                                        +-----------+
                                        | Branch    |
                                        | continue |
                                        | or END   |
                                        +-----------+
                                            |
                                       if count < 3
                                            |
                                            v
                                        +-----------+
                                        |   Loop    |
                                        |increment |
                                        └-----------+
                                            |
                                            v (edge)
                                        +-----------+
                                        |Researcher| (back to start)
                                        └-----------+
```

## Components Summary

| Component | Method | Description |
|-----------|--------|-------------|
| **Node** | `graph.add_node()` | Agent action (Researcher, Writer, Reviewer) |
| **Edge** | `graph.add_edge()` | Linear flow (A -> B) |
| **Branch** | `graph.add_conditional_edges()` | If/else logic (continue or END) |
| **Loop** | Add edge back to earlier node | Repeat until condition |
| **Entry** | `graph.set_entry_point()` | Start node |
| **END** | `END` constant | End workflow |

## Full Example with UI

```python
from agentnext import LangGraphUI, FrameworkSelector

# Select framework
fw = FrameworkSelector.get_framework('langgraph')

# Get UI
ui = LangGraphUI.workflow_builder()

# Build graph
workflow = {
    "nodes": {
        "research": {"agent": "openai", "model": "gpt-4o"},
        "write": {"agent": "openai", "model": "gpt-4o"},
        "review": {"agent": "openai", "model": "gpt-4o"},
    },
    "edges": [
        {"from": "research", "to": "write"},
        {"from": "write", "to": "review"},
    ],
    "branches": {
        "review": {
            "condition": "count < 3",
            "true": "increment",
            "false": "END"
        }
    },
    "loops": {
        "increment": "research"  # Loop back
    }
}
```