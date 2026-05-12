# Governance Protocols Mapping

## Governance Frameworks → Schema.org

| Framework | Schema.org Type | Domain |
|-----------|----------------|--------|
| **ITIL** | Guide | Service Management |
| **COBIT** | Guide | IT Governance |
| **TOGAF** | Guide | Enterprise Architecture |
| **NIST CSF** | Legislation | Cybersecurity |
| **COSO** | Guide | Internal Controls |
| **ISO 37301** | Credential | Compliance |

## Governance Bodies

| Body | Schema.org Organization | Standard |
|------|---------------------|----------|
| **ISO** | StandardsOrganization | ISO standards |
| **IETF** | StandardsOrganization | RFC standards |
| **W3C** | StandardsOrganization | Web standards |
| **IEEE** | StandardsOrganization | Tech standards |
| **NIST** | GovernmentOrganization | US standards |
| **IEC** | StandardsOrganization | Intl standards |

## Decision Making

```python
@dataclass
class GovernanceDecision:
    id: str
    
    # Decision
    title: str = ""
    decision_type: str = ""  # Policy, Procedure, Directive
    
    # Actors
    proposer: str = ""      # Person
    approver: str = ""       # Person
    stakeholders: List[str] = []  # Person
    
    # Process
    status: str = ""         # Draft, Approved, Rejected
    effective_date: date = None
    
    # Schema.org
    result: str = ""         # DecisionResult
```

## Policy Types

| Policy | Schema.org Type | Properties |
|--------|--------------|------------|
| Security Policy | Legislation | requiresAuth, encryption |
| Privacy Policy | Legislation | dataController, consent |
| Acceptable Use | Legislation | permittedUse |
| Data Retention | Legislation | retentionPeriod |
| Incident Response | Guide | responseProcedure |

## Organizational Roles

```python
@dataclass
class GovernanceRole:
    id: str
    name: str = ""           # Role.name
    
    # Hierarchy
    reports_to: str = ""    # Reports to role
    level: int = 0          # Hierarchy level
    scope: str = ""         # Responsibility scope
    
    # Authority
    can_approve: List[str] = []   # Approvable actions
    can_create: List[str] = []    # Creatable entities
    can_delete: List[str] = []    # Deletable entities
    
    # Schema.org
    role_name: str = ""       # Role type
```

## Committee Structure

| Committee | Schema.org Organization |
|-----------|----------------------|
| Board of Directors | Organization > Corporation |
| Executive Team | Organization > Consortium |
| Audit Committee | Organization > Committee |
| Risk Committee | Organization > Committee |
| IT Committee | Organization > Committee |

## Compliance Governance

```python
@dataclass
class ComplianceProgram:
    id: str
    
    # Framework
    framework: str = ""         # SOX, HIPAA, GDPR
    version: str = ""
    
    # Controls
    controls: List[Control] = []
    policies: List[Policy] = []
    
    # Monitoring
    audit_schedule: str = ""
    last_audit: date = None
    next_audit: date = None
    
    # Ownership
    owner: str = ""            # Person
    sponsor: str = ""         # Person
    
    # Schema.org
    credential: str = ""      # Certification
```

## Risk Governance

```python
@dataclass
class Risk:
    id: str
    
    name: str = ""
    description: str = ""
    
    # Classification
    category: str = ""        # Operational, Financial, Compliance
    likelihood: str = ""     # Low, Medium, High
    impact: str = ""         # Low, Medium, High
    
    # Treatment
    mitigation: str = ""
    owner: str = ""
    status: str = ""          # Open, Mitigated, Accepted
    
    # Schema.org
    identifier: str = ""     # Risk ID
```

## Audit Framework

```python
@dataclass
class Audit:
    id: str
    
    # Audit details
    type: str = ""           # Internal, External
    scope: str = ""          # System, Process
    period_start: date = None
    period_end: date = None
    
    # Findings
    findings: List[Finding] = []
    recommendations: List[str] = []
    
    # Status
    status: str = ""         # In Progress, Complete
    opinion: str = ""        # Unqualified, Qualified
    
    # Schema.org
    result: str = ""        # AuditReport
```

## Implementation

```python
# Governance Organization
board = Organization(
    name="Board of Directors",
    additionalType="Corporation"
)

# Executive Team
executive = Organization(
    name="Executive Team",
    parentOrganization=board
)

# Policies
policies = [
    Legislation(name="Security Policy", ...),
    Legislation(name="Privacy Policy", ...),
]

# Roles
roles = [
    GovernanceRole(name="CISO", ...),
    GovernanceRole(name="DPO", ...),
]
```

Reference: https://www.iso.org | https://www.nist.gov | https://www.coso.org