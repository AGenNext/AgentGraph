# Builder Coverage - Visual Builders by Framework

## Current Status

| Framework | Builder | Visual Editor | Status |
|------------|---------|---------------|--------|
| OpenAI | OpenAIBuilder | Yes | ✅ Built |
| Anthropic | OpenAIBuilder | - | ⚠️ Use OpenAI |
| LangGraph | LangGraphBuilder | Yes | ✅ Built |
| LangChain | LangChainBuilder | Yes | ✅ Built |
| Google | GoogleBuilder | Yes | ✅ Built |
| Microsoft | MicrosoftBuilder | Yes | ✅ Built |
| CrewAI | LangGraphBuilder | - | ⚠️ Use LangGraph |
| AutoGen | MicrosoftBuilder | - | ⚠️ Use Microsoft |
| LlamaIndex | - | No | ❌ Missing |
| Salesforce | - | No | ❌ Missing |
| SmolAgents | - | No | ❌ Missing |

## Built: 6/11 (55%)

## Missing Visual Components

### LangGraph (Full)
- ✅ workflow_builder()
- ✅ checkpoint_viewer()  
- ✅ store_viewer()
- ❌ node_palette()
- ❌ edge_editor()
- ❌ branch_editor()
- ❌ loop_editor()
- ❌ visual_canvas()
- ❌ yaml_editor()

### Other Frameworks
Missing full visual editors for:
- CrewAI (crew builder)
- AutoGen (studio)
- LlamaIndex (index/query)
- Salesforce (Einstein)
- SmolAgents

## What Needs Building

```python
# Full LangGraphBuilder needed
class LangGraphBuilder:
    def node_palette(self):
        """Drag & drop nodes"""
        
    def edge_editor(self):
        """Draw connections"""
        
    def branch_editor(self):
        """Add if/else logic"""
        
    def loop_editor(self):
        """Add loops"""
        
    def visual_canvas(self):
        """Full drag & drop canvas"""
        
    def yaml_editor(self):
        """Text (YAML) editor"""
        
    def hybrid_editor(self):
        """Visual ↔ Code sync"""

# CrewAIBuilder needed
class CrewAIBuilder:
    def crew_builder(self):
        """Build agent crew"""
        
    def process_flow(self):
        """Sequential/hierarchical"""

# LlamaIndexBuilder needed
class LlamaIndexBuilder:
    def index_builder(self):
        """Build RAG index"""
        
    def query_engine(self):
        """Query interface"""

# SalesforceBuilder needed
class SalesforceBuilder:
    def einstein_agent(self):
        """Einstein AI agent"""
        
    def crm_integration(self):
        """CRM tools"""
```

## Recommendation

1. **Complete LangGraphBuilder** with all visual components
2. **Add CrewAIBuilder** using LangGraph as base
3. **Add LlamaIndexBuilder** for RAG workflows
4. **Delegate others** to existing builders (salesforce → openai, etc)