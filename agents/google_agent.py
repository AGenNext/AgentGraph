"""Google Agent SDK - References capabilities from registry."""

from typing import Optional, List, Callable, Any
import os

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig
from core.registry import REGISTRY


class ToolCallHooks:
    """Pre/post tool call hooks."""
    def __init__(self):
        self.pre = []
        self.post = []
    def on_before_tool(self, h): self.pre.append(h)
    def on_after_tool(self, h): self.post.append(h)


class GoogleAgent(BaseAgent):
    """Google Gemini agent - uses registry references.
    
    Preferred Model: gemini-2.0-flash
    
    Capabilities (from registry):
    - did:content-team:skill:research:v1
    - did:content-team:skill:seo:v1
    - did:content-team:skill:fact_checking:v1
    
    Tools (from registry):
    - did:content-team:tool:web_search:v1
    - did:content-team:tool:browser:v1
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            agent_id="google-research-writer",
            name="Google Research Writer",
            description="Research using Google Gemini with registry refs",
            capabilities=[],  # From registry
            skills=[],  # DID references
            api_key=api_key or os.getenv("GOOGLE_API_KEY"),
        )
        
        # Reference skills from registry by DID
        skill_ids = ["research", "seo", "fact_checking", "vision"]
        for sid in skill_ids:
            skill = REGISTRY.get_skill(sid)
            if skill:
                self.skills.append(skill.id)  # DID: did:content-team:skill:...
                self.capabilities.append(skill.description)
        
        self.llm_config = LLMConfig.from_env("google")
        self._llm = None
    
    def _get_port(self) -> int:
        return 8004
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _get_prompt(self, prompt_name: str) -> str:
        """Get prompt from registry."""
        prompt = REGISTRY.get_prompt(prompt_name)
        return prompt.template if prompt else ""
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        if "research" in ct:
            return self._research(request)
        elif "seo" in ct:
            return self._seo(request)
        else:
            return self._default(request)
    
    def _get_skill_did(self, skill_name: str) -> str:
        """Get skill DID reference."""
        skill = REGISTRY.get_skill(skill_name)
        return skill.id if skill else f"did:content-team:skill:{skill_name}:v1"
    
    def _research(self, request: ContentRequest) -> ContentResult:
        # Get prompt template from registry
        tmpl = self._get_prompt("analysis") or "Analyze: {topic}"
        prompt = tmpl.format(topic=request.topic)
        
        llm = self._get_llm()
        skill_did = self._get_skill_did("research")
        
        if llm.is_available:
            content = llm.generate(prompt, system_prompt="Research assistant")
            return ContentResult(
                content=content,
                agent_id=self.agent_id,
                quality_score=0.90,
                metadata={"skill_ref": skill_did},
            )
        
        return ContentResult(
            content=f"# Research: {request.topic}\n[Google Gemini]",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"skill_ref": skill_did},
        )
    
    def _seo(self, request: ContentRequest) -> ContentResult:
        skill_did = self._get_skill_did("seo")
        return ContentResult(
            content=f"# SEO: {request.topic}\n[SEO content]",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"skill_ref": skill_did},
        )
    
    def _default(self, request: ContentRequest) -> ContentResult:
        skill_did = self._get_skill_did("fact_checking")
        return ContentResult(
            content=f"# {request.topic}\n[Content]",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"skill_ref": skill_did},
        )