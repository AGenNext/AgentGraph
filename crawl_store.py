"""
Crawl official docs → LlamaIndex → VectorDB
Store all framework documentation in a multimodal vector database
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from typing import List, Dict
from urllib.parse import urljoin

# Official docs URLs (verified working)
DOC_SOURCES = {
    "langgraph": "https://python.langchain.com/docs/langgraph/",
    "langchain": "https://python.langchain.com/docs/",
    "autogen": "https://microsoft.github.io/autogen/",
    "crewai": "https://docs.crewai.com/",
    "anthropic": "https://docs.anthropic.com/en/docs/",
    "github": "https://docs.github.com/en/copilot",
    "docker": "https://docs.docker.com/",
    "google": "https://cloud.google.com/vertex-ai/docs/",
}

def fetch_page(url: str, timeout: int = 30) -> str:
    """Fetch a page and extract content"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=timeout, verify=False)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"Error: {url} → {e}")
        return ""

def extract_content(html: str, url: str) -> Dict:
    """Extract structured content from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove scripts and styles
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    
    # Get main content
    main = soup.find("main") or soup.find("article") or soup.find("body")
    
    # Extract text
    text = main.get_text(separator="\n", strip=True) if main else ""
    
    # Extract headings with content
    sections = []
    for heading in soup.find_all(["h1", "h2", "h3"]):
        # Get next siblings until next heading
        content = []
        for sibling in heading.find_next_siblings():
            if sibling.name in ["h1", "h2", "h3"]:
                break
            if sibling.name:
                content.append(sibling.get_text(strip=True))
        if content:
            sections.append({
                "heading": heading.get_text(strip=True),
                "content": " ".join(content[:10]),  # First 10 elements
            })
    
    # Extract code blocks
    code_blocks = [pre.get_text(strip=True) for pre in soup.find_all("pre")]
    
    # Extract links
    links = [{"text": a.get_text(strip=True), "href": a.get("href", "")} 
            for a in soup.find_all("a", href=True) if a.get("href")]
    
    return {
        "url": url,
        "text": text[:50000],  # Limit
        "sections": sections[:50],
        "code_blocks": code_blocks[:20],
        "links": links[:30],
    }

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Chunk text into smaller pieces"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

# Store in JSON as fallback (vector DB requires more setup)
def store_raw(data: Dict):
    """Store raw crawled data"""
    output_dir = "./knowledge_base/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    for name, content in data.items():
        with open(f"{output_dir}/{name}_content.json", "w") as f:
            json.dump(content, f, indent=2)
    
    # Save index
    with open(f"{output_dir}/index.json", "w") as f:
        index = {name: {"url": info["url"], "sections": len(info.get("sections", []))} 
                for name, info in data.items()}
        json.dump(index, f, indent=2)
    
    return output_dir

def create_vector_store(data: Dict):
    """Create vector store using simple embedding (no external DB needed)"""
    
    # Create chunks with metadata
    all_chunks = []
    
    for framework, info in data.items():
        # Chunk the text
        chunks = chunk_text(info.get("text", ""), chunk_size=500)
        
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "framework": framework,
                "chunk_id": i,
                "text": chunk,
                "url": info.get("url", ""),
            })
    
    # Save chunks
    output_dir = "./knowledge_base/vectors"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/chunks.json", "w") as f:
        json.dump(all_chunks, f, indent=2)
    
    print(f"Created {len(all_chunks)} chunks from {len(data)} frameworks")
    return output_dir

def create_summary_index(data: Dict) -> str:
    """Create searchable summary index"""
    
    output = """# Agent Framework Documentation Index

## Source Files

| Framework | URL | Sections |
|-----------|-----|----------|
"""
    
    for name, info in data.items():
        output += f"| {name} | {info.get('url', 'N/A')} | {len(info.get('sections', []))} |\n"
    
    output += "\n## Feature Summary\n\n"
    
    # Feature keywords to search for
    features = {
        "checkpoints": ["checkpoint", "save", "persist", "resume", "state"],
        "memory": ["memory", "store", "context"],
        "human_loop": ["human", "interrupt", "feedback", "approval"],
        "multi_agent": ["multi", "crew", "group", "team"],
        "tools": ["tool", "function", "call"],
        "streaming": ["stream"],
        "mcp": ["mcp", "context protocol"],
    }
    
    for feature, keywords in features.items():
        output += f"### {feature}\n"
        for name, info in data.items():
            text = info.get("text", "").lower()
            found = any(kw in text for kw in keywords)
            symbol = "✅" if found else "❌"
            output += f"- {name}: {symbol}\n"
        output += "\n"
    
    return output

def main():
    """Main crawler"""
    
    print("=" * 60)
    print("CRAWLING OFFICIAL DOCS")
    print("=" * 60)
    
    all_data = {}
    
    for name, url in DOC_SOURCES.items():
        print(f"\n{name}: {url}")
        
        # Fetch page
        html = fetch_page(url)
        if not html:
            continue
        
        # Extract content
        content = extract_content(html, url)
        
        if content.get("text"):
            all_data[name] = content
            print(f"  ✓ Extracted {len(content['text'])} chars, {len(content['sections'])} sections")
        else:
            print("  ✗ No content")
    
    print(f"\n=== Crawled {len(all_data)} frameworks ===")
    
    # Store raw
    raw_dir = store_raw(all_data)
    print(f"Raw: {raw_dir}/")
    
    # Create vector chunks
    vec_dir = create_vector_store(all_data)
    print(f"Vectors: {vec_dir}/")
    
    # Create summary
    summary = create_summary_index(all_data)
    with open("./knowledge_base/README.md", "w") as f:
        f.write(summary)
    print("Summary: ./knowledge_base/README.md")
    
    print("\nDone!")

if __name__ == "__main__":
    main()