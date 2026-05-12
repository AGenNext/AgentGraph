# Security Protocols Mapping

## Authentication Protocols → Schema.org

| Protocol | Schema.org Action | Implementation |
|----------|------------------|----------------|
| **OAuth2.0** | AuthorizeAction | Action with consent |
| **SAML** | AuthenticateAction | Single Sign-On |
| **OpenID Connect** | AuthorizeAction | OIDC flow |
| **LDAP** | AuthenticateAction | Directory auth |
| **Kerberos** | AuthenticateAction | Windows auth |
| **API Key** | IdentifyAction | Token auth |
| **JWT** | AuthorizeAction | Token auth |
| **SSH Key** | AuthenticateAction | Key auth |

## Authorization Models → Schema.org

| Model | Schema.org Type | Description |
|-------|------------------|-------------|
| **RBAC** | Role | Role-based access |
| **ABAC** | Role | Attribute-based |
| **DAC** | ACL | Discretionary |
| **MAC** | Enumeration | Mandatory |

## Encryption Standards

| Type | Schema.org | Use Case |
|------|-----------|---------|
| **TLS 1.3** | ActionAccessSpecification | Transport |
| **AES-256** | Encryption | Data at rest |
| **RSA** | PublicKeyCrypto | Key exchange |
| **SHA-256** | CryptographicHash | Integrity |
| **Argon2** | CryptographicHash | Password hash |
| **HKDF** | KeyDerivationFunction | Key derivation |

## Security Actions

```python
@dataclass
class SecurityAction:
    id: str
    
    action_type: str = ""        # Schema.org Action
    protocol: str = ""          # OAuth2, SAML, etc.
    mechanism: str = ""          # Authentication mechanism
    
    # Auth fields
    requires_mfa: bool = False
    session_timeout: int = 3600
    max_attempts: int = 3
    
    # Schema.org
    result: str = ""             # Success/Failure
    target: str = ""            # Resource
```

## JWT Structure

```python
@dataclass
class JWT:
    # Header
    alg: str = "RS256"          # Algorithm
    typ: str = "JWT"
    
    # Payload
    sub: str = ""              # Subject (Person)
    iss: str = ""              # Issuer
    aud: str = ""              # Audience
    exp: int = 0              # Expiration
    iat: int = 0              # Issued at
    nbf: int = 0              # Not before
    
    # Custom claims
    roles: List[str] = []       # Role
    permissions: List[str] = []  # Permission
    organization: str = ""        # Organization
```

## API Security

| Standard | Schema.org Type | Port |
|----------|---------------|------|
| **HTTPS** | URL | 443 |
| **WSS** | URL | 443 |
| **SSH** | URL | 22 |
| **SFTP** | URL | 22 |

## Common Vulnerabilities → Schema.org

| Vulnerability | Schema.org | Mitigation |
|-------------|----------|------------|
| SQL Injection | ValidateAction | Input sanitization |
| XSS | ValidateAction | Output encoding |
| CSRF | Token | Anti-CSRF token |
| SSRF | RestrictAction | URL validation |
| IDOR | AuthorizeAction | Access control |
| Path Traversal | ValidateAction | Path sanitize |

## OAuth2 Flows

| Grant Type | Schema.org Action | Use Case |
|-----------|--------------------|----------|
| Authorization Code | AuthorizeAction | Web apps |
| Implicit | AuthorizeAction | SPA |
| Client Credentials | AuthenticateAction | M2M |
| Refresh Token | UpdateAction | Token refresh |

## Security Headers (HTTP)

| Header | Schema.org Property | Value |
|--------|-------------------|-------|
| Strict-Transport-Security | url (secure) | max-age=31536000 |
| Content-Security-Policy | identifier | policy |
| X-Content-Type-Options | contentType | nosniff |
| X-Frame-Options | allow | DENY |
| X-XSS-Protection | protection | 1 |
| Referrer-Policy | referrer | strict-origin |

## Implementation

```python
@dataclass
class SecurityPolicy:
    id: str
    
    # Protocol
    auth_protocol: str = ""      # OAuth2, SAML
    encryption: str = ""         # AES-256, TLS
    
    # Access
    role: str = ""              # Role-based
    permission: List[str] = [] 
    
    # Compliance
    mfa_required: bool = False
    session_timeout: int = 3600
    
    # Schema.org
    accepted_payment: List[str] = []  # PaymentMethod
```

Reference: https://schema.org/docs/action-hierarchy | https://oauth.net/2/ | https://tools.ietf.org/html/rfc6749