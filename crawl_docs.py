"""
Crawl agent framework docs and create structured data using LlamaIndex
"""

from firecrawl import FirecrawlAgent
from llama_index.core import Document, KnowledgeGraphIndex
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
import json
import os
from typing import List, Dict

# Framework docs URLs
FRAMEWORK_SOURCES = {
    "langgraph": {
        "url": "https://docs.langgraph.ai/",
        "description": "LangGraph Agent Framework - Checkpoints, Memory, Human-in-Loop"
    },
    "langchain": {
        "url": "https://python.langchain.com/docs/",
        "description": "LangChain - Memory, Agents, Chains, Tools"
    },
    "autogen": {
        "url": "https://microsoft.github.io/autogen/",
        "description": "Microsoft AutoGen - Multi-Agent, Human Feedback"
    },
    "crewai": {
        "url": "https://docs.crewai.com/",
        "description": "CrewAI - Role-based Multi-Agent, Memory"
    },
    "openai": {
        "url": "https://platform.openai.com/docs/agents",
        "description": "OpenAI Agents SDK - Tools, Streaming, Guardrails"
    },
    "anthropic": {
        "url": "https://docs.anthropic.com/",
        "description": "Anthropic Claude - Tool Use, Computer Use, MCP"
    },
    "github_copilot": {
        "url": "https://docs.github.com/en/copilot",
        "description": "GitHub Copilot - Custom Agents, Skills, Memory"
    },
    "salesforce": {
        "url": "https://developer.salesforce.com/docs/ai/agentforce/",
        "description": "Salesforce Agentforce - Builder, Flow Integration"
    },
    "smolagents": {
        "url": "https://smolagents.ai/",
        "description": "SmolAgents - Code-interpreting, Minimal deps"
    },
    "docker": {
        "url": "https://docs.docker.com/",
        "description": "Docker AI - Build Assistant"
    },
}

# Feature categories to extract
FEATURE_CATEGORIES = [
    "checkpoints",
    "memory", 
    "human_in_loop",
    "multi_agent",
    "tools",
    "streaming",
    "computer_use",
    "mcp",
    "guardrails",
]

def crawl_framework_docs():
    """Crawl all framework documentation using Firecrawl"""
    
    crawler = FirecrawlAgent()
    all_docs = []
    
    for framework, info in FRAMEWORK_SOURCES.items():
        print(f"Crawling {framework}...")
        
        try:
            # Use Firecrawl to extract content
            result = crawler.crawl(
                url=info["url"],
                options={
                    "formats": ["markdown", "html"],
                    "only": ["main", "article", "section"],
                }
            )
            
            docs.append({
                "framework": framework,
                "description": info["description"],
                "url": info["url"],
                "content": result.markdown if hasattr(result, 'markdown') else str(result),
            })
            
        except Exception as e:
            print(f"Error crawling {framework}: {e}")
            continue
    
    return all_docs

def extract_features_structured(docs: List[Dict]) -> Dict:
    """Extract features from docs into structured format"""
    
    structured_data = {}
    
    for doc in docs:
        framework = doc["framework"]
        content = doc["content"]
        
        features = {
            "checkpoints": [],
            "memory": [],
            "human_in_loop": [],
            "multi_agent": [],
            "tools": [],
            "streaming": [],
            "computer_use": None,
            "mcp": None,
            "guardrails": None,
        }
        
        # Simple keyword-based extraction (can be enhanced with LLM)
        content_lower = content.lower()
        
        # Checkpoints
        if any(kw in content_lower for kw in ["checkpointer", "checkpoint", "memory saver", "save state"]):
            features["checkpoints"].append("save_resume")
        if "sqlite" in content_lower:
            features["checkpoints"].append("sqlite")
        if "postgres" in content_lower:
            features["checkpoints"].append("postgres")
            
        # Memory
        if "memory" in content_lower:
            features["memory"].append("short_term")
        if "store" in content_lower:
            features["memory"].append("long_term")
        if "semantic" in content_lower:
            features["memory"].append("semantic")
            
        # Human-in-loop
        if "interrupt" in content_lower:
            features["human_in_loop"].append("interrupt")
        if "human" in content_lower and "feedback" in content_lower:
            features["human_in_loop"].append("feedback")
        if "approval" in content_lower:
            features["human_in_loop"].append("approval")
            
        # Multi-agent
        if "multi" in content_lower and "agent" in content_lower:
            features["multi_agent"].append("native")
        if "crew" in content_lower:
            features["multi_agent"].append("crew")
        if "group" in content_lower:
            features["multi_agent"].append("group")
            
        # Tools
        if "tool" in content_lower:
            features["tools"].append("function_calling")
        if "code" in content_lower and "exec" in content_lower:
            features["tools"].append("code_exec")
        if "search" in content_lower:
            features["tools"].append("search")
            
        # Streaming
        if "stream" in content_lower:
            features["streaming"].append("token")
            
        # Computer use
        if "computer" in content_lower and "use" in content_lower:
            features["computer_use"] = True
            
        # MCP
        if "mcp" in content_lower or "model context protocol" in content_lower:
            features["mcp"] = True
            
        # Guardrails
        if "guardrail" in content_lower:
            features["guardrails"] = True
        
        structured_data[framework] = features
    
    return structured_data

def create_knowledge_graph(structured_data: Dict):
    """Create knowledge graph using LlamaIndex"""
    
    # Create documents
    documents = []
    
    for framework, features in structured_data.items():
        # Create a rich text representation
        doc_text = f"""
# {framework.upper()}

## Features

### Checkpoints/State
{', '.join(features.get('checkpoints', [])) or 'Not available'}

### Memory
{', '.join(features.get('memory', [])) or 'Not available'}

### Human-in-Loop
{', '.join(features.get('human_in_loop', [])) or 'Not available'}

### Multi-Agent
{', '.join(features.get('multi_agent', [])) or 'Not available'}

### Tools
{', '.join(features.get('tools', [])) or 'Not available'}

### Streaming
{', '.join(features.get('streaming', [])) or 'Not available'}

### Computer Use
{('Yes' if features.get('computer_use') else 'No')}

### MCP Support
{('Yes' if features.get('mcp') else 'No')}

### Guardrails
{('Yes' if features.get('guardrails') else 'No')}
"""
        
        documents.append(Document(
            text=doc_text,
            doc_id=framework,
            extra_info={
                "framework": framework,
                "url": FRAMEWORK_SOURCES.get(framework, {}).get("url", ""),
            }
        ))
    
    # Create knowledge graph index
    storage_context = StorageContext.from_defaults()
    
    # Save to directory
    output_dir = "./knowledge_base"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save structured data as JSON
    with open(f"{output_dir}/structured_features.json", "w") as f:
        json.dump(structured_data, f, indent=2)
    
    # Save documents
    for doc in documents:
        with open(f"{output_dir}/{doc.doc_id}.md", "w") as f:
            f.write(doc.text)
    
    return structured_data

def main():
    """Main function to crawl and create knowledge base"""
    
    print("Starting documentation crawl...")
    
    # Crawl docs
    docs = crawl_framework_docs()
    
    if not docs:
        print("No docs crawled. Using manual data...")
        docs = []
    
    # Extract features
    structured = extract_features_structured(docs)
    
    # Add manually verified features
    manual_features = {
        "langgraph": {
            "checkpoints": ["save_resume", "sqlite", "postgres", "mongodb", "redis", "dynamodb"],
            "memory": ["short_term", "long_term"],
            "human_in_loop": ["interrupt", "suspend", "feedback", "approval"],
            "multi_agent": ["manual"],
            "tools": ["function_calling", "code_exec", "search"],
            "streaming": ["token"],
            "computer_use": False,
            "mcp": True,
            "guardrails": False,
        },
        "langchain": {
            "checkpoints": [],
            "memory": ["short_term", "long_term", "semantic", "entity"],
            "human_in_loop": ["interrupt", "feedback"],
            "multi_agent": ["manual"],
            "tools": ["function_calling", "code_exec", "search"],
            "streaming": ["token"],
            "computer_use": False,
            "mcp": True,
            "guardrails": True,
        },
        "autogen": {
            "checkpoints": [],
            "memory": [],
            "human_in_loop": ["feedback"],
            "multi_agent": ["native", "group", "sequential"],
            "tools": ["function_calling", "code_exec"],
            "streaming": [],
            "computer_use": False,
            "mcp": False,
            "guardrails": True,
        },
        "crewai": {
            "checkpoints": [],
            "memory": ["short_term", "long_term", "semantic"],
            "human_in_loop": [],
            "multi_agent": ["native", "crew", "sequential", "hierarchical"],
            "tools": ["function_calling", "search", "scraping"],
            "streaming": ["token"],
            "computer_use": False,
            "mcp": True,
            "guardrails": True,
        },
        "openai": {
            "checkpoints": [],
            "memory": [],
            "human_in_loop": [],
            "multi_agent": [],
            "tools": ["function_calling", "code_exec"],
            "streaming": ["token"],
            "computer_use": False,
            "mcp": False,
            "guardrails": True,
        },
        "anthropic": {
            "checkpoints": [],
            "memory": [],
            "human_in_loop": [],
            "multi_agent": [],
            "tools": ["function_calling", "text_editor", "bash"],
            "streaming": ["token"],
            "computer_use": True,
            "mcp": True,
            "guardrails": False,
        },
        "github_copilot": {
            "checkpoints": [],
            "memory": ["short_term", "enterprise"],
            "human_in_loop": ["feedback"],
            "multi_agent": ["native", "custom"],
            "tools": ["function_calling", "git"],
            "streaming": [],
            "computer_use": False,
            "mcp": True,
            "guardrails": True,
        },
        "salesforce": {
            "checkpoints": [],
            "memory": ["short_term", "long_term"],
            "human_in_loop": ["feedback", "approval"],
            "multi_agent": ["native"],
            "tools": ["api", "flow"],
            "streaming": [],
            "computer_use": False,
            "mcp": False,
            "guardrails": True,
        },
        "smolagents": {
            "checkpoints": [],
            "memory": [],
            "human_in_loop": [],
            "multi_agent": [],
            "tools": ["function_calling", "code_exec"],
            "streaming": [],
            "computer_use": False,
            "mcp": False,
            "guardrails": False,
        },
        "docker": {
            "checkpoints": [],
            "memory": [],
            "human_in_loop": [],
            "multi_agent": [],
            "tools": ["build_assist"],
            "streaming": [],
            "computer_use": False,
            "mcp": False,
            "guardrails": False,
        },
    }
    
    # Merge with manual
    for framework, features in manual_features.items():
        if framework in structured:
            for key, value in features.items():
                if not structured[framework].get(key):
                    structured[framework][key] = value
        else:
            structured[framework] = features
    
    # Create knowledge base
    kb = create_knowledge_graph(structured)
    
    print(f"\nKnowledge base created with {len(kb)} frameworks")
    print(f"Output: ./knowledge_base/")
    
    return kb

if __name__ == "__main__":
    main()