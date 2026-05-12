# All Frameworks Complete Reference

## Integration of All Standards & Frameworks

### Complete Framework Map

| Category | Frameworks | Schema.org Files |
|----------|-----------|------------------|
| **Core** | Schema.org V30.0 | ALL |
| **Compliance** | GDPR, HIPAA, SOC2, ISO27001, PCI-DSS, CCPA, FERPA, COPPA | COMPLIANCE_MAPPING |
| **Security** | OAuth2, SAML, TLS, JWT, OpenID | SECURITY_PROTOCOLS |
| **Governance** | ITIL, COBIT, TOGAF, NIST, COSO, ISO37301 | GOVERNANCE_PROTOCOLS |
| **Cloud** | AWS, Azure, GCP | CLOUD_PROVIDERS |
| **W3 Standards** | JSON-LD, RDF, Dublin Core, FOAF | W3_STANDARDS |
| **OS** | Linux (POSIX) | LINUX_INSIGHTS |
| **Best Practices** | Google, Microsoft SEO | BEST_PRACTICES |

## Complete Reference

### 1. Core Schema.org Types (11)

```
Thing (root)
├── Action (16 categories, 78 types)
├── CreativeWork (20+ subtypes)
├── Event (15+ subtypes)
├── Intangible (30+ subtypes)
├── MedicalEntity (20+ subtypes)
├── Organization (50+ subtypes)
├── Person (+ Patient)
├── Place (30+ subtypes)
├── Product (10+ subtypes)
└── StructuredValue (25+ subtypes)
```

### 2. Compliance Frameworks

| Framework | Domain | Schema.org Type |
|-----------|--------|---------------|
| GDPR | Privacy | Legislation |
| CCPA | Privacy | Legislation |
| COPPA | Privacy | Legislation |
| HIPAA | Healthcare | MedicalGuideline |
| HITECH | Healthcare | MedicalGuideline |
| SOC2 | Security | Credential |
| ISO27001 | Security | Credential |
| PCI-DSS | Finance | Legislation |
| SOX | Finance | Legislation |
| GLBA | Finance | Legislation |
| FERPA | Education | EducationalCredential |

### 3. Security Protocols

| Protocol | Use | Schema.org Action |
|---------|-----|-----------------|
| OAuth2 | Auth | AuthorizeAction |
| SAML | Auth | AuthenticateAction |
| OIDC | Auth | AuthorizeAction |
| JWT | Token | Credentials |
| TLS 1.3 | Transport | ActionAccessSpecification |
| SSH | Transport | ActionAccessSpecification |
| LDAP | Auth | AuthenticateAction |
| Kerberos | Auth | AuthenticateAction |

### 4. Governance Frameworks

| Framework | Purpose | Schema.org Type |
|-----------|---------|----------------|
| ITIL | Service Management | Guide |
| COBIT | IT Governance | Guide |
| TOGAF | Architecture | Guide |
| NIST CSF | Cybersecurity | Legislation |
| COSO | Internal Controls | Guide |
| ISO 37301 | Compliance | Credential |

### 5. Cloud Providers

| Provider | Product Type | Service Type |
|----------|------------|-----------|
| AWS | CloudPlatform | WebAPI |
| Azure | CloudPlatform | WebAPI |
| GCP | CloudPlatform | WebAPI |
| Google Cloud Run | Container | WebService |
| Azure Functions | FaaS | WebService |
| AWS Lambda | FaaS | WebService |

### 6. Standards Bodies

| Body | Schema.org Organization | Standards |
|------|---------------------|---------|
| ISO | StandardsOrganization | ISO 27001, etc. |
| IETF | StandardsOrganization | RFC standards |
| W3C | StandardsOrganization | HTML, JSON-LD |
| IEEE | StandardsOrganization | Technical |
| NIST | GovernmentOrganization | NIST CSF |
| IEC | StandardsOrganization | International |

### 7. Data Types (Schema.org)

| Type | Python | Example |
|------|--------|---------|
| Boolean | bool | True |
| Date | date | 2024-01-15 |
| DateTime | datetime | 2024-01-15T10:00:00 |
| Float | float | 3.14 |
| Integer | int | 42 |
| Text | str | "text" |
| Time | time | 10:00:00 |
| URL | str | "https://" |
| Duration | str | "PT1H" |

### 8. Enumerations

| Enumeration | Values |
|--------------|--------|
| DayOfWeek | Monday-Sunday |
| ItemAvailability | InStock, OutOfStock, PreOrder |
| EventStatusType | Scheduled, Cancelled, Postponed |
| OrderStatus | Processing, Delivered, Cancelled |
| PaymentStatusType | Pending, Completed, Failed |

### 9. Relationships

| Relationship | Schema.org Property |
|--------------|-------------------|
| Person works for | worksFor → Organization |
| Product made by | manufacturer → Organization |
| Event at | location → Place |
| Book written by | author → Person |
| Movie directed by | director → Person |
| Offer has price | offers → Offer |

### 10. Implementation Coverage

| Category | Count | Status |
|----------|-------|-------|
| Core Types | 11 | ✅ Complete |
| Sub-types | 100+ | ✅ Covered |
| Properties | 200+ | ✅ Defined |
| Enumerations | 50+ | ✅ Defined |
| Actions | 78 | ✅ Mapped |

### 11. Complete Mapping Files

| File | Purpose |
|------|---------|
| SCHEMA_COVERAGE.md | Core types coverage |
| SCHEMA_FULL_MAPPING.md | Complete type mapping |
| SCHEMA_PROPERTIES.md | All properties |
| SCHEMA_VALUES.md | Value types |
| SCHEMA_WIRING.md | Full wiring |
| SCHEMA_ORG_MAPPING.md | Type mappings |
| CONNECTION_MAP.md | Entity relationships |
| W3_STANDARDS.md | W3 standards |
| LINUX_INSIGHTS.md | Linux mapping |
| CLOUD_PROVIDERS.md | Cloud providers |
| COMPLIANCE_MAPPING.md | Compliance |
| SECURITY_PROTOCOLS.md | Security |
| GOVERNANCE_PROTOCOLS.md | Governance |
| BEST_PRACTICES.md | Implementation guide |

### 12. Database Coverage

| Database | Schema.org Types |
|----------|-----------------|
| movie_database | Movie, VideoObject |
| book_database | Book |
| music_database | MusicRecording, MusicAlbum |
| travel_database | Flight, Hotel, Place |
| events_database | Event, Festival, Conference |
| sports_database | SportsEvent, SportsTeam |
| retail_database | Product, Offer |
| food_database | Restaurant, Recipe |
| healthcare_database | MedicalEntity, Drug, Hospital |
| banking_database | BankAccount, FinancialProduct |
| insurance_database | InsuranceProduct |
| realestate_database | RealEstateListing |
| crypto_database | FinancialProduct |
| news_database | NewsArticle |
| automotive_database | Vehicle |
| nonprofit_database | Nonprofit |
| education_database | EducationalOrganization |
| iot_database | Device |
| gaming_database | VideoGame |
| skills_database | Service, JobPosting |
| software_media | SoftwareApplication, MediaObject |
| webcontent_database | WebPage, FAQPage, HowTo |
| software_categories | SoftwareApplication |

Reference: https://schema.org/docs/full.html