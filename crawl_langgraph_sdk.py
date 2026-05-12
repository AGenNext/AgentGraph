"""
Crawl LangGraph SDK from GitHub - APIs + Schemas
"""

import requests
import re
import json
from typing import Dict, List

GITHUB_RAW = "https://raw.githubusercontent.com/langchain-ai/langgraph/main/libs/sdk-py/langgraph_sdk"

SDK_MODULES = {
    "_async/assistants.py": "AssistantsClient",
    "_async/threads.py": "ThreadsClient", 
    "_async/runs.py": "RunsClient",
    "_async/store.py": "StoreClient",
    "_async/cron.py": "CronClient",
}

def get_methods(content: str) -> List[str]:
    methods = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('def ') or line.startswith('async def '):
            match = re.match(r'(async def |def )(\w+)', line)
            if match:
                methods.append(match.group(2))
    return methods

def get_schemas(content: str) -> Dict:
    """Extract TypedDict schemas"""
    schemas = {}
    pattern = r'class (\w+)\(TypedDict.*?\):(.*?)(?=\nclass |\Z)'
    classes = re.findall(pattern, content, re.S)
    for name, body in classes:
        fields = re.findall(r'^\s+(\w+):', body, re.M)
        if fields:
            schemas[name] = fields
    return schemas

def crawl_sdk() -> Dict:
    results = {"endpoints": {}, "schemas": {}}
    
    # Get endpoints from each module
    for path, client_name in SDK_MODULES.items():
        url = f"{GITHUB_RAW}/{path}"
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                methods = get_methods(resp.text)
                results["endpoints"][client_name] = [m for m in methods if m != '__init__']
        except Exception as e:
            print(f"Error: {e}")
    
    # Get schemas from schema.py
    url = f"{GITHUB_RAW}/schema.py"
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            results["schemas"] = get_schemas(resp.text)
            print(f"Found {len(results['schemas'])} schemas")
    except Exception as e:
        print(f"Error: {e}")
    
    return results

def main():
    print("=== Crawling LangGraph SDK ===")
    results = crawl_sdk()
    
    total_endpoints = sum(len(m) for m in results["endpoints"].values())
    total_schemas = len(results["schemas"])
    print(f"\n=== {total_endpoints} endpoints, {total_schemas} schemas ===")
    
    with open("knowledge_base/langgraph_sdk_api.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Saved to knowledge_base/langgraph_sdk_api.json")

if __name__ == "__main__":
    main()