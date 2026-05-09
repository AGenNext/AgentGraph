"""Registry System - Internal Decentralized IDs.

Internal DID format: did:content-team:{namespace}:{name}:v{version}

For WaltID blockchain integration (separate repo), use:
- WALTID_API_URL
- WALTID_API_KEY  
- WALTID_ISSUER_DID
"""

import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


def generate_did(namespace: str, name: str, version: str = "v1") -> str:
    return f"did:content-team:{namespace}:{name}:{version}"


def parse_did(did: str) -> Dict[str, str]:
    parts = did.split(":")
    if len(parts) >= 5:
        return dict(zip(["scheme", "authority", "namespace", "name", "version"], parts))
    return {}


@dataclass
class RegistryEntry:
    id: str
    name: str
    description: str
    namespace: str
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    version: str = "v1"


@dataclass
class SkillEntry(RegistryEntry):
    namespace: str = "skill"


@dataclass
class PromptEntry(RegistryEntry):
    namespace: str = "prompt"


@dataclass
class ToolEntry(RegistryEntry):
    namespace: str = "tool"
    framework: Optional[str] = None


class Registry:
    def __init__(self):
        self._skills: Dict[str, SkillEntry] = {}
        self._prompts: Dict[str, PromptEntry] = {}
        self._tools: Dict[str, ToolEntry] = {}
        self._load_builtins()
    
    def _load_builtins(self):
        # Built-in skills
        for sid, name, desc in [("coding", "Coding", "Generate code"), ("research", "Research", "Research")]:
            self._skills[sid] = SkillEntry(id=generate_did("skill", sid), name=name, description=desc, namespace="skill")
        # Built-in prompts
        for pid, name, desc in [("creative", "Creative Writing", "Creative content")]:
            self._prompts[pid] = PromptEntry(id=generate_did("prompt", pid), name=name, description=desc, namespace="prompt")
        
        # Framework tools (populated from integrations)
        framework_tools = [
            ("web_search", "Web Search", "Search the web for information", "langgraph"),
            ("langchain_code", "LangChain Code", "Generate LangChain code", "langchain"),
            ("autogen_code", "AutoGen Code", "Generate AutoGen agents", "autogen"),
            ("crewai_code", "CrewAI Code", "Generate CrewAI pipelines", "crewai"),
            ("openai_api", "OpenAI API", "Interact with OpenAI models", "openai"),
            ("anthropic_api", "Anthropic API", "Interact with Claude models", "anthropic"),
            ("google_search", "Google Search", "Search via Google", "google"),
            ("state_graph", "StateGraph", "Create state-based graphs", "langgraph"),
            ("react_agent", "ReAct Agent", "Reasoning + Action agent", "langgraph"),
            ("tool_use", "Tool Use", "Use tools in chains", "langchain"),
            ("memory", "Memory", "Persistent memory", "langchain"),
            ("streaming", "Streaming", "Stream agent output", "langgraph"),
        ]
        for tid, name, desc, fw in framework_tools:
            self._tools[tid] = ToolEntry(id=generate_did("tool", tid), name=name, description=desc, namespace="tool", framework=fw)
    
    def get_skill(self, name: str) -> Optional[SkillEntry]:
        return self._skills.get(name)
    def get_prompt(self, name: str) -> Optional[PromptEntry]:
        return self._prompts.get(name)
    def get_tool(self, name: str) -> Optional[ToolEntry]:
        return self._tools.get(name)
    def list_skills(self) -> List[SkillEntry]:
        return list(self._skills.values())
    def list_prompts(self) -> List[PromptEntry]:
        return list(self._prompts.values())
    def list_tools(self) -> List[ToolEntry]:
        return list(self._tools.values())


REGISTRY = Registry()


def get_registry() -> Registry:
    return REGISTRY
