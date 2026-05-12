"""OpenAI-compatible Creative Writer Agent."""

from typing import Optional, Callable, Any, Literal
import os
import time
import logging

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig

logger = logging.getLogger(__name__)


# === OpenAI Product Variants ===
OpenAIProduct = Literal["chatgpt", "codex", "o1", "o3", "gpt4"]


# === Tool Call Hooks (same as Microsoft Agent) ===
class ToolCallHooks:
    """Pre/post tool call hooks for any agent."""
    
    def __init__(self):
        self.pre_hooks: list[Callable] = []
        self.post_hooks: list[Callable] = []
    
    def on_before_tool(self, hook: Callable): self.pre_hooks.append(hook)
    def on_after_tool(self, hook: Callable): self.post_hooks.append(hook)
    
    def run_pre(self, tool: str, inp: dict):
        for h in self.pre_hooks: h(tool, inp)
    
    def run_post(self, tool: str, inp: dict, out: Any):
        for h in self.post_hooks: h(tool, inp, out)


# === Swarm Mode for Multi-Agent Orchestration ===
class SwarmMode:
    """OpenAI Swarm - handoffs between agents."""
    
    def __init__(self):
        self.agents: dict[str, Any] = {}
        self.current_agent: str = None
    
    def add_agent(self, name: str, agent: Any):
        """Add agent to swarm."""
        self.agents[name] = agent
    
    def transfer_to(self, agent_name: str):
        """Handoff to another agent."""
        self.current_agent = agent_name
        return self.agents.get(agent_name)
    
    def run(self, prompt: str) -> str:
        """Run swarm with handoffs."""
        if not self.current_agent:
            return "No agent selected"
        agent = self.agents.get(self.current_agent)
        return f"Running {self.current_agent} with: {prompt}"


class OpenAIAgent(BaseAgent):
    """Creative content writer - works with ANY LLM (OpenAI, Ollama, LM Studio, etc.).
    
    Supports pre_tool_call_hook and post_tool_call_hook for monitoring.
    """
    
    @property
    def preferred_model(self) -> str:
        """Preferred LLM model for this agent."""
        return "gpt-4o" 
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        enable_hooks: bool = True,
        enable_swarm: bool = False,
        product: OpenAIProduct = "chatgpt",
    ):
        super().__init__(
            agent_id="openai-creative-writer",
            name="OpenAI Creative Writer",
            description="Creative content writer specializing in storytelling, blog posts",
            capabilities=["generate_creative", "write_blog", "storytelling"],
            skills=["creative-writing", "blog-writing", "storytelling"],
            api_key=api_key or os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY"),
        )
        
        # Support any LLM via flexible configuration
        self.llm_config = LLMConfig.from_env()
        
        # Override with passed parameters
        if base_url:
            self.llm_config.base_url = base_url
        if model:
            self.llm_config.model = model
        if api_key:
            self.llm_config.api_key = api_key
        if provider:
            self.llm_config.provider = provider
        
        self._llm = None
        
        # Tool call hooks
        self._hooks = ToolCallHooks() if enable_hooks else None
        
        # Swarm mode for multi-agent handoffs
        self._swarm = SwarmMode() if enable_swarm else None
        
        # Product variant (chatgpt, codex, o1, o3, gpt4)
        self.product = product
    
    @property
    def swarm(self) -> SwarmMode:
        """Access swarm mode for multi-agent orchestration."""
        return self._swarm
    
    @property
    def pre_tool_call_hook(self) -> Callable:
        """Register pre-tool-call hook."""
        return self._hooks.on_before_tool if self._hooks else None
    
    @property
    def post_tool_call_hook(self) -> Callable:
        """Register post-tool-call hook."""
        return self._hooks.on_after_tool if self._hooks else None
    
    def _get_port(self) -> int:
        return 8001
    
    def _get_llm(self) -> LLMClient:
        """Get or create the flexible LLM client."""
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        """Generate creative content using flexible LLM."""
        
        llm = self._get_llm()
        prompt = self._build_prompt(request)
        
        # Try to generate with LLM
        if llm.is_available:
            try:
                content = llm.generate(
                    prompt=prompt,
                    system_prompt="You are a creative content writer specializing in engaging, high-quality content.",
                    temperature=0.8,
                    max_tokens=2000,
                )
                
                # Check for error response
                if content.startswith("Error:"):
                    return self._mock_response(prompt, request)
                
                return ContentResult(
                    content=content,
                    agent_id=self.agent_id,
                    quality_score=0.9,
                    metadata={
                        "model": self.llm_config.model,
                        "provider": self.llm_config.provider,
                    },
                )
            except Exception as e:
                return self._mock_response(prompt, request)
        else:
            # Use mock response in demo mode
            return self._mock_response(prompt, request)
    
    def _build_prompt(self, request: ContentRequest) -> str:
        """Build the prompt based on request."""
        base = f"Write a {request.length} {request.content_type} about {request.topic}."
        
        if request.style:
            base += f" Style: {request.style}."
        
        if request.context.get("audience"):
            base += f" Target audience: {request.context['audience']}."
        
        return base
    
    def _mock_response(self, prompt: str, request: ContentRequest) -> ContentResult:
        """Mock response for demo mode."""
        
        templates = {
            "blog": f"""# {request.topic.title()}

## Introduction

In today's rapidly evolving landscape, {request.topic} has emerged as a crucial area 
of focus for professionals and enthusiasts alike. This comprehensive exploration 
delves into the intricacies and nuances that make this subject so compelling.

## Key Insights

Our analysis reveals several pivotal aspects worth exploring:

1. **Understanding the Fundamentals** - Building a strong foundation
2. **Practical Applications** - Real-world implementations
3. **Future Implications** - What's on the horizon

## Conclusion

The journey through {request.topic} reveals both challenges and opportunities. 
As we continue to navigate these waters, staying informed and adaptable remains key.

---

*Generated by {self.name}*""",
            
            "storytelling": f"""# The Story of {request.topic.title()}

Once upon a time, in a world not so different from our own, there existed a topic 
that captivated the imagination of all who encountered it: {request.topic}.

The tale begins with humble origins, Growing from a simple idea into something 
extraordinary through the power of creativity and dedication.

*To be continued...*

---

*Generated by {self.name}*""",
        }
        
        template = templates.get(request.content_type, templates["blog"])
        
        return ContentResult(
            content=template,
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"model": self.llm_config.model, "mock": True},
        )