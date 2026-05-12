# Google & Microsoft Schema Mapping

## Google Ecosystem → Schema.org

| Google Service | Schema.org Type | Source |
|---------------|----------------|--------|
| Google Search | WebApplication | - |
| Google Maps | WebPage | schema.org/Place |
| Gmail | WebApplication | schema.org/EmailMessage |
| Google Drive | DataFeed | schema.org/Dataset |
| Google Calendar | WebApplication | schema.org/Schedule |
| Google Analytics | WebApplication | schema.org/AnalysisNewsArticle |
| Google Ads | FinancialProduct | schema.org/Advertising |
| Google Cloud | WebAPI | schema.org/WebAPI |
| YouTube | VideoObject | schema.org/VideoObject |
| Android | OperatingSystem | schema.org/OperatingSystem |
| Chrome | WebBrowser | schema.org/SoftwareApplication |
| TensorFlow | ML Framework | schema.org/Code |
| BERT | ML Model | schema.org/MLModel |

## Microsoft Ecosystem → Schema.org

| Microsoft Service | Schema.org Type | Source |
|-------------------|----------------|--------|
| Azure | CloudPlatform | schema.org/WebAPI |
| Office 365 | SoftwareSuite | schema.org/SoftwareApplication |
| Teams | WebApplication | schema.org/Communication |
| Outlook | WebApplication | schema.org/EmailMessage |
| OneDrive | DataFeed | schema.org/Dataset |
| SharePoint | WebPage | schema.org/WebPage |
|Power Automate| WorkflowAutomation | schema.org/AutomateAction |
| Power Apps | SoftwareApplication | schema.org/MobileApplication |
| Azure DevOps | WebApplication | schema.org/CodeRepository |
| SQL Server | Database | schema.org/Database |
| LinkedIn | SocialNetwork | schema.org/SocialNetwork |
| .NET | RuntimePlatform | schema.org/RuntimePlatform |
| Visual Studio | SoftwareApplication | schema.org/IDE |

## API Reference Mapping

| Company | API | Schema.org Type | Endpoint |
|---------|-----|-----------------|----------|
| Google | Custom Search | WebAPI | api.google.com |
| Google | Maps JavaScript | WebAPI | maps.googleapis.com |
| Google | Gmail API | WebAPI | gmail.googleapis.com |
| Google | Calendar API | WebAPI | calendar.googleapis.com |
| Google | Drive API | WebAPI | www.googleapis.com |
| Google | YouTube Data | WebAPI | youtube.googleapis.com |
| Google | Cloud Storage | WebAPI | storage.googleapis.com |
| Microsoft | Graph API | WebAPI | graph.microsoft.com |
| Microsoft | Azure AD | WebAPI | login.microsoft.com |
| Microsoft | Azure Storage | WebAPI | core.windows.net |
| Microsoft | Teams API | WebAPI | teams.microsoft.com |

## OAuth Integration

| Provider | Schema.org Type | Scope |
|----------|----------------|-------|
| Google OAuth | ActionAccessSpecification | OAuth2 |
| Microsoft OAuth | ActionAccessSpecification | OAuth2 |
| GitHub OAuth | ActionAccessSpecification | OAuth2 |

## Product Mapping

```python
@dataclass
class CloudProduct:
    name: str = ""             # Product.name
    provider: str = ""         # Product.brand (Organization)
    category: str = ""        # Product.category
    pricing: str = ""          # Offer.price
    features: List[str] = []   # Product.feature
    
    # Cloud-specific
    region: str = ""           # Place (region)
    availability: str = ""   # Offer.availability
    tier: str = ""            # Offer.level
```

## Service Mapping

| Service | Schema.org Service |
|---------|------------------|
| Google Cloud Run | WebService |
| Azure Functions | WebService |
| AWS Lambda | WebService |

## Implementation

```python
google_products = {
    "cloud_platform": Product(
        name="Google Cloud",
        brand="Alphabet",
        category="Cloud Computing",
        offer=Offer(price="Pay per use")
    ),
    "search": Product(
        name="Google Search",
        brand="Alphabet",
        category="Search Engine"
    ),
    "maps": Product(
        name="Google Maps Platform",
        brand="Alphabet",
        category="Mapping API"
    )
}

microsoft_products = {
    "azure": Product(
        name="Microsoft Azure",
        brand="Microsoft",
        category="Cloud Computing",
        offer=Offer(price="Pay per use")
    ),
    "office365": Product(
        name="Microsoft 365",
        brand="Microsoft",
        category="Productivity Suite"
    ),
    "teams": Product(
        name="Microsoft Teams",
        brand="Microsoft",
        category="Communication"
    )
}
```

Reference: https://cloud.google.com/docs | https://docs.microsoft.com/