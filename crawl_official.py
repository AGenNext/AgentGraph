"""
Crawl official agent framework documentation and create structured data
Uses official docs URLs - NO search results
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin
from typing import Dict, List, Optional
import re

# OFFICIAL DOCUMENTATION URLs - Directly from each framework's website
OFFICIAL_DOCS = {
    # Core Agent Frameworks
    "langgraph": {
        "name": "LangGraph",
        "base_url": "https://docs.langgraph.ai",
        "doc_urls": [
            "https://docs.langgraph.ai/concepts/",
            "https://docs.langgraph.ai/how-to/",
        ],
        "features_page": "https://docs.langgraph.ai/concepts/",
    },
    "langchain": {
        "name": "LangChain",
        "base_url": "https://python.langchain.com",
        "doc_urls": [
            "https://python.langchain.com/docs/concepts/",
            "https://python.langchain.com/docs/modules/",
        ],
        "features_page": "https://python.langchain.com/docs/concepts/",
    },
    "autogen": {
        "name": "AutoGen",
        "base_url": "https://microsoft.github.io/autogen",
        "doc_urls": [
            "https://microsoft.github.io/autogen/docs/",
            "https://microsoft.github.io/autogen/docs/Use-Cases/",
        ],
        "features_page": "https://microsoft.github.io/autogen/docs/",
    },
    "crewai": {
        "name": "CrewAI",
        "base_url": "https://docs.crewai.com",
        "doc_urls": [
            "https://docs.crewai.com/",
            "https://docs.crewai.com/core-functionality/",
        ],
        "features_page": "https://docs.crewai.com/",
    },
    "openai": {
        "name": "OpenAI Agents SDK",
        "base_url": "https://platform.openai.com",
        "doc_urls": [
            "https://platform.openai.com/docs/agents",
            "https://platform.openai.com/docs/agents/quickstart",
        ],
        "features_page": "https://platform.openai.com/docs/agents",
    },
    "anthropic": {
        "name": "Anthropic Claude",
        "base_url": "https://docs.anthropic.com",
        "doc_urls": [
            "https://docs.anthropic.com/en/docs/",
            "https://docs.anthropic.com/en/docs/build-with-claude/tool-use",
            "https://docs.anthropic.com/en/docs/build-with-claude/computer-use",
        ],
        "features_page": "https://docs.anthropic.com/en/docs/",
    },
    # DevOps Agent Tools
    "github_copilot": {
        "name": "GitHub Copilot",
        "base_url": "https://docs.github.com",
        "doc_urls": [
            "https://docs.github.com/en/copilot",
            "https://docs.github.com/en/copilot/tools-and-extensions",
        ],
        "features_page": "https://docs.github.com/en/copilot",
    },
    "docker": {
        "name": "Docker AI",
        "base_url": "https://docs.docker.com",
        "doc_urls": [
            "https://docs.docker.com/ai/",
            "https://docs.docker.com/desktop/",
        ],
        "features_page": "https://docs.docker.com/ai/",
    },
    # Cloud AI Platforms
    "salesforce": {
        "name": "Salesforce Agentforce",
        "base_url": "https://developer.salesforce.com",
        "doc_urls": [
            "https://developer.salesforce.com/docs/ai/agentforce/",
        ],
        "features_page": "https://developer.salesforce.com/docs/ai/agentforce/",
    },
    "google_vertex": {
        "name": "Google Vertex AI",
        "base_url": "https://cloud.google.com",
        "doc_urls": [
            "https://cloud.google.com/vertex-ai",
            "https://cloud.google.com/vertex-ai/docs/",
        ],
        "features_page": "https://cloud.google.com/vertex-ai/docs/",
    },
    # Specialized
    "smolagents": {
        "name": "SmolAgents",
        "base_url": "https://smolagents.ai",
        "doc_urls": [
            "https://smolagents.ai/",
        ],
        "features_page": "https://smolagents.ai/",
    },
    "mcp": {
        "name": "Model Context Protocol",
        "base_url": "https://modelcontextprotocol.io",
        "doc_urls": [
            "https://modelcontextprotocol.io/docs",
            "https://modelcontextprotocol.io/docs/server",
        ],
        "features_page": "https://modelcontextprotocol.io/docs",
    },
}

def fetch_page(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch a single page"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_features_from_html(html: str, framework: str) -> Dict:
    """Extract features from HTML using BeautifulSoup"""
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    
    # Get all headings
    headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])]
    
    return {
        "text": text[:50000],  # Limit text length
        "headings": headings,
        "raw_html": str(soup)[:20000],
    }

def crawl_official_docs() -> Dict:
    """Crawl all official documentation"""
    
    all_data = {}
    
    for framework_id, info in OFFICIAL_DOCS.items():
        print(f"\n=== Crawling {info['name']} ===")
        print(f"Base: {info['base_url']}")
        
        framework_data = {
            "name": info["name"],
            "framework_id": framework_id,
            "base_url": info["base_url"],
            "pages": {},
        }
        
        for doc_url in info["doc_urls"]:
            print(f"  Fetching: {doc_url}")
            html = fetch_page(doc_url)
            
            if html:
                features = extract_features_from_html(html, framework_id)
                page_name = doc_url.split('/')[-1] or "index"
                framework_data["pages"][page_name] = features
        
        all_data[framework_id] = framework_data
    
    return all_data

def analyze_features(crawled_data: Dict) -> Dict:
    """Analyze the crawled data to extract features"""
    
    feature_definitions = {
        "checkpoints": {
            "description": "Save and resume state",
            "keywords": ["checkpoint", "save state", "memory saver", "persist", "resume"],
        },
        "short_term_memory": {
            "description": "In-process memory",
            "keywords": ["memory", "inmemory", "buffer"],
        },
        "long_term_memory": {
            "description": "Persistent storage",
            "keywords": ["store", "postgres", "mongodb", "redis", "database"],
        },
        "semantic_memory": {
            "description": "Semantic/embedding-based memory",
            "keywords": ["semantic", "embedding", "recall"],
        },
        "human_interrupt": {
            "description": "Pause agent execution",
            "keywords": ["interrupt", "pause", "suspend"],
        },
        "human_feedback": {
            "description": "Request human input",
            "keywords": ["human input", "feedback", "user proxy"],
        },
        "approval_gates": {
            "description": "Require approval to proceed",
            "keywords": ["approval", "human-in-the-loop"],
        },
        "multi_agent": {
            "description": "Multiple agent orchestration",
            "keywords": ["multi-agent", "crew", "group chat", "team"],
        },
        "function_calling": {
            "description": "Tool/function calling",
            "keywords": ["function", "tool", "tool use"],
        },
        "code_interpreter": {
            "description": "Execute code",
            "keywords": ["code exec", "python repl", "interpreter"],
        },
        "web_search": {
            "description": "Search the web",
            "keywords": ["search", "serp", "google"],
        },
        "streaming": {
            "description": "Token-by-token streaming",
            "keywords": ["stream", "streaming"],
        },
        "computer_use": {
            "description": "Control computer directly",
            "keywords": ["computer use", "desktop", "mouse", "keyboard"],
        },
        "mcp": {
            "description": "Model Context Protocol",
            "keywords": ["mcp", "model context protocol"],
        },
        "guardrails": {
            "description": "Input/output validation",
            "keywords": ["guardrail", "validate", "policy"],
        },
    }
    
    analyzed = {}
    
    for framework_id, data in crawled_data.items():
        all_text = ""
        for page_data in data.get("pages", {}).values():
            all_text += page_data.get("text", "").lower() + " "
        
        features = {}
        for feature_id, feature_info in feature_definitions.items():
            features[feature_id] = False
            for keyword in feature_info["keywords"]:
                if keyword in all_text:
                    features[feature_id] = True
                    break
        
        analyzed[framework_id] = {
            "name": data["name"],
            "base_url": data["base_url"],
            "features": features,
            "pages_found": list(data.get("pages", {}).keys()),
        }
    
    return analyzed

def create_structured_knowledge(analyzed_data: Dict) -> str:
    """Create structured markdown knowledge base"""
    
    output = """# Agent Framework Knowledge Base

This document contains comprehensive feature comparisons for all major agent frameworks,
extracted from official documentation.

---

"""
    
    # Add each framework
    for framework_id, data in analyzed_data.items():
        output += f"## {data['name']}\n"
        output += f"**ID**: {framework_id}\n"
        output += f"**Docs**: {data['base_url']}\n\n"
        
        output += "### Features\n"
        output += "| Feature | Supported |\n"
        output += "|--------|----------|\n"
        
        for feature, supported in data.get("features", {}).items():
            output += f"| {feature} | {'✅' if supported else '❌'} |\n"
        
        output += "\n---\n\n"
    
    # Add comparison table
    output += "## Feature Comparison\n\n"
    output += "| Framework | Checkpoints | Memory | Human-in-Loop | Multi-Agent | Tools | Streaming | Computer Use | MCP |\n"
    output += "|-----------|-----------|--------|--------------|------------|-------|----------|-------------|-----|\n"
    
    for framework_id, data in analyzed_data.items():
        f = data.get("features", {})
        output += f"| {data['name']} "
        output += f"| {'✅' if f.get('checkpoints') else '❌'} "
        output += f"| {'✅' if f.get('short_term_memory') or f.get('long_term_memory') else '❌'} "
        output += f"| {'✅' if f.get('human_interrupt') or f.get('human_feedback') else '❌'} "
        output += f"| {'✅' if f.get('multi_agent') else '❌'} "
        output += f"| {'✅' if f.get('function_calling') else '❌'} "
        output += f"| {'✅' if f.get('streaming') else '❌'} "
        output += f"| {'✅' if f.get('computer_use') else '❌'} "
        output += f"| {'✅' if f.get('mcp') else '❌'} |\n"
    
    return output

def save_knowledge_base(analyzed_data: Dict, structured_md: str):
    """Save knowledge base to files"""
    
    output_dir = "./knowledge_base"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save JSON
    with open(f"{output_dir}/frameworks.json", "w") as f:
        json.dump(analyzed_data, f, indent=2)
    
    # Save markdown
    with open(f"{output_dir}/knowledge_base.md", "w") as f:
        f.write(structured_md)
    
    # Save individual framework docs
    for framework_id, data in analyzed_data.items():
        filename = f"{output_dir}/{framework_id}.md"
        with open(filename, "w") as f:
            f.write(f"# {data['name']}\n\n")
            f.write(f"Documentation: {data['base_url']}\n\n")
            f.write("## Features\n\n")
            for feature, supported in data.get("features", {}).items():
                f.write(f"- {feature}: {'Yes' if supported else 'No'}\n")

def main():
    """Main function"""
    
    print("=" * 60)
    print("CRAWLING OFFICIAL DOCUMENTATION")
    print("=" * 60)
    
    # Step 1: Crawl official docs
    crawled = crawl_official_docs()
    
    # Step 2: Analyze features
    analyzed = analyze_features(crawled)
    
    # Step 3: Create structured knowledge
    structured = create_structured_knowledge(analyzed)
    
    # Step 4: Save
    save_knowledge_base(analyzed, structured)
    
    print("\n" + "=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    print(f"Knowledge base saved to: ./knowledge_base/")
    print(f"  - frameworks.json (structured data)")
    print(f"  - knowledge_base.md (markdown)")
    print(f"  - {list(analyzed.keys())} individual docs")
    
    # Print summary
    print("\n=== SUMMARY ===")
    for fid, data in analyzed.items():
        print(f"\n{data['name']}:")
        features = [k for k, v in data.get("features", {}).items() if v]
        print(f"  Features: {', '.join(features)}")

if __name__ == "__main__":
    main()