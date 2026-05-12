# Transform All Frameworks to Schema.org Primitives

## Complete Framework → Schema.org Mapping

### 1. COMPLIANCE FRAMEWORKS

| Framework | Schema.org Type | Properties |
|-----------|-----------------|------------|
| GDPR | Legislation | dataController, dataProcessor, rightToDelete |
| HIPAA | MedicalGuideline | PHI, securityRule, breachNotification |
| SOC2 | Credential | auditType, trustServiceCriteria |
| ISO27001 | Credential | securityControl, certification |
| PCI-DSS | Legislation | paymentCard, securityStandard |
| CCPA | Legislation | rightToOptOut, doNotSell |
| FERPA | EducationalCredential | studentRecord, privacyConsent |

**Implementation**:
```python
@dataclass
class ComplianceFramework:
    name: str = ""          # Legislation.name
    jurisdiction: str = ""
    effective_date: date = None
    legal_force: str = "InForce"  # LegalForceStatus
    
    # Schema.org mapping
    additional_type: str = "Legislation"
    defines: List[str] = []  # Laws defined
    about: List[str] = []    # Topics covered
```

---

### 2. SECURITY PROTOCOLS

| Protocol | Schema.org Type | Properties |
|----------|------------------|------------|
| OAuth2.0 | Action | authorize, consent |
| SAML | Action | authenticate, sso |
| OpenID | Action | authorize, identify |
| JWT | Credential | token, claims, signature |
| TLS 1.3 | ActionAccessSpecification | encryption, transport |
| SSH | ActionAccessSpecification | keyExchange |
| LDAP | Action | authenticate, directory |
| Kerberos | Action | authenticate, ticket |

**Implementation**:
```python
@dataclass
class SecurityProtocol:
    name: str = ""          # Action.name
    protocol: str = ""      # Protocol name
    mechanism: str = ""    # Auth mechanism
    
    # Schema.org
    additional_type: str = "Action"
    result: str = ""        # Success/Failure
    object: str = ""       # Auth object
    target: str = ""      # Target service
```

---

### 3. GOVERNANCE FRAMEWORKS

| Framework | Schema.org Type | Description |
|-----------|------------------|------------|
| ITIL | Guide | Service management |
| COBIT | Guide | IT governance |
| TOGAF | Guide | Enterprise arch |
| NIST CSF | Legislation | Cybersecurity |
| COSO | Guide | Internal controls |
| ISO 37301 | Credential | Compliance |

**Implementation**:
```python
@dataclass
class GovernanceFramework:
    name: str = ""          # Guide.name / Credential.name
    version: str = ""
    
    # Governance
    category: str = ""     # Framework category
    scope: str = ""       # Scope (enterprise, IT, etc.)
    
    # Schema.org
    additional_type: str = "Guide"
    about: List[str] = []  # Topics
```

---

### 4. CLOUD PROVIDERS

| Provider | Schema.org Type | Properties |
|----------|------------------|------------|
| AWS | WebAPI | region, service |
| Azure | WebAPI | subscription, tenant |
| GCP | WebAPI | project, region |
| Google Cloud Run | Service | container, serverless |
| Azure Functions | Service | function, serverless |
| AWS Lambda | Service | function, serverless |

**Implementation**:
```python
@dataclass
class CloudProvider:
    name: str = ""          # WebAPI.name
    provider: str = ""      # Organization
    
    # Cloud-specific
    region: str = ""       # Place
    availability: str = "" # ItemAvailability
    pricing: str = ""      # Offer.price
    
    # Schema.org
    additional_type: str = "WebAPI"
    service_url: str = ""
    endpoint: str = ""
```

---

### 5. AGENT RUNTIME

| Runtime | Schema.org Type | Properties |
|---------|------------------|------------|
| VoltAgent | SoftwareApplication | agent, memory, skills |
| AgentScope | SoftwareApplication | multiAgent, deployment |
| Haystack | SoftwareApplication | rag, pipeline |
| GitHub Copilot | SoftwareApplication | ai, coding |
| Deno | RuntimePlatform | typescript, secure |
| Bun | RuntimePlatform | javascript, fast |

**Implementation**:
```python
@dataclass
class AgentRuntime:
    name: str = ""          # SoftwareApplication.name
    version: str = ""
    
    # Agent features
    memory: bool = False   # Has memory
    rag: bool = False      # RAG support
    voice: bool = False   # Voice I/O
    mcp: bool = False    # MCP support
    guardrails: bool = False
    
    # Schema.org
    additional_type: str = "RuntimePlatform"
    application_category: str = "DeveloperApplication"
    operating_system: str = ""  # Platform
```

---

### 6. PROGRAMMING RUNTIME

| Runtime | Schema.org Type | Language |
|---------|------------------|---------|
| Node.js | RuntimePlatform | JavaScript |
| Bun | RuntimePlatform | JavaScript/TypeScript |
| Deno | RuntimePlatform | TypeScript |
| PyPy | RuntimePlatform | Python |
| GraalVM | RuntimePlatform | Multi-language |
| wasmtime | RuntimePlatform | WebAssembly |
| .NET | RuntimePlatform | C# |
| JVM | RuntimePlatform | Java |

**Implementation**:
```python
@dataclass
class ProgrammingRuntime:
    name: str = ""          # RuntimePlatform.name
    version: str = ""
    
    # Runtime
    language: str = ""       # ProgrammingLanguage
    type: str = ""          # Interpreted, Compiled, VM
    garbage_collected: bool = False
    async_support: bool = False
    wasm_support: bool = False
    
    # Schema.org
    additional_type: str = "RuntimePlatform"
    programming_language: str = ""  # Language
```

---

### 7. DATABASE BACKENDS

| Database | Schema.org Type | Properties |
|----------|------------------|------------|
| SurrealDB | Database | graph, in-memory |
| PostgreSQL | Database | relational |
| MySQL | Database | relational |
| Redis | Database | key-value |
| MongoDB | Database | document |
| Neo4j | Database | graph |

**Implementation**:
```python
@dataclass
class DatabaseBackend:
    name: str = ""          # Database.type (using Schema.org DB)
    version: str = ""
    
    # Type
    database_type: str = ""  # Relational, Graph, Document
    storage: str = ""        # In-memory, Disk
    
    # Connection
    host: str = ""         # Place (server)
    port: int = 0
    credentials: str = ""   # Credential
    
    # Schema.org (no specific type, using properties)
    additional_type: str = "WebAPI"
```

---

### 8. W3 STANDARDS

| Standard | Schema.org Type | Properties |
|----------|------------------|------------|
| JSON-LD | MediaType | @context, @type |
| RDF | StructuredValue | subject, predicate, object |
| Dublin Core | StructuredValue | title, creator, subject |
| FOAF | Person | name, knows, mbox |
| SKOS | DefinedTermSet | concept, scheme |
| OWL | StructuredValue | class, property |

**Implementation**:
```python
@dataclass
class W3Standard:
    name: str = ""          # MediaType / StructuredValue
    standard: str = ""      # Standard name
    
    # W3 properties
    version: str = ""
    namespace: str = ""
    
    # Schema.org
    additional_type: str = "StructuredValue"
    domain: str = ""
    range: str = ""
```

---

### 9. LINUX (Operating System)

| Component | Schema.org Type | Properties |
|-----------|------------------|------------|
| User | Person | name, homeDir, shell |
| Process | Action | pid, command, status |
| Service | Service | name, enabled, status |
| File | CreativeWork | name, path, permissions |
| Package | Product | name, version, Architecture |
| Device | Place | address, capacity |

**Implementation**:
```python
@dataclass
class LinuxComponent:
    name: str = ""
    type: str = ""          # Component type
    
    # Linux-specific
    path: str = ""         # Place (address)
    permissions: str = ""  # Intangible (permission)
    owner: str = ""        # Person
    
    # Schema.org mapping
    component_type: str = "Thing"
```

---

### 10. TIME FRAMEWORKS (ISO 8601, RFC 3339)

| Format | Schema.org Type | Properties |
|-------|------------------|------------|
| Date | Date | YYYY-MM-DD |
| DateTime | DateTime | ISO 8601 |
| Time | Time | HH:MM:SS |
| Duration | Duration | ISO 8601 duration |
| Timezone | Place | UTC offset |

**Implementation**:
```python
@dataclass
class SchemaorgTime:
    value: str = ""         # Date/DateTime value
    
    # Properties
    timezone: str = ""     # Place (timezone)
    utc_offset: int = 0
    
    # Schema.org data type
    data_type: str = "Date"  # or DateTime, Time, Duration
```

---

## Complete Transformation Function

```python
def transform_framework_to_schema(framework: str, data: dict) -> dict:
    """Transform any framework to Schema.org primitives"""
    
    transformers = {
        "compliance": transform_compliance,
        "security": transform_security,
        "governance": transform_governance,
        "cloud": transform_cloud,
        "agent": transform_agent,
        "runtime": transform_runtime,
        "database": transform_database,
        "w3": transform_w3,
        "linux": transform_linux,
        "time": transform_time,
    }
    
    category = data.get("category", "unknown")
    
    if category in transformers:
        return transformers[category](data)
    
    return {"error": "Unknown framework category"}
```

---

## Summary Table

| Framework Category | Schema.org Type | Files |
|-------------------|---|-------|
| Compliance | Legislation, Credential, MedicalGuideline | COMPLIANCE_MAPPING.md |
| Security | Action, ActionAccessSpecification | SECURITY_PROTOCOLS.md |
| Governance | Guide | GOVERNANCE_PROTOCOLS.md |
| Cloud | WebAPI, Service | CLOUD_PROVIDERS.md |
| Agent Runtime | SoftwareApplication, RuntimePlatform | AGENT_RUNTIME_REPOS.md |
| Programming Runtime | RuntimePlatform | RUNTIME_REPOS.md |
| Database | (properties only) | SURREALDB_WIRING.md |
| W3 Standards | StructuredValue, MediaType | W3_STANDARDS.md |
| Linux | Person, Action, Service, Thing | LINUX_INSIGHTS.md |
| Time | Date, DateTime, Duration | time_search.py |

Reference: https://schema.org/docs/full.html