# LangGraph Workflow UX - Drag & Drop vs Text

## User Experience Options

### Option 1: Drag & Drop (Visual Editor)

```
┌──────────────────────────────────────────────────────────┐
│                    LANGGRAPH STUDIO                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   +─────────────┐      +─────────────┐                    │
│   │  ○ Research │─────▶│  ○ Write   │                    │
│   │  Researcher│      │  Writer    │                    │
│   └─────────────┘      └─────────────┘                    │
│         │                    │                             │
│         │                    ▼                             │
│         │              +─────────────┐                   │
│         │              │  ○ Review   │                     │
│         │              │  Reviewer   │                     │
│         │              └─────────────┘                   │
│         │                    │                          │
│         │                    ▼ (if count < 3)           │
│         │              +─────────────┐                    │
│         │              │  ◇ Branch  │                    │
│         │              └─────────────┘                   │
│         │                    │                          │
│         │                    ▼                          │
│         │              +─────────────┐                   │
│         └─────────────▶│  ○ Increment                   │
│                        │  Loop       │                    │
│                        └─────────────┘                   │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  [+ Add Node]  [+ Add Branch]  [+ Add Loop]   |  Save    │
└──────────────────────────────────────────────────────────┘

Features:
  - Drag nodes from palette
  - Connect by dragging edges
  - Double-click to edit node config
  - Right-click for branch/loop options
  - Zoom/pan canvas
  - Undo/redo support
```

### Option 2: Text (YAML/JSON)

```yaml
# workflow.yaml
name: "Research-Write-Review"

nodes:
  - id: research
    agent: openai
    model: gpt-4o
    role: "Researcher"
    
  - id: write
    agent: openai
    model: gpt-4o
    role: "Writer"
    
  - id: review
    agent: openai
    model: gpt-4o
    role: "Reviewer"
    
  - id: increment
    type: counter
    step: 1

edges:
  - from: research
    to: write
    
  - from: write
    to: review
    
  - from: increment
    to: research

branches:
  - node: review
    condition: "count < 3"
    true: increment
    false: END

entry: research
```

### Option 3: Hybrid (Both)

```
┌──────────────────────────────────────────────────────────┐
│                        EDITOR                          │
├──────────────────────────────────────────────────────────┤
│  [Visual] [Code] [Preview]                              │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Visual Mode:                          Code Mode:         │
│  ┌────────┐                       workflow.yaml        │
│  │ ○ Rsch │                       ```yaml            │
│  └───────┘                       nodes:              │
│      │                           - id: research      │
│      ▼                           - id: write        │
│  ┌────────┐                       ```               │
│  │ ○ Write│                                           │
│  └────────┘                       [Sync ↔]          │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  Mode: Auto-sync (changes in one update the other)      │
└──────────────────────────────────────────────────────────┘
```

## UI Components from agentnext

```python
from agentnext import LangGraphUI

# Visual Editor Component
LangGraphUI.workflow_builder()
# → {'type': 'workflow', 'component': 'langgraph_workflow'}

# Checkpoint Viewer (see state at each node)
LangGraphUI.checkpoint_viewer()
# → {'type': 'checkpoints', 'component': 'langgraph_checkpoints'}

# Store Viewer (see persisted data)
LangGraphUI.store_viewer()
# → {'type': 'store', 'component': 'langgraph_store'}
```

## Builder Implementation

```python
# Option 1: Use internal builder
builder = LangGraphBuilder()

# Create visual editor
app = builder.visual_editor(
    canvas=True,      # Drag & drop
    node_palette=True,
    edge_drag=True,
    text_mode=True,    # YAML/JSON edit
    sync=True         # Hybrid mode
)
app.launch()

# Option 2: Use Streamlit
from agentnext.ui import chat_ui, config_form

chat_ui()           # Chat interface
config_form()       # Config form
```

## User Experience Summary

| Mode | Interaction | Best For |
|------|-------------|----------|
| **Drag & Drop** | Visual canvas | Building workflows |
| **Text (YAML)** | Code editor | Version control, copy-paste |
| **Hybrid** | Both synced | Flexibility |
| **Chat** | Natural language | "Add a research node..." |

## Prompt-Based (Natural Language)

```
User: "Add a research node using gpt-4o"
AI:   ✓ Added node 'research' with OpenAI(gpt-4o)

User: "Connect research to writer"
AI:   ✓ Added edge research → writer

User: "Add a loop that repeats 3 times"
AI:   ✓ Added branch and loop
```

## Full Example

```python
from agentnext import *

# Launch visual editor
builder = LangGraphBuilder()
app = builder.visual_editor(
    mode="hybrid",      # drag + text
    default_model="gpt-4o"
)
app.launch()

# Or chat-based
chat_ui().launch()
```