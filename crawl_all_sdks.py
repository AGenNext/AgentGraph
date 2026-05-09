"""
Crawl ALL agent framework SDKs from GitHub
Get endpoints + schemas from actual source code
"""

import requests
import re
import json

FRAMEWORKS = {
    "langgraph": {
        "owner": "langchain-ai",
        "repo": "langgraph",
        "path": "libs/sdk-py/langgraph_sdk",
        "files": ["schema.py", "_sync/assistants.py", "_sync/threads.py", "_sync/runs.py", "_sync/store.py", "_sync/cron.py"],
    },
    "openai": {
        "owner": "openai",
        "repo": "openai-python",
        "path": "src/openai",
        "files": ["_client.py", "agents.py"],
    },
    "anthropic": {
        "owner": "anthropics",
        "repo": "anthropic-sdk-python",
        "path": "src/anthropic",
        "files": ["_client.py"],
    },
    "google_adk": {
        "owner": "google",
        "repo": "adk-agentkit",
        "path": "google_adk",
        "files": ["agent.py", "runner.py", "session.py"],
    },
}

GITHUB_RAW = "https://raw.githubusercontent.com/{owner}/{repo}/main/{path}/{file}"
GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"

def get_methods(content):
    """Extract def/class from Python"""
    methods = re.findall(r'^\s*(def |async def |class )(\w+)', content, re.M)
    return methods

def get_schemas(content):
    """Extract TypedDict schemas"""
    schemas = {}
    pattern = r'class (\w+)\(TypedDict.*?\):(.*?)(?=\nclass |\Z)'
    for name, body in re.findall(pattern, content, re.S):
        fields = re.findall(r'^\s+(\w+):', body, re.M)
        if fields:
            schemas[name] = fields
    return schemas

def crawl_framework(name, config):
    results = {"endpoints": [], "schemas": {}}
    owner, repo, path = config["owner"], config["repo"], config["path"]
    
    for file in config["files"]:
        url = GITHUB_RAW.format(owner=owner, repo=repo, path=path, file=file)
        print(f"  {name}: {file}")
        
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                # Get methods/classes
                symbols = get_methods(resp.text)
                results["endpoints"].extend(symbols)
                
                # Get schemas
                schemas = get_schemas(resp.text)
                results["schemas"].update(schemas)
        except Exception as e:
            print(f"    Error: {e}")
    
    return results

def main():
    print("=== Crawling ALL Framework SDKs ===")
    all_results = {}
    
    for name, config in FRAMEWORKS.items():
        print(f"\n=== {name.upper()} ===")
        try:
            all_results[name] = crawl_framework(name, config)
        except Exception as e:
            print(f"Error: {e}")
    
    # Summarize
    print("\n=== Summary ===")
    for name, data in all_results.items():
        n_endpoints = len(data.get("endpoints", []))
        n_schemas = len(data.get("schemas", {}))
        print(f"{name}: {n_endpoints} endpoints, {n_schemas} schemas")
    
    with open("knowledge_base/all_sdks_api.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("\nSaved to knowledge_base/all_sdks_api.json")

if __name__ == "__main__":
    main()