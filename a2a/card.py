"""Agent card for capability discovery."""

from typing import Optional
from .messages import AgentCard, AgentCapability, AgentSkill


# Predefined agent cards for each team member

OPENAI_AGENT_CARD = AgentCard(
    agentId="openai-creative-writer",
    name="OpenAI Creative Writer",
    description="Creative content writerSpecializing in storytelling, blog posts, and engaging narratives",
    url="http://localhost:8001",
    version="1.0.0",
    capabilities=[
        AgentCapability(
            name="generate_creative",
            description="Generate creative and engaging content"
        ),
        AgentCapability(
            name="write_blog",
            description="Write blog posts and articles"
        ),
        AgentCapability(
            name="storytelling",
            description="Create compelling narratives"
        ),
    ],
    skills=[
        AgentSkill(
            id="creative-writing",
            name="Creative Writing",
            description="Generate imaginative, engaging creative content",
            tags=["creative", "blog", "story"]
        ),
    ]
)

SALESFORCE_AGENT_CARD = AgentCard(
    agentId="salesforce-sales-writer",
    name="Salesforce Sales Writer",
    description="Sales and business content writer with CRM integration",
    url="http://localhost:8002",
    version="1.0.0",
    capabilities=[
        AgentCapability(
            name="sales_copy",
            description="Generate compelling sales copy"
        ),
        AgentCapability(
            name="business_content",
            description="Create business-focused content"
        ),
        AgentCapability(
            name="crm_integration",
            description="Integrate with Salesforce CRM data"
        ),
    ],
    skills=[
        AgentSkill(
            id="sales-writing",
            name="Sales Writing",
            description="Generate persuasive sales and marketing copy",
            tags=["sales", "marketing", "business"]
        ),
    ]
)

MICROSOFT_AGENT_CARD = AgentCard(
    agentId="microsoft-enterprise-writer",
    name="Microsoft Enterprise Writer",
    description="Enterprise content writer with Microsoft 365 integration",
    url="http://localhost:8003",
    version="1.0.0",
    capabilities=[
        AgentCapability(
            name="enterprise_content",
            description="Generate enterprise-grade content"
        ),
        AgentCapability(
            name="technical_docs",
            description="Write technical documentation"
        ),
        AgentCapability(
            name="m365_integration",
            description="Integrate with Microsoft 365"
        ),
    ],
    skills=[
        AgentSkill(
            id="enterprise-writing",
            name="Enterprise Writing",
            description="Generate professional enterprise content",
            tags=["enterprise", "technical", "docs"]
        ),
    ]
)

GOOGLE_AGENT_CARD = AgentCard(
    agentId="google-research-writer",
    name="Google Research Writer",
    description="Research and SEO content writer using Gemini",
    url="http://localhost:8004",
    version="1.0.0",
    capabilities=[
        AgentCapability(
            name="research_content",
            description="Generate research-based content"
        ),
        AgentCapability(
            name="seo_optimization",
            description="Optimize content for SEO"
        ),
        AgentCapability(
            name="factual_writing",
            description="Write factually accurate content"
        ),
    ],
    skills=[
        AgentSkill(
            id="research-writing",
            name="Research Writing",
            description="Generate research-backed content",
            tags=["research", "seo", "facts"]
        ),
    ]
)

DOCKER_AGENT_CARD = AgentCard(
    agentId="docker-devops-writer",
    name="Docker DevOps Writer",
    description="Docker & Kubernetes content specialist",
    url="http://localhost:8005",
    version="1.0.0",
    capabilities=[
        AgentCapability(
            name="dockerfile_content",
            description="Generate Dockerfiles"
        ),
        AgentCapability(
            name="docker_compose",
            description="Generate compose files"
        ),
        AgentCapability(
            name="kubernetes_yaml",
            description="Generate K8s manifests"
        ),
        AgentCapability(
            name="devops_docs",
            description="Write DevOps documentation"
        ),
    ],
    skills=[
        AgentSkill(
            id="docker-writing",
            name="Docker Writing",
            description="Generate Docker configs",
            tags=["docker", "kubernetes", "devops"]
        ),
    ]
)

GITHUB_AGENT_CARD = AgentCard(
    agentId="github-dev-writer",
    name="GitHub Developer Writer",
    description="GitHub content specialist",
    url="http://localhost:8006",
    version="1.0.0",
    capabilities=[
        AgentCapability(
            name="readme_docs",
            description="Generate READMEs"
        ),
        AgentCapability(
            name="pr_descriptions",
            description="Generate PR descriptions"
        ),
        AgentCapability(
            name="github_actions",
            description="Generate GitHub Actions"
        ),
    ],
    skills=[
        AgentSkill(
            id="github-writing",
            name="GitHub Writing",
            description="Generate GitHub content",
            tags=["github", "markdown", "ci-cd"]
        ),
    ]
)

OPENHANDS_AGENT_CARD = AgentCard(
    agentId="openhands-sdk-writer",
    name="OpenHands SDK Writer",
    description="OpenHands agent SDK specialist",
    url="http://localhost:8007",
    version="1.0.0",
    capabilities=[
        AgentCapability(name="agent_code", description="Generate agent code"),
        AgentCapability(name="tool_definition", description="Generate tool definitions"),
        AgentCapability(name="skill_creation", description="Create skills"),
    ],
    skills=[AgentSkill(id="openhands-dev", name="OpenHands Development", description="Generate OpenHands code", tags=["agent", "sdk"])],
)

LLAMAINDEX_AGENT_CARD = AgentCard(
    agentId="llamaindex-writer",
    name="LlamaIndex Agent Writer",
    description="Data-augmented LLM agents - RAG, query engines",
    url="http://localhost:8008",
    version="1.0.0",
    capabilities=[
        AgentCapability(name="query_engine", description="Generate query engines"),
        AgentCapability(name="data_agent", description="Create data agents"),
        AgentCapability(name="chat_engine", description="Build chat engines"),
    ],
    skills=[AgentSkill(id="llamaindex", name="LlamaIndex RAG", description="Build RAG agents", tags=["rag", "data-querying"])],
)

LANGCHAIN_AGENT_CARD = AgentCard(
    agentId="langchain-writer",
    name="LangChain Agent Writer",
    description="LangChain agents, chains, tools, memory",
    url="http://localhost:8009",
    version="1.0.0",
    capabilities=[
        AgentCapability(name="agent_definition", description="Create agents"),
        AgentCapability(name="chain_creation", description="Build chains"),
        AgentCapability(name="tool_integration", description="Integrate tools"),
    ],
    skills=[AgentSkill(id="langchain", name="LangChain Development", description="Build LangChain agents", tags=["chain", "llm"])],
)

COORDINATOR_AGENT_CARD = AgentCard(
    agentId="team-coordinator",
    name="Team Coordinator",
    description="Orchestrates multi-agent team for content collaboration",
    url="http://localhost:8000",
    version="1.0.0",
    capabilities=[
        AgentCapability(
            name="coordinate_team",
            description="Coordinate team of agents"
        ),
        AgentCapability(
            name="delegate_tasks",
            description="Delegate tasks to appropriate agents"
        ),
        AgentCapability(
            name="synthesize_results",
            description="Synthesize results from multiple agents"
        ),
    ],
    skills=[
        AgentSkill(
            id="team-coordination",
            name="Team Coordination",
            description="Orchestrate multi-agent content generation",
            tags=["coordination", "team", "orchestration"]
        ),
    ]
)


# Registry for agent cards
AGENT_CARDS = {
    "openai-creative-writer": OPENAI_AGENT_CARD,
    "salesforce-sales-writer": SALESFORCE_AGENT_CARD,
    "microsoft-enterprise-writer": MICROSOFT_AGENT_CARD,
    "google-research-writer": GOOGLE_AGENT_CARD,
    "docker-devops-writer": DOCKER_AGENT_CARD,
    "github-dev-writer": GITHUB_AGENT_CARD,
    "openhands-sdk-writer": OPENHANDS_AGENT_CARD,
    "team-coordinator": COORDINATOR_AGENT_CARD,
}


def get_agent_card(agent_id: str) -> Optional[AgentCard]:
    """Get an agent card by ID."""
    return AGENT_CARDS.get(agent_id)


def get_all_agent_cards() -> list[AgentCard]:
    """Get all registered agent cards."""
    return list(AGENT_CARDS.values())


def get_agents_by_skill(skill_tag: str) -> list[AgentCard]:
    """Get agents that have a specific skill tag."""
    return [
        card for card in AGENT_CARDS.values()
        if any(skill_tag in skill.tags for skill in card.skills)
    ]


def find_agent_for_capability(capability: str) -> Optional[AgentCard]:
    """Find an agent that supports a specific capability."""
    for card in AGENT_CARDS.values():
        if any(cap.name == capability for cap in card.capabilities):
            return card
    return None