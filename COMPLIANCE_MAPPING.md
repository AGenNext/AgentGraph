# Compliance Standards Mapping

## Compliance Frameworks → Schema.org

| Framework | Schema.org Type | Domain |
|-----------|----------------|--------|
| **GDPR** | Legislation | Privacy |
| **HIPAA** | MedicalGuideline | Healthcare |
| **SOC2** | Certification | Security |
| **ISO27001** | Certification | Security |
| **PCI-DSS** | Legislation | Finance |
| **SOX** | Legislation | Finance |
| **CCPA** | Legislation | Privacy |
| **FERPA** | Legislation | Education |
| **COPPA** | Legislation | Privacy |
| **GLBA** | Legislation | Finance |
| **HIPAA Security** | MedicalGuideline | Healthcare |

## Compliance Types → Schema.org Structures

### Privacy Laws

| Regulation | Schema.org | Key Fields |
|------------|-----------|-----------|
| GDPR | Legislation | dataController, dataProcessor |
| CCPA | Legislation | rightToDelete, rightToOptOut |
| COPPA | Legislation | parentalConsent, minorAge |

### Security Standards

| Standard | Schema.org | Certification |
|----------|-----------|---------------|
| SOC2 | Credential | auditType, trustServiceCriteria |
| ISO27001 | Credential | securityControl, certification |
| FedRAMP | Credential | impactLevel, authorization |

### Healthcare Compliance

| Regulation | Schema.org | MedicalEntity |
|-----------|------------|------------|
| HIPAA | MedicalGuideline | PHI, securityRule |
| HITECH | MedicalGuideline | breachNotification |
| FERPA | EducationalCredential | studentRecord |

## Implementation

```python
from enum import Enum

class ComplianceFramework(Enum):
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    SOC2 = "SOC 2"
    ISO27001 = "ISO 27001"
    PCI_DSS = "PCI-DSS"
    CCPA = "CCPA"

@dataclass
class ComplianceRequirement:
    id: str
    framework: str
    requirement: str
    
    # Schema.org fields
    description: str = ""
    legal_force: str = ""  # InForce, NotInForce
    jurisdiction: str = ""
    effective_date: Optional[date] = None

@dataclass
class DataProcessingAgreement:
    id: str
    
    # Parties
    controller: str = ""  # Organization
    processor: str = ""     # Organization
    
    # GDPR fields
    purpose: str = ""
    data_types: List[str] = []
    retention_period: str = ""
    transfers: bool = False
    
    # Schema.org
    contract: str = ""    # Legislation
```

## Data Classification

| Level | Schema.org | Example |
|-------|-----------|---------|
| Public | Thing.visibility | Public data |
| Internal | Thing.visibility | Internal docs |
| Confidential | Thing.visibility | Business data |
| Restricted | Thing.visibility | PII, PHI |

## Audit Trail (Schema.org)

```python
@dataclass
class AuditEntry:
    id: str
    
    # What
    action: str = ""           # Schema.org Action
    resource: str = ""        # Resource affected
    resource_type: str = ""   # Schema.org type
    
    # Who
    actor: str = ""           # Person
    actor_role: str = ""       # Role
    
    # When
    timestamp: datetime = None
    
    # Compliance
    compliance_framework: str = ""
    regulation: str = ""
    data_classification: str = ""
```

## Compliance Status

```python
@dataclass
class ComplianceStatus:
    id: str
    
    framework: str              # GDPR, HIPAA, SOC2
    
    # Status fields
    compliant: bool = False
    last_audit: date = None
    next_audit: date = None
    
    # Evidence
    policies: List[str] = []
    certifications: List[str] = []
    controls: List[str] = []
    
    # Schema.org mapping
    credential: str = ""         # Credential type
```

Reference: https://schema.org/docs/legislation | https://www.gdpr-info.eu | https://www.hhs.gov/hipaa