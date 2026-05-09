"""
Crawl LangGraph SDK from GitHub to get all API endpoints
"""

import requests
import re
import json
from typing import Dict, List

# GitHub raw URL for LangGraph SDK
GITHUB_RAW = "https://raw.githubusercontent.com/langchain-ai/langgraph/main/libs/sdk-py/langgraph_sdk"

# SDK modules to crawl
SDK_MODULES = {
    "_async/assistants.py": "AssistantsClient",
    "_async/threads.py": "ThreadsClient", 
    "_async/runs.py": "RunsClient",
    "_async/store.py": "StoreClient",
    "_async/cron.py": "CronClient",
}

def get_methods(content: str) -> List[str]:
    """Extract method definitions from Python source"""
    methods = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('def ') or line.startswith('async def '):
            # Extract function name
            match = re.match(r'(async def |def )(\w+)', line)
            if match:
                methods.append(match.group(2))
    return methods

def crawl_sdk() -> Dict:
    """Crawl all SDK modules"""
    results = {}
    
    for path, client_name in SDK_MODULES.items():
        url = f"{GITHUB_RAW}/{path}"
        print(f"Fetching: {url}")
        
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                methods = get_methods(resp.text)
                results[client_name] = methods
                print(f"  Found {len(methods)} methods")
            else:
                print(f"  Failed: {resp.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
    
    return results

def main():
    print("=== Crawling LangGraph SDK ===")
    results = crawl_sdk()
    
    total = sum(len(m) for m in results.values())
    print(f"\n=== Total: {total} endpoints ===")
    
    # Save to file
    with open("knowledge_base/langgraph_sdk_endpoints.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Saved to knowledge_base/langgraph_sdk_endpoints.json")

if __name__ == "__main__":
    main()