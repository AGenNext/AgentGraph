"""
Agent Platform - Complete Schema.org Implementation

This module provides a complete agent platform using Schema.org types:
- Agent = SoftwareApplication
- Task = Action
- Owner = Person
- Organization = Organization (company/department)
- Skills = knowsLanguage
- Pricing = Offer
- Location = Place
- Events = Event
- Credentials = PropertyValue

References:
- Schema.org: https://schema.org
- NAICS (Industry): https://www.census.gov/naics/
- SOC (Job Roles): https://www.bls.gov/soc/
- ISO 4217 (Currency): https://www.iso.org/iso-4217-currency-codes.html
- IETF BCP 47 (Languages): https://tools.ietf.org/html/bcp47

Author: Schema.org Agent Platform
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from decimal import Decimal


# =============================================================================
# ENUMERATIONS
# =============================================================================

class ActionStatusType(Enum):
    """Status of an action/task"""
    POTENTIAL = "PotentialActionStatus"
    ACTIVE = "ActiveActionStatus"
    COMPLETED = "CompletedActionStatus"
    FAILED = "FailedActionStatus"


class ItemAvailability(Enum):
    """Availability status"""
    IN_STOCK = "InStock"
    ONLINE_ONLY = "OnlineOnly"
    PRE_ORDER = "PreOrder"
    OUT_OF_STOCK = "OutOfStock"


class EventStatusType(Enum):
    """Event status"""
    SCHEDULED = "EventScheduled"
    CANCELLED = "EventCancelled"
    POSTPONED = "EventPostponed"


# =============================================================================
# CATEGORY TYPES - Based on Global Standards
# NAICS: https://www.census.gov/naics/
# SOC: https://www.bls.gov/soc/
# =============================================================================

class IndustryCategory(Enum):
    """
    Industry categories based on NAICS (North American Industry Classification System)
    Reference: https://www.census.gov/naics/
    """
    # Technology (51-54)
    TECHNOLOGY = "Technology"
    SOFTWARE = "Software"
    AI_MACHINE_LEARNING = "AI/Machine Learning"
    CLOUD_COMPUTING = "Cloud Computing"
    CYBERSECURITY = "Cybersecurity"
    
    # Healthcare
    HEALTHCARE = "Healthcare"
    PHARMACEUTICALS = "Pharmaceuticals"
    MEDICAL_DEVICES = "Medical Devices"
    BIOTECH = "Biotechnology"
    
    # Finance
    FINANCE = "Finance"
    BANKING = "Banking"
    INSURANCE = "Insurance"
    INVESTMENT = "Investment"
    CRYPTOCURRENCY = "Cryptocurrency"
    
    # Retail & E-commerce
    RETAIL = "Retail"
    E_COMMERCE = "E-Commerce"
    CONSUMER_GOODS = "Consumer Goods"
    
    # Manufacturing
    MANUFACTURING = "Manufacturing"
    AUTOMOTIVE = "Automotive"
    AEROSPACE = "Aerospace"
    INDUSTRIAL = "Industrial"
    
    # Education
    EDUCATION = "Education"
    E_LEARNING = "E-Learning"
    EdTech = "EdTech"
    
    # Media & Entertainment
    MEDIA = "Media"
    ENTERTAINMENT = "Entertainment"
    GAMING = "Gaming"
    BROADCASTING = "Broadcasting"
    
    # Professional Services
    CONSULTING = "Consulting"
    LEGAL = "Legal"
    ACCOUNTING = "Accounting"
    MARKETING = "Marketing"
    REAL_ESTATE = "Real Estate"
    
    # Other
    AGRICULTURE = "Agriculture"
    ENERGY = "Energy"
    TELECOMMUNICATIONS = "Telecommunications"
    TRANSPORTATION = "Transportation"
    GOVERNMENT = "Government"
    NON_PROFIT = "Non-Profit"


class ServiceCategory(Enum):
    """Service type categories"""
    # By Function
    ASSISTANT = "Assistant"
    ANALYST = "Analyst"
    DEVELOPER = "Developer"
    WRITER = "Writer"
    RESEARCHER = "Researcher"
    SUPPORT = "Support"
    SALES = "Sales"
    MARKETING = "Marketing"
    
    # By Service Type
    B2B = "B2B"
    B2C = "B2C"
    C2C = "Consumer to Consumer"
    SAAS = "SaaS"
    
    # By Delivery
    API_SERVICE = "API Service"
    WEB_APP = "Web Application"
    MOBILE_APP = "Mobile Application"
    CHATBOT = "Chatbot"


class JobRoleCategory(Enum):
    """Job role categories"""
    # By Function
    JUNIOR = "Junior"
    SENIOR = "Senior"
    LEAD = "Lead"
    MANAGER = "Manager"
    DIRECTOR = "Director"
    VP = "VP"
    C_LEVEL = "C-Level"
    
    # By Department
    ENGINEERING = "Engineering"
    PRODUCT = "Product"
    DESIGN = "Design"
    SALES = "Sales"
    MARKETING = "Marketing"
    OPERATIONS = "Operations"
    FINANCE = "Finance"
    HR = "Human Resources"


class SkillCategory(Enum):
    """Skill categories"""
    # Data Operations
    DATA_READ = "data_read"
    DATA_WRITE = "data_write"
    DATA_QUERY = "data_query"
    DATA_ANALYSIS = "data_analysis"
    
    # Web & API
    WEB_SEARCH = "web_search"
    HTTP_REQUEST = "http_request"
    API_CALL = "api_call"
    WEBHOOK = "webhook"
    
    # Code & Execution
    CODE_EXECUTE = "code_execute"
    SHELL_COMMAND = "shell_command"
    FUNCTION_CALL = "function_call"
    
    # File Operations
    FILE_READ = "file_read"
    FILE_WRITE = "file_write"
    FILE_DELETE = "file_delete"
    
    # Communication
    SEND_EMAIL = "send_email"
    SEND_MESSAGE = "send_message"
    POST_NOTIFICATION = "post_notification"
    
    # AI/ML
    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    SPEECH_RECOGNITION = "speech_recognition"
    TRANSLATION = "translation"
    
    # Browser
    BROWSER_OPEN = "browser_open"
    BROWSER_CLICK = "browser_click"
    BROWSER_TYPE = "browser_type"
    
    # Monitoring
    LOG_WRITE = "log_write"
    METRIC_RECORD = "metric_record"
    ALERT_SEND = "alert_send"


class SoftwareCategory(Enum):
    """Software/Agent application categories"""
    # AI Agents
    AI_AGENT = "AI Agent"
    VIRTUAL_ASSISTANT = "Virtual Assistant"
    CHATBOT = "Chatbot"
    AUTONOMOUS_AGENT = "Autonomous Agent"
    
    # Productivity
    PRODUCTIVITY = "Productivity"
    CALENDAR = "Calendar"
    NOTE_TAKING = "Note Taking"
    PROJECT_MANAGEMENT = "Project Management"
    
    # Development
    DEVELOPMENT = "Development"
    IDE = "IDE"
    CODE_COMPLETION = "Code Completion"
    DEBUGGING = "Debugging"
    TESTING = "Testing"
    
    # Data & Analytics
    DATA_ANALYTICS = "Data Analytics"
    BUSINESS_INTELLIGENCE = "Business Intelligence"
    VISUALIZATION = "Visualization"
    REPORTING = "Reporting"
    
    # Communication
    COMMUNICATION = "Communication"
    VIDEO_CONFERENCING = "Video Conferencing"
    EMAIL_CLIENT = "Email Client"
    COLLABORATION = "Collaboration"
    
    # Marketing & Sales
    MARKETING_AUTOMATION = "Marketing Automation"
    CRM = "CRM"
    SALES_ENablement = "Sales Enablement"
    CUSTOMER_SUPPORT = "Customer Support"
    
    # Security
    SECURITY = "Security"
    IDENTITY_MANAGEMENT = "Identity Management"
    NETWORK_SECURITY = "Network Security"
    THREAT_DETECTION = "Threat Detection"
    
    # Infrastructure
    INFRASTRUCTURE = "Infrastructure"
    CLOUD_MANAGEMENT = "Cloud Management"
    CONTAINER_ORCHESTRATION = "Container Orchestration"
    DEVOPS = "DevOps"
    
    # Content
    CONTENT_MANAGEMENT = "Content Management"
    CMS = "CMS"
    DOCUMENT_MANAGEMENT = "Document Management"
    DIGITAL_ASSET_MANAGEMENT = "Digital Asset Management"
    
    # E-commerce
    ECOMMERCE = "E-Commerce"
    PAYMENT_PROCESSING = "Payment Processing"
    INVENTORY_MANAGEMENT = "Inventory Management"
    POINT_OF_SALE = "Point of Sale"


# =============================================================================
# CORE CLASSES
# =============================================================================

@dataclass
class Thing:
    """Base Schema.org type"""
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    
    def to_jsonld(self) -> Dict[str, Any]:
        result = {"@type": self.__class__.__name__}
        if self.id:
            result["@id"] = self.id
        if self.name:
            result["name"] = self.name
        if self.description:
            result["description"] = self.description
        if self.url:
            result["url"] = self.url
        return result


@dataclass
class PostalAddress(Thing):
    """Postal address"""
    street_address: Optional[str] = None
    address_locality: Optional[str] = None
    address_region: Optional[str] = None
    address_country: Optional[str] = None
    postal_code: Optional[str] = None


@dataclass
class GeoCoordinates(Thing):
    """Geographic coordinates"""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation: Optional[float] = None


@dataclass
class Place(Thing):
    """Physical or virtual place"""
    address: Optional[PostalAddress] = None
    geo: Optional[GeoCoordinates] = None
    telephone: Optional[str] = None


@dataclass
class MonetaryAmount(Thing):
    """Money value"""
    currency: Optional[str] = "USD"
    value: Optional[float] = None


@dataclass
class PriceSpecification(Thing):
    """Price specification"""
    price: Optional[float] = None
    price_currency: Optional[str] = "USD"
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None


@dataclass
class UnitPriceSpecification(PriceSpecification):
    """Price per unit"""
    price_per_unit: Optional[float] = None
    unit_code: Optional[str] = None


@dataclass
class Offer(Thing):
    """Pricing offer"""
    price: Optional[float] = None
    price_currency: Optional[str] = "USD"
    availability: Optional[ItemAvailability] = None
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None
    unit_price: Optional[UnitPriceSpecification] = None


@dataclass
class PropertyValue(Thing):
    """Key-value property"""
    property_id: Optional[str] = None
    value: Optional[Any] = None


# =============================================================================
# ORGANIZATION - Company/Department
# =============================================================================

@dataclass
class Organization(Thing):
    """
    Organization (company/department)
    Includes Schema.org properties + custom platform fields
    """
    # Schema.org fields
    legal_name: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    parent_organization: Optional[Organization] = None
    sub_organization: List[Organization] = field(default_factory=list)
    member: List[Any] = field(default_factory=list)
    
    # === CUSTOM FIELDS ===
    # Business
    industry: Optional[str] = None  # IndustryCategory
    employee_count: int = 0
    founded_year: Optional[int] = None
    website: Optional[str] = None
    
    # Location
    headquarters: Optional[Place] = None
    
    # Tier
    tier: str = "standard"  # free, standard, enterprise
    subscription_status: str = "active"
    
    # Limits
    max_agents: int = 10
    max_api_calls_per_day: int = 1000
    
    # Billing
    billing_email: Optional[str] = None
    plan: Optional[str] = None
    
    def add_department(self, dept: Organization):
        """Add a sub-department"""
        dept.parent_organization = self
        self.sub_organization.append(dept)
    
    def add_member(self, person: Person):
        """Add a member"""
        self.member.append(person)


# =============================================================================
# PERSON - User/Owner/Employee
# =============================================================================

@dataclass
class Person(Thing):
    """
    Person (owner, employee)
    Includes Schema.org properties + custom platform fields
    """
    # Schema.org fields
    email: Optional[str] = None
    job_title: Optional[str] = None
    telephone: Optional[str] = None
    works_for: List[Organization] = field(default_factory=list)
    knows_language: List[str] = field(default_factory=list)  # Skills
    
    # === CUSTOM FIELDS ===
    # Account
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    
    # Role (SOC-based)
    role: Optional[str] = None  # JobRoleCategory
    department: Optional[str] = None
    
    # Status
    account_status: str = "active"
    verified: bool = False
    
    # Limits
    max_agents_owned: int = 5
    max_api_calls_per_day: int = 100
    
    def add_skill(self, skill: str):
        """Add a skill"""
        if skill not in self.knows_language:
            self.knows_language.append(skill)


# =============================================================================
# SOFTWAREAPPLICATION - AGENT
# =============================================================================

@dataclass
class SoftwareApplication(Thing):
    """
    Agent - The main entity representing an AI agent
    Includes Schema.org properties + custom platform fields
    """
    # Identity (Schema.org)
    application_category: Optional[str] = None
    application_sub_category: Optional[str] = None
    software_version: Optional[str] = None
    
    # Technical (Schema.org)
    runtime: Optional[str] = None
    programming_language: Optional[str] = None
    software_requirements: Optional[str] = None
    
    # Skills/Capabilities
    knows_language: List[str] = field(default_factory=list)  # Agent skills
    available_language: List[str] = field(default_factory=list)  # Supported languages
    
    # Ownership (Schema.org)
    author: Optional[Person] = None  # Owner/creator
    
    # Organization (Schema.org)
    provider: Optional[Organization] = None  # Company providing
    works_for: Optional[Organization] = None  # Works in department
    
    # Location (Schema.org)
    location: Optional[Place] = None
    
    # Pricing (Schema.org)
    offers: List[Offer] = field(default_factory=list)
    
    # Validity (Schema.org)
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None
    
    # === CUSTOM FIELDS (Platform-specific) ===
    # Status & Config
    status: str = "active"  # active, paused, deprecated
    config: Dict[str, Any] = field(default_factory=dict)
    
    # Limits
    max_concurrent_tasks: int = 10
    rate_limit_per_minute: int = 60
    max_memory_mb: int = 512
    
    # Custom metadata
    tags: List[str] = field(default_factory=list)
    category: Optional[str] = None  # IndustryCategory value
    service_type: Optional[str] = None  # ServiceCategory value
    job_role: Optional[str] = None  # JobRoleCategory value
    
    # Integration
    webhook_url: Optional[str] = None
    callback_url: Optional[str] = None
    
    # Monitoring
    is_active: bool = True
    last_active: Optional[datetime] = None
    uptime_percent: float = 0.0
    
    # Custom properties
    additional_property: List[PropertyValue] = field(default_factory=list)
    
    def add_skill(self, skill: str):
        """Add a skill"""
        if skill not in self.knows_language:
            self.knows_language.append(skill)
    
    def set_pricing(self, price: float, currency: str = "USD", plan_name: str = "Basic"):
        """Set pricing plan"""
        offer = Offer(
            name=plan_name,
            price=price,
            price_currency=currency,
            availability=ItemAvailability.IN_STOCK
        )
        self.offers.append(offer)
    
    def set_owner(self, person: Person):
        """Set owner"""
        self.author = person
    
    def set_organization(self, org: Organization):
        """Set organization"""
        self.provider = org
    
    def set_department(self, dept: Organization):
        """Set department"""
        self.works_for = dept
    
    def to_jsonld(self) -> Dict[str, Any]:
        result = super().to_jsonld()
        if self.application_category:
            result["applicationCategory"] = self.application_category
        if self.knows_language:
            result["knowsLanguage"] = self.knows_language
        if self.author:
            result["author"] = {"@id": self.author.id}
        if self.provider:
            result["provider"] = {"@id": self.provider.id}
        if self.works_for:
            result["worksFor"] = {"@id": self.works_for.id}
        if self.offers:
            result["offers"] = [o.to_jsonld() for o in self.offers]
        return result


# =============================================================================
# ACTION - TASK
# =============================================================================

@dataclass
class Action(Thing):
    """
    Task - An action performed by an agent
    Includes Schema.org properties + custom platform fields
    """
    # Action type (Schema.org)
    action_type: Optional[str] = None
    
    # Status (Schema.org)
    action_status: Optional[ActionStatusType] = None
    
    # Agent performing (Schema.org)
    agent: Optional[SoftwareApplication] = None
    
    # Input/Output (Schema.org)
    object: Optional[Any] = None  # Input
    result: Optional[Any] = None   # Output
    
    # Timing (Schema.org)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[timedelta] = None
    
    # Error (Schema.org)
    error: Optional[str] = None
    
    # === CUSTOM FIELDS (Platform-specific) ===
    # Execution
    priority: int = 5  # 1-10
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 300
    
    # Resources
    cpu_units: float = 1.0
    memory_mb: int = 256
    
    # Progress
    progress_percent: int = 0
    current_step: Optional[str] = None
    
    # Cost tracking
    compute_cost: float = 0.0
    api_calls: int = 0
    tokens_used: int = 0
    
    # Metadata
    parent_task_id: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Results reference
    result_url: Optional[str] = None
    logs: List[str] = field(default_factory=list)
    
    def start(self):
        """Start the task"""
        self.action_status = ActionStatusType.ACTIVE
        self.start_time = datetime.now()
    
    def complete(self, result: Any):
        """Complete the task"""
        self.action_status = ActionStatusType.COMPLETED
        self.result = result
        self.end_time = datetime.now()
        if self.start_time:
            self.duration = self.end_time - self.start_time
    
    def fail(self, error: str):
        """Fail the task"""
        self.action_status = ActionStatusType.FAILED
        self.error = error
        self.end_time = datetime.now()
    
    def to_jsonld(self) -> Dict[str, Any]:
        result = super().to_jsonld()
        if self.action_type:
            result["@type"] = self.action_type
        if self.action_status:
            result["actionStatus"] = self.action_status.value
        if self.agent:
            result["agent"] = {"@id": self.agent.id}
        if self.result:
            result["result"] = self.result
        if self.start_time:
            result["startTime"] = self.start_time.isoformat()
        if self.end_time:
            result["endTime"] = self.end_time.isoformat()
        return result


# =============================================================================
# EVENT
# =============================================================================

@dataclass
class Event(Thing):
    """Event (task events, system events)"""
    event_status: Optional[EventStatusType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[Place] = None
    organizer: Optional[Organization] = None
    attendee: Optional[SoftwareApplication] = None  # Agent


# =============================================================================
# CREDENTIALS
# =============================================================================

@dataclass
class Credential(Thing):
    """API Key / Certificate / Token"""
    credential_type: Optional[str] = None  # api_key, oauth, jwt, certificate
    key_hash: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None
    owner: Optional[SoftwareApplication] = None
    revoked: bool = False
    
    def is_valid(self) -> bool:
        """Check if credential is valid"""
        if self.revoked:
            return False
        if self.valid_through:
            return datetime.now() < self.valid_through
        return True
    
    def revoke(self):
        """Revoke credential"""
        self.revoked = True


# =============================================================================
# SUBSCRIPTION
# =============================================================================

@dataclass
class Subscription(Thing):
    """Agent subscription"""
    offer: Optional[Offer] = None
    agent: Optional[SoftwareApplication] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "active"
    auto_renew: bool = False
    
    def cancel(self):
        """Cancel subscription"""
        self.status = "cancelled"
    
    def renew(self):
        """Renew subscription"""
        if self.end_date:
            self.end_date = self.end_date + timedelta(days=30)


# =============================================================================
# COST TRACKING
# =============================================================================

@dataclass
class CostRecord(Thing):
    """Cost tracking for tasks"""
    agent: Optional[SoftwareApplication] = None
    task: Optional[Action] = None
    
    # Cost breakdown
    compute_cost: float = 0.0
    api_cost: float = 0.0
    storage_cost: float = 0.0
    network_cost: float = 0.0
    total_cost: float = 0.0
    
    # Metrics
    compute_time: float = 0.0  # seconds
    api_calls: int = 0
    tokens_used: int = 0
    
    def calculate_total(self):
        """Calculate total cost"""
        self.total_cost = self.compute_cost + self.api_cost + self.storage_cost + self.network_cost


# =============================================================================
# SCHEDULE
# =============================================================================

@dataclass
class Schedule(Thing):
    """Task schedule"""
    agent: Optional[SoftwareApplication] = None
    cron_expression: Optional[str] = None
    timezone: str = "UTC"
    next_run: Optional[datetime] = None
    last_run: Optional[datetime] = None
    active: bool = True
    
    def should_run(self) -> bool:
        """Check if should run now"""
        if not self.active:
            return False
        if self.next_run:
            return datetime.now() >= self.next_run
        return False


# =============================================================================
# MEMORY
# =============================================================================

@dataclass
class Memory(Thing):
    """
    Agent Memory - Knowledge/Past Interactions
    """
    memory_type: Optional[str] = None  # short_term, long_term, episodic, semantic
    content: Optional[Any] = None
    importance: float = 0.5  # 0-1
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    created_by: Optional[SoftwareApplication] = None  # Agent that created
    context: Optional[Action] = None  # Related task
    
    def access(self):
        """Record memory access"""
        self.access_count += 1
        self.last_accessed = datetime.now()
    
    def to_jsonld(self) -> Dict[str, Any]:
        result = super().to_jsonld()
        if self.memory_type:
            result["memoryType"] = self.memory_type
        if self.content:
            result["content"] = self.content
        if self.importance:
            result["importance"] = self.importance
        return result


@dataclass
class Conversation(Thing):
    """
    Conversation/Session memory
    """
    participants: List[Union[Person, SoftwareApplication]] = field(default_factory=list)
    messages: List[Dict[str, Any]] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def add_message(self, sender: Any, content: str, metadata: Dict = None):
        """Add a message to conversation"""
        message = {
            "sender": sender.id if hasattr(sender, 'id') else str(sender),
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.messages.append(message)
    
    def end(self):
        """End conversation"""
        self.end_time = datetime.now()


@dataclass
class KnowledgeBase(Thing):
    """
    Knowledge base / Vector store
    """
    knowledge_type: Optional[str] = None  # facts, documents, code, etc
    entries: List[Dict[str, Any]] = field(default_factory=list)
    embedding_model: Optional[str] = None
    
    def add_entry(self, content: str, vector: List[float] = None, metadata: Dict = None):
        """Add knowledge entry"""
        entry = {
            "content": content,
            "vector": vector,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }
        self.entries.append(entry)
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search knowledge (simple text match)"""
        results = []
        for entry in self.entries:
            if query.lower() in entry.get("content", "").lower():
                results.append(entry)
                if len(results) >= limit:
                    break
        return results


# =============================================================================
# AGENT PLATFORM REPOSITORY
# =============================================================================

class AgentPlatform:
    """
    Complete Agent Platform using Schema.org types
    """
    
    def __init__(self):
        self.organizations: Dict[str, Organization] = {}
        self.persons: Dict[str, Person] = {}
        self.agents: Dict[str, SoftwareApplication] = {}
        self.tasks: Dict[str, Action] = {}
        self.credentials: Dict[str, Credential] = {}
        self.subscriptions: Dict[str, Subscription] = {}
        self.schedules: Dict[str, Schedule] = {}
        self.cost_records: List[CostRecord] = []
        
        # Memory
        self.memories: Dict[str, Memory] = {}
        self.conversations: Dict[str, Conversation] = {}
        self.knowledge_bases: Dict[str, KnowledgeBase] = {}
    
    # -------------------------------------------------------------------------
    # Organization Management
    # -------------------------------------------------------------------------
    
    def create_organization(
        self,
        id: str,
        name: str,
        legal_name: str = None,
        email: str = None
    ) -> Organization:
        """Create an organization"""
        org = Organization(
            id=id,
            name=name,
            legal_name=legal_name or name,
            email=email
        )
        self.organizations[id] = org
        return org
    
    def create_department(
        self,
        parent_id: str,
        id: str,
        name: str
    ) -> Organization:
        """Create a department"""
        parent = self.organizations.get(parent_id)
        if not parent:
            raise ValueError(f"Organization {parent_id} not found")
        
        dept = Organization(id=id, name=name)
        parent.add_department(dept)
        self.organizations[id] = dept
        return dept
    
    def get_organization(self, id: str) -> Optional[Organization]:
        """Get organization"""
        return self.organizations.get(id)
    
    # -------------------------------------------------------------------------
    # Person Management
    # -------------------------------------------------------------------------
    
    def create_person(
        self,
        id: str,
        name: str,
        email: str = None,
        job_title: str = None
    ) -> Person:
        """Create a person"""
        person = Person(
            id=id,
            name=name,
            email=email,
            job_title=job_title
        )
        self.persons[id] = person
        return person
    
    def add_person_to_organization(self, person_id: str, org_id: str):
        """Add person to organization"""
        person = self.persons.get(person_id)
        org = self.organizations.get(org_id)
        if person and org:
            org.add_member(person)
            person.works_for.append(org)
    
    # -------------------------------------------------------------------------
    # Agent Management
    # -------------------------------------------------------------------------
    
    def create_agent(
        self,
        id: str,
        name: str,
        description: str = None,
        category: str = "AI Agent"
    ) -> SoftwareApplication:
        """Create an agent"""
        agent = SoftwareApplication(
            id=id,
            name=name,
            description=description,
            application_category=category
        )
        self.agents[id] = agent
        return agent
    
    def set_agent_owner(self, agent_id: str, person_id: str):
        """Set agent owner"""
        agent = self.agents.get(agent_id)
        person = self.persons.get(person_id)
        if agent and person:
            agent.set_owner(person)
    
    def set_agent_organization(self, agent_id: str, org_id: str):
        """Set agent organization"""
        agent = self.agents.get(agent_id)
        org = self.organizations.get(org_id)
        if agent and org:
            agent.set_organization(org)
    
    def set_agent_department(self, agent_id: str, dept_id: str):
        """Set agent department"""
        agent = self.agents.get(agent_id)
        dept = self.organizations.get(dept_id)
        if agent and dept:
            agent.set_department(dept)
    
    def add_agent_skill(self, agent_id: str, skill: str):
        """Add skill to agent"""
        agent = self.agents.get(agent_id)
        if agent:
            agent.add_skill(skill)
    
    def set_agent_pricing(
        self,
        agent_id: str,
        price: float,
        currency: str = "USD",
        plan_name: str = "Basic"
    ):
        """Set agent pricing"""
        agent = self.agents.get(agent_id)
        if agent:
            agent.set_pricing(price, currency, plan_name)
    
    def get_agent(self, id: str) -> Optional[SoftwareApplication]:
        """Get agent"""
        return self.agents.get(id)
    
    def list_agents(self, org_id: str = None, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """List all agents with pagination"""
        if org_id:
            org = self.organizations.get(org_id)
            if org:
                all_agents = [a for a in self.agents.values() 
                       if a.provider and a.provider.id == org_id]
        else:
            all_agents = list(self.agents.values())
        
        total = len(all_agents)
        total_pages = (total + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size
        items = all_agents[start:end]
        
        return {
            "items": [a.to_jsonld() for a in items],
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": max(1, total_pages)
        }
    
    # -------------------------------------------------------------------------
    # Task Management
    # -------------------------------------------------------------------------
    
    def create_task(
        self,
        id: str,
        agent_id: str,
        task_type: str = "Action",
        name: str = None,
        task_input: Any = None
    ) -> Action:
        """Create a task"""
        agent = self.agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        task = Action(
            id=id,
            name=name or f"Task {id}",
            action_type=task_type,
            agent=agent,
            object=task_input
        )
        self.tasks[id] = task
        return task
    
    def start_task(self, task_id: str):
        """Start a task"""
        task = self.tasks.get(task_id)
        if task:
            task.start()
    
    def complete_task(self, task_id: str, result: Any):
        """Complete a task"""
        task = self.tasks.get(task_id)
        if task:
            task.complete(result)
            
            # Track cost
            cost = CostRecord(
                id=f"cost-{task_id}",
                agent=task.agent,
                task=task
            )
            self.cost_records.append(cost)
    
    def fail_task(self, task_id: str, error: str):
        """Fail a task"""
        task = self.tasks.get(task_id)
        if task:
            task.fail(error)
    
    def get_task(self, id: str) -> Optional[Action]:
        """Get task"""
        return self.tasks.get(id)
    
    def list_tasks(self, agent_id: str = None, status: ActionStatusType = None, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """List tasks with pagination"""
        tasks = list(self.tasks.values())
        
        if agent_id:
            tasks = [t for t in tasks if t.agent and t.agent.id == agent_id]
        
        if status:
            tasks = [t for t in tasks if t.action_status == status]
        
        total = len(tasks)
        total_pages = (total + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size
        items = tasks[start:end]
        
        return {
            "items": [t.to_jsonld() for t in items],
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": max(1, total_pages)
        }
    
    # -------------------------------------------------------------------------
    # Credentials
    # -------------------------------------------------------------------------
    
    def create_api_key(
        self,
        id: str,
        agent_id: str,
        key_hash: str,
        valid_days: int = 365
    ) -> Credential:
        """Create API key"""
        agent = self.agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        credential = Credential(
            id=id,
            credential_type="api_key",
            key_hash=key_hash,
            valid_from=datetime.now(),
            valid_through=datetime.now() + timedelta(days=valid_days),
            owner=agent
        )
        self.credentials[id] = credential
        return credential
    
    def revoke_credential(self, credential_id: str):
        """Revoke credential"""
        credential = self.credentials.get(credential_id)
        if credential:
            credential.revoke()
    
    # -------------------------------------------------------------------------
    # Subscriptions
    # -------------------------------------------------------------------------
    
    def create_subscription(
        self,
        id: str,
        agent_id: str,
        price: float,
        currency: str = "USD",
        days: int = 30
    ) -> Subscription:
        """Create subscription"""
        agent = self.agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        offer = Offer(
            name="Subscription",
            price=price,
            price_currency=currency
        )
        
        subscription = Subscription(
            id=id,
            offer=offer,
            agent=agent,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=days)
        )
        self.subscriptions[id] = subscription
        return subscription
    
    # -------------------------------------------------------------------------
    # Export
    # -------------------------------------------------------------------------
    
    def to_jsonld(self) -> Dict[str, Any]:
        """Export entire platform as JSON-LD"""
        return {
            "@context": "https://schema.org",
            "@graph": [
                *[org.to_jsonld() for org in self.organizations.values()],
                *[person.to_jsonld() for person in self.persons.values()],
                *[agent.to_jsonld() for agent in self.agents.values()],
                *[task.to_jsonld() for task in self.tasks.values()],
            ]
        }


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def main():
    """Example: Create complete agent platform"""
    
    platform = AgentPlatform()
    
    # 1. Create Organization
    print("=== Creating Organization ===")
    company = platform.create_organization(
        id="org-acme",
        name="Acme Corporation",
        email="contact@acme.com"
    )
    print(f"Created: {company.name}")
    
    # 2. Create Departments
    print("\n=== Creating Departments ===")
    engineering = platform.create_department("org-acme", "dept-eng", "Engineering")
    sales = platform.create_department("org-acme", "dept-sales", "Sales")
    print(f"Created: {engineering.name}, {sales.name}")
    
    # 3. Create Person
    print("\n=== Creating Person ===")
    john = platform.create_person(
        id="person-john",
        name="John Doe",
        email="john@acme.com",
        job_title="AI Engineer"
    )
    platform.add_person_to_organization("person-john", "org-acme")
    print(f"Created: {john.name} ({john.job_title})")
    
    # 4. Create Agent
    print("\n=== Creating Agent ===")
    agent = platform.create_agent(
        id="agent-assistant",
        name="AI Assistant",
        description="General purpose AI assistant",
        category="AI Agent"
    )
    
    # Set relationships
    platform.set_agent_owner("agent-assistant", "person-john")
    platform.set_agent_organization("agent-assistant", "org-acme")
    platform.set_agent_department("agent-assistant", "dept-eng")
    
    # Add skills
    platform.add_agent_skill("agent-assistant", "web_search")
    platform.add_agent_skill("agent-assistant", "file_read")
    platform.add_agent_skill("agent-assistant", "code_execute")
    platform.add_agent_skill("agent-assistant", "data_analysis")
    
    # Set pricing
    platform.set_agent_pricing("agent-assistant", 29.99, "USD", "Basic Plan")
    platform.set_agent_pricing("agent-assistant", 99.99, "USD", "Pro Plan")
    
    print(f"Created: {agent.name}")
    print(f"  Skills: {agent.knows_language}")
    print(f"  Owner: {agent.author.name if agent.author else 'None'}")
    print(f"  Org: {agent.provider.name if agent.provider else 'None'}")
    
    # 5. Create Tasks
    print("\n=== Creating Tasks ===")
    task1 = platform.create_task(
        id="task-001",
        agent_id="agent-assistant",
        task_type="SearchAction",
        name="Search for information",
        task_input={"query": "weather"}
    )
    platform.start_task("task-001")
    platform.complete_task("task-001", {"results": ["sunny", "25C"]})
    print(f"Task: {task1.name} - Status: {task1.action_status.value}")
    
    task2 = platform.create_task(
        id="task-002",
        agent_id="agent-assistant",
        task_type="AnalyzeAction",
        name="Analyze data"
    )
    platform.start_task("task-002")
    platform.complete_task("task-002", {"analysis": "completed", "cost": 0.05})
    print(f"Task: {task2.name} - Status: {task2.action_status.value}")
    
    # 6. Create API Key
    print("\n=== Creating Credentials ===")
    api_key = platform.create_api_key(
        id="key-001",
        agent_id="agent-assistant",
        key_hash="sk-xxxxx",
        valid_days=365
    )
    print(f"API Key: {api_key.id} - Valid: {api_key.is_valid()}")
    
    # 7. Create Subscription
    print("\n=== Creating Subscription ===")
    sub = platform.create_subscription(
        id="sub-001",
        agent_id="agent-assistant",
        price=29.99
    )
    print(f"Subscription: {sub.id} - Status: {sub.status}")
    
    # 8. List all
    print("\n=== Platform Summary ===")
    agents = platform.list_agents()
    print(f"Total Agents: {len(agents)}")
    
    tasks = platform.list_tasks(agent_id="agent-assistant")
    print(f"Total Tasks: {len(tasks)}")
    
    completed = platform.list_tasks(agent_id="agent-assistant", status=ActionStatusType.COMPLETED)
    print(f"Completed Tasks: {len(completed)}")
    
    # 9. Export JSON-LD
    print("\n=== JSON-LD Export ===")
    jsonld = platform.to_jsonld()
    print(f"Exported {len(jsonld['@graph'])} entities")


if __name__ == "__main__":
    main()


"""
Agent Platform - Schema.org Implementation

Usage:
    from agent_platform import AgentPlatform, SoftwareApplication, Action
    
    # Create platform
    platform = AgentPlatform()
    
    # Create organization
    company = platform.create_organization("org-1", "Acme Inc")
    
    # Create person
    owner = platform.create_person("person-1", "John", "john@acme.com")
    
    # Create agent
    agent = platform.create_agent("agent-1", "AI Assistant")
    agent.set_owner(owner)
    agent.set_organization(company)
    agent.add_skill("web_search")
    agent.set_pricing(29.99)
    
    # Create task
    task = platform.create_task("task-1", "agent-1", "SearchAction")
    task.start()
    task.complete({"results": [...]})
    
    # Export
    print(platform.to_jsonld())

References:
    - https://schema.org/SoftwareApplication
    - https://schema.org/Action
    - https://schema.org/Organization
    - https://schema.org/Person
    - https://schema.org/Offer
"""