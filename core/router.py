"""Content type router."""

from typing import Optional
from dataclasses import dataclass


@dataclass
class RouteResult:
    """Result of content routing."""
    
    primary_agent: str
    support_agents: list[str]
    content_type: str
    style: str = "professional"
    length: str = "medium"


class ContentRouter:
    """Routes content requests to appropriate agents."""
    
    # Agent capabilities mapping
    AGENT_CAPABILITIES = {
        "openai-creative-writer": {
            "content_types": ["blog", "storytelling", "creative", "social", "article"],
            "styles": ["casual", "professional", "humorous", "inspirational"],
        },
        "salesforce-sales-writer": {
            "content_types": ["sales", "marketing", "business", "promotional", "email"],
            "styles": ["persuasive", "professional", "urgent"],
        },
        "microsoft-enterprise-writer": {
            "content_types": ["technical_docs", "enterprise", "documentation", "report"],
            "styles": ["formal", "technical", "detailed"],
        },
        "google-research-writer": {
            "content_types": ["seo", "research", "factual", "educational"],
            "styles": ["informative", " factual", "educational"],
        },
    }
    
    # Content type to lead agent mapping
    CONTENT_TYPE_LEAD = {
        "blog": "openai-creative-writer",
        "storytelling": "openai-creative-writer",
        "creative": "openai-creative-writer",
        "social": "openai-creative-writer",
        "article": "openai-creative-writer",
        "sales": "salesforce-sales-writer",
        "marketing": "salesforce-sales-writer",
        "business": "salesforce-sales-writer",
        "promotional": "salesforce-sales-writer",
        "email": "salesforce-sales-writer",
        "technical_docs": "microsoft-enterprise-writer",
        "enterprise": "microsoft-enterprise-writer",
        "documentation": "microsoft-enterprise-writer",
        "report": "microsoft-enterprise-writer",
        "seo": "google-research-writer",
        "research": "google-research-writer",
        "factual": "google-research-writer",
        "educational": "google-research-writer",
    }
    
    # Multi-agent content types
    MULTI_AGENT_TYPES = {
        "comprehensive": ["openai", "google", "microsoft"],
        "campaign": ["salesforce", "google"],
        "full_article": ["openai", "google"],
        "enterprise_kit": ["salesforce", "microsoft", "google"],
    }
    
    def __init__(self):
        self.default_lead = "openai-creative-writer"
        self.default_support: list[str] = []
    
    def route(
        self,
        topic: str,
        content_type: str = "blog",
        style: str = "professional",
        enable_multi_agent: bool = False,
    ) -> RouteResult:
        """Route content to appropriate agent(s)."""
        
        # Determine primary agent
        primary = self.CONTENT_TYPE_LEAD.get(
            content_type, self.default_lead
        ).split("-")[0]
        
        # Determine support agents
        support = self._get_support_agents(content_type, enable_multi_agent)
        
        return RouteResult(
            primary_agent=primary,
            support_agents=support,
            content_type=content_type,
            style=style,
            length="medium",
        )
    
    def _get_support_agents(
        self,
        content_type: str,
        enable_multi_agent: bool = False,
    ) -> list[str]:
        """Get support agents for multi-agent collaboration."""
        
        if not enable_multi_agent:
            return []
        
        # Multi-agent support mapping
        support_mapping = {
            "blog": ["google"],  # SEO optimization
            "marketing": ["google", "microsoft"],  # Enterprise + SEO
            "enterprise": ["google"],  # Research
            "comprehensive": ["google", "microsoft"],
        }
        
        return support_mapping.get(content_type, [])
    
    def get_agent_for_capability(self, capability: str) -> Optional[str]:
        """Find agent that handles a specific capability."""
        
        for agent_id, caps in self.AGENT_CAPABILITIES.items():
            if capability in caps.get("content_types", []):
                return agent_id
        
        return None
    
    def get_all_routes(self) -> dict:
        """Get all available routes."""
        return self.CONTENT_TYPE_LEAD.copy()