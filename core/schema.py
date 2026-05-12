"""Agent Schema - Standard definition of all agent attributes."""

from typing import List, Optional, Dict, Any, Literal
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# Core Enums
# ============================================================================

class AgentStatus(Enum):
    """Agent lifecycle status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROVISIONING = "provisioning"
    STOPPED = "stopped"
    ERROR = "error"


class AgentTier(Enum):
    """Pricing tier."""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class AuthType(Enum):
    """Authentication type."""
    NONE = "none"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    IAM = "iam"
    JWT = "jwt"


class StreamingMode(Enum):
    """Streaming response mode."""
    NONE = "none"
    LINES = "lines"
    SSE = "sse"


# ============================================================================
# Agent Metadata
# ============================================================================

@dataclass
class AgentMetadata:
    """Complete agent metadata."""
    
    # Identity
    id: str
    name: str
    description: str
    version: str = "1.0.0"
    status: AgentStatus = AgentStatus.ACTIVE
    
    # Provider
    provider: Optional[str] = None  # e.g., "openai", "anthropic"
    provider_model: Optional[str] = None  # e.g., "gpt-4o"
    
    # URLs
    url: str = "http://localhost:8000"
    documentation_url: Optional[str] = None
    
    # Timestamps
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    # Visibility
    is_public: bool = True
    tier: AgentTier = AgentTier.FREE
    
    # Limits
    rate_limit: Optional[int] = None  # requests per minute
    max_concurrent: Optional[int] = None
    
    # Tags
    tags: List[str] = field(default_factory=list)


# ============================================================================
# Capabilities
# ============================================================================

@dataclass
class Capability:
    """Single capability definition."""
    
    name: str  # e.g., "code_generation", "image_understanding"
    description: str
    
    # Input/Output
    input_modes: List[str] = field(default_factory=lambda: ["text"])
    output_modes: List[str] = field(default_factory=lambda: ["text"])
    
    # Constraints
    max_tokens: Optional[int] = None
    context_window: Optional[int] = None
    
    # Features
    streaming: bool = False
    function_calling: bool = False
    json_output: bool = False
    supports_vision: bool = False
    
    # Custom params
    parameters: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Skills
# ============================================================================

@dataclass
class Skill:
    """Skill definition."""
    
    id: str  # e.g., "coding", "creative_writing"
    name: str
    description: str
    
    # Categorization
    category: Optional[str] = None  # e.g., "programming", "writing"
    tags: List[str] = field(default_factory=list)
    
    # Examples
    examples: List[str] = field(default_factory=list)
    
    # Configuration
    config: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Tools
# ============================================================================

@dataclass
class Tool:
    """Tool definition."""
    
    name: str
    description: str
    
    # Type
    type: str = "function"  # "function", "browser", "code_interpreter"
    
    # Parameters
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Auth
    auth_type: AuthType = AuthType.NONE
    requires_auth: bool = False
    
    # Categories
    category: Optional[str] = None  # "search", "computation", "communication"


# ============================================================================
# Toolsets
# ============================================================================

@dataclass
class Toolset:
    """Collection of tools."""
    
    id: str
    name: str
    description: str
    
    tools: List[Tool] = field(default_factory=list)
    
    # Scope
    is_builtin: bool = False
    is_global: bool = True


# ============================================================================
# Model Config
# ============================================================================

@dataclass
class ModelConfig:
    """LLM configuration."""
    
    provider: str  # "openai", "anthropic", etc.
    model: str  # "gpt-4o", "claude-3", etc.
    
    # Generation
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 1.0
    top_k: Optional[int] = None
    
    # Context
    context_window: int = 128000
    
    # Safety
    content_filter: bool = True
    
    # Advanced
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    
    # Custom
    extra_params: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Authentication
# ============================================================================

@dataclass
class AuthConfig:
    """Authentication configuration."""
    
    type: AuthType
    required: bool = True
    
    # For API_KEY
    api_key_header: Optional[str] = None
    
    # For OAuth2
    auth_url: Optional[str] = None
    token_url: Optional[str] = None
    scopes: List[str] = field(default_factory=list)
    
    # For IAM/JWT
    issuer: Optional[str] = None
    audience: Optional[str] = None


# ============================================================================
# Input/Output Schema
# ============================================================================

@dataclass
class InputSchema:
    """Input format specification."""
    
    type: str = "object"
    properties: Dict[str, Any] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)


@dataclass
class OutputSchema:
    """Output format specification."""
    
    type: str = "object"
    properties: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Agent Card (A2A Protocol)
# ============================================================================

@dataclass
class AgentCard:
    """Complete agent card for A2A protocol."""
    
    # Identity
    agent_id: str
    name: str
    description: str
    url: str
    
    # Version
    version: str = "1.0.0"
    
    # Provider
    provider: Optional[str] = None
    model: Optional[str] = None
    
    # Capabilities & Skills
    capabilities: List[Capability] = field(default_factory=list)
    skills: List[Skill] = field(default_factory=list)
    tools: List[Tool] = field(default_factory=list)
    toolsets: List[Toolset] = field(default_factory=list)
    
    # Model
    model_config: Optional[ModelConfig] = None
    
    # Auth
    auth: Optional[AuthConfig] = None
    
    # I/O Schema
    input_schema: Optional[InputSchema] = None
    output_schema: Optional[OutputSchema] = None
    
    # Features
    streaming: bool = False
    function_calling: bool = False
    supports_vision: bool = False
    
    # Limits
    rate_limit: Optional[int] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "version": self.version,
            "provider": self.provider,
            "model": self.model,
            "capabilities": [
                {"name": c.name, "description": c.description}
                for c in self.capabilities
            ],
            "skills": [
                {"id": s.id, "name": s.name, "description": s.description}
                for s in self.skills
            ],
            "streaming": self.streaming,
            "function_calling": self.function_calling,
            "supports_vision": self.supports_vision,
        }


# ============================================================================
# Complete Agent Definition
# ============================================================================

@dataclass
class Agent:
    """Complete agent definition."""
    
    # Core (required)
    id: str
    name: str
    description: str
    
    # Identity
    card: AgentCard
    
    # Implementation
    entry_point: Optional[str] = None
    code: Optional[str] = None
    
    # Configuration
    model_config: Optional[ModelConfig] = None
    auth_config: Optional[AuthConfig] = None
    
    # Plugins
    toolsets: List[Toolset] = field(default_factory=list)
    
    # State
    status: AgentStatus = AgentStatus.ACTIVE
    is_active: bool = True
    
    # Limits
    max_retries: int = 3
    timeout: int = 300
    
    # Custom
    extensions: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "card": self.card.to_dict() if self.card else None,
        }


# ============================================================================
# Standard Skill Library
# ============================================================================

# Pre-defined standard skills
STANDARD_SKILLS = {
    # Programming
    "coding": Skill(
        id="coding",
        name="Coding",
        description="Generate code in various programming languages",
        category="programming",
        tags=["code", "programming", "development"],
    ),
    "code_review": Skill(
        id="code_review",
        name="Code Review",
        description="Review and critique code",
        category="programming",
        tags=["code", "review", "quality"],
    ),
    "debugging": Skill(
        id="debugging",
        name="Debugging",
        description="Find and fix bugs",
        category="programming",
        tags=["bug", "fix", "debug"],
    ),
    
    # Writing
    "creative_writing": Skill(
        id="creative_writing",
        name="Creative Writing",
        description="Write creative content like stories, poems",
        category="writing",
        tags=["story", "poetry", "creative"],
    ),
    "technical_writing": Skill(
        id="technical_writing",
        name="Technical Writing",
        description="Write technical documentation",
        category="writing",
        tags=["docs", "technical", "api"],
    ),
    "copywriting": Skill(
        id="copywriting",
        name="Copywriting",
        description="Write marketing copy",
        category="writing",
        tags=["marketing", "sales", "ads"],
    ),
    
    # Analysis
    "data_analysis": Skill(
        id="data_analysis",
        name="Data Analysis",
        description="Analyze and interpret data",
        category="analysis",
        tags=["data", "statistics", "insights"],
    ),
    "financial_analysis": Skill(
        id="financial_analysis",
        name="Financial Analysis",
        description="Analyze financial data",
        category="analysis",
        tags=["finance", "investment", "stocks"],
    ),
    "market_research": Skill(
        id="market_research",
        name="Market Research",
        description="Research market trends",
        category="analysis",
        tags=["market", "research", "trends"],
    ),
    
    # Reasoning
    "reasoning": Skill(
        id="reasoning",
        name="Logical Reasoning",
        description="Logical reasoning and problem solving",
        category="reasoning",
        tags=["logic", "problem_solving"],
    ),
    "math": Skill(
        id="math",
        name="Mathematics",
        description="Solve math problems",
        category="reasoning",
        tags=["math", "calculation"],
    ),
    
    # Search
    "web_search": Skill(
        id="web_search",
        name="Web Search",
        description="Search the web",
        category="search",
        tags=["search", "browsing"],
    ),
    "research": Skill(
        id="research",
        name="Research",
        description="Research topics thoroughly",
        category="search",
        tags=["research", "facts"],
    ),
    
    # RAG
    "rag": Skill(
        id="rag",
        name="RAG",
        description="Retrieval-augmented generation",
        category="rag",
        tags=["retrieval", "knowledge"],
    ),
    "document_search": Skill(
        id="document_search",
        name="Document Search",
        description="Search documents",
        category="rag",
        tags=["document", "search"],
    ),
    
    # Multimodal
    "vision": Skill(
        id="vision",
        name="Image Understanding",
        description="Understand images",
        category="multimodal",
        tags=["image", "vision"],
    ),
    "audio": Skill(
        id="audio",
        name="Audio Processing",
        description="Process audio",
        category="multimodal",
        tags=["audio", "speech"],
    ),
    
    # Communication
    "translation": Skill(
        id="translation",
        name="Translation",
        description="Translate between languages",
        category="communication",
        tags=["language", "translation"],
    ),
    "summarization": Skill(
        id="summarization",
        name="Summarization",
        description="Summarize content",
        category="communication",
        tags=["summary", " condensing"],
    ),
    
    # DevOps
    "docker": Skill(
        id="docker",
        name="Docker",
        description="Docker and containerization",
        category="devops",
        tags=["docker", "container"],
    ),
    "kubernetes": Skill(
        id="kubernetes",
        name="Kubernetes",
        description="Kubernetes orchestration",
        category="devops",
        tags=["k8s", "orchestration"],
    ),
    "ci_cd": Skill(
        id="ci_cd",
        name="CI/CD",
        description="Continuous integration/deployment",
        category="devops",
        tags=["ci", "cd", "automation"],
    ),
    
    # Enterprise
    "enterprise": Skill(
        id="enterprise",
        name="Enterprise",
        description="Enterprise-level features",
        category="enterprise",
        tags=["enterprise", "security"],
    ),
    "compliance": Skill(
        id="compliance",
        name="Compliance",
        description="Compliance and governance",
        category="enterprise",
        tags=["compliance", " governance"],
    ),
    "secure_processing": Skill(
        id="secure_processing",
        name="Secure Processing",
        description="Secure data processing",
        category="enterprise",
        tags=["security", "privacy"],
    ),
    
    # Platform-specific
    "aws": Skill(
        id="aws",
        name="AWS",
        description="Amazon Web Services",
        category="platform",
        tags=["aws", "cloud"],
    ),
    "azure": Skill(
        id="azure",
        name="Azure",
        description="Microsoft Azure",
        category="platform",
        tags=["azure", "cloud"],
    ),
    "gcp": Skill(
        id="gcp",
        name="Google Cloud",
        description="Google Cloud Platform",
        category="platform",
        tags=["gcp", "cloud"],
    ),
    
    # Database
    "sql": Skill(
        id="sql",
        name="SQL",
        description="SQL queries",
        category="database",
        tags=["sql", "database"],
    ),
    "nosql": Skill(
        id="nosql",
        name="NoSQL",
        description="NoSQL databases",
        category="database",
        tags=["mongodb", "database"],
    ),
}


# ============================================================================
# Standard Capability Library
# ============================================================================

STANDARD_CAPABILITIES = {
    # Text Generation
    "text_generation": Capability(
        name="text_generation",
        description="Generate text content",
        input_modes=["text"],
        output_modes=["text"],
        streaming=True,
    ),
    "code_generation": Capability(
        name="code_generation",
        description="Generate code",
        input_modes=["text"],
        output_modes=["text", "code"],
    ),
    
    # Vision
    "image_understanding": Capability(
        name="image_understanding",
        description="Understand images",
        input_modes=["image"],
        output_modes=["text"],
        supports_vision=True,
    ),
    
    # Function Calling
    "function_calling": Capability(
        name="function_calling",
        description="Call functions/tools",
        function_calling=True,
    ),
    
    # Structured Output
    "structured_output": Capability(
        name="structured_output",
        description="Output structured JSON",
        json_output=True,
    ),
    
    # Streaming
    "streaming": Capability(
        name="streaming",
        description="Stream responses",
        streaming=True,
    ),
    
    # Context
    "long_context": Capability(
        name="long_context",
        description="Handle long context",
        context_window=1000000,
    ),
}


# ============================================================================
# Standard Tool Library
# ============================================================================

STANDARD_TOOLS = {
    "web_search": Tool(
        name="web_search",
        description="Search the web",
        type="search",
    ),
    "code_executor": Tool(
        name="code_executor",
        description="Execute code",
        type="code_interpreter",
    ),
    "browser": Tool(
        name="browser",
        description="Browse web pages",
        type="browser",
    ),
    "calculator": Tool(
        name="calculator",
        description="Perform calculations",
        type="computation",
    ),
    "file_reader": Tool(
        name="file_reader",
        description="Read files",
        type="function",
    ),
    "file_writer": Tool(
        name="file_writer",
        description="Write files",
        type="function",
    ),
    "sql_executor": Tool(
        name="sql_executor",
        description="Execute SQL queries",
        type="function",
    ),
}