"""
WaltID API Endpoints Documentation

Complete list of all WaltID API endpoints.

Reference:
- https://github.com/walt-id/waltid-identity
- https://docs.walt.id/
- https://walt.id/blog/product-update-26

APIs:
1. Wallet API (wallet-api)
2. Identity API (identity-api)  
3. Issuer API (issuer-api)
4. Verifier API (verifier-api)

Base URL (local): http://localhost:8080
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


# =============================================================================
# API GROUPS
# =============================================================================

class APIType(Enum):
    WALLET = "wallet-api"
    IDENTITY = "identity-api"
    ISSUER = "issuer-api"
    VERIFIER = "verifier-api"


@dataclass
class APIEndpoint:
    """API endpoint definition"""
    method: str
    path: str
    description: str
    api_type: APIType
    parameters: Dict[str, Any] = field(default_factory=dict)
    request_body: Optional[Dict[str, Any]] = None
    response: Optional[Dict[str, Any]] = None


# =============================================================================
# WALLET API ENDPOINTS
# =============================================================================

WALLET_API_ENDPOINTS: List[APIEndpoint] = [
    # =========================================================================
    # WALLETS
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/wallets",
        description="Create a new wallet",
        api_type=APIType.WALLET,
        request_body={"owner": "string"}
    ),
    APIEndpoint(
        method="GET",
        path="/wallets/{walletId}",
        description="Get wallet by ID",
        api_type=APIType.WALLET,
        parameters={"walletId": "string"}
    ),
    APIEndpoint(
        method="GET",
        path="/wallets",
        description="List all wallets",
        api_type=APIType.WALLET
    ),
    APIEndpoint(
        method="DELETE",
        path="/wallets/{walletId}",
        description="Delete wallet",
        api_type=APIType.WALLET,
        parameters={"walletId": "string"}
    ),
    
    # =========================================================================
    # KEYS
    # =========================================================================
    APIEndpoint(
        method="GET",
        path="/wallets/{walletId}/keys",
        description="List all keys in wallet",
        api_type=APIType.WALLET,
        parameters={"walletId": "string"}
    ),
    APIEndpoint(
        method="POST",
        path="/wallets/{walletId}/keys",
        description="Add key to wallet",
        api_type=APIType.WALLET,
        parameters={"walletId": "string"},
        request_body={"keyType": "string", "algorithm": "string"}
    ),
    APIEndpoint(
        method="PUT",
        path="/wallets/{walletId}/keys/{keyId}",
        description="Update key in wallet",
        api_type=APIType.WALLET,
        parameters={"walletId": "string", "keyId": "string"},
        request_body={"keyType": "string"}
    ),
    APIEndpoint(
        method="DELETE",
        path="/wallets/{walletId}/keys/{keyId}",
        description="Delete key from wallet",
        api_type=APIType.WALLET,
        parameters={"walletId": "string", "keyId": "string"}
    ),
    
    # =========================================================================
    # CREDENTIALS
    # =========================================================================
    APIEndpoint(
        method="GET",
        path="/wallets/{walletId}/credentials",
        description="List credentials in wallet",
        api_type=APIType.WALLET,
        parameters={"walletId": "string"}
    ),
    APIEndpoint(
        method="POST",
        path="/wallets/{walletId}/credentials",
        description="Add credential to wallet",
        api_type=APIType.WALLET,
        parameters={"walletId": "string"},
        request_body={"credential": "object"}
    ),
    APIEndpoint(
        method="GET",
        path="/wallets/{walletId}/credentials/{credentialId}",
        description="Get specific credential",
        api_type=APIType.WALLET,
        parameters={"walletId": "string", "credentialId": "string"}
    ),
    APIEndpoint(
        method="DELETE",
        path="/wallets/{walletId}/credentials/{credentialId}",
        description="Delete credential",
        api_type=APIType.WALLET,
        parameters={"walletId": "string", "credentialId": "string"}
    ),
    
    # =========================================================================
    # PRESENTATIONS
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/wallets/{walletId}/presentations",
        description="Create credential presentation",
        api_type=APIType.WALLET,
        parameters={"walletId": "string"},
        request_body={
            "credentials": ["object"],
            "verifierDid": "string",
            "challenge": "string"
        }
    ),
    APIEndpoint(
        method="GET",
        path="/wallets/{walletId}/presentations/{presentationId}",
        description="Get presentation",
        api_type=APIType.WALLET,
        parameters={"walletId": "string", "presentationId": "string"}
    ),
    
    # =========================================================================
    # OIDC
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/wallets/{walletId}/oidc/login",
        description="OIDC login initiation",
        api_type=APIType.WALLET,
        parameters={"walletId": "string"},
        request_body={"clientId": "string", "redirectUri": "string"}
    ),
    APIEndpoint(
        method="GET",
        path="/wallets/{walletId}/oidc/callback",
        description="OIDC callback handler",
        api_type=APIType.WALLET,
        parameters={"walletId": "string", "code": "string"}
    ),
]


# =============================================================================
# IDENTITY API ENDPOINTS
# =============================================================================

IDENTITY_API_ENDPOINTS: List[APIEndpoint] = [
    # =========================================================================
    # IDENTITIES (DID)
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/identities",
        description="Create new identity (DID)",
        api_type=APIType.IDENTITY,
        request_body={
            "method": "string",  # key, web, etc.
            "keyType": "string"
        }
    ),
    APIEndpoint(
        method="GET",
        path="/identities/{did}",
        description="Get identity by DID",
        api_type=APIType.IDENTITY,
        parameters={"did": "string"}
    ),
    APIEndpoint(
        method="PUT",
        path="/identities/{did}",
        description="Update identity",
        api_type=APIType.IDENTITY,
        parameters={"did": "string"},
        request_body={"document": "object"}
    ),
    APIEndpoint(
        method="DELETE",
        path="/identities/{did}",
        description="Delete identity",
        api_type=APIType.IDENTITY,
        parameters={"did": "string"}
    ),
    
    # =========================================================================
    # DID DOCUMENTS
    # =========================================================================
    APIEndpoint(
        method="GET",
        path="/identities/{did}/did-document",
        description="Get DID document",
        api_type=APIType.IDENTITY,
        parameters={"did": "string"}
    ),
    
    # =========================================================================
    # SIGNING & VERIFICATION
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/identities/{did}/sign",
        description="Sign data with identity key",
        api_type=APIType.IDENTITY,
        parameters={"did": "string"},
        request_body={
            "data": "string",
            "privateKey": "string"
        }
    ),
    APIEndpoint(
        method="POST",
        path="/identities/{did}/verify",
        description="Verify signature",
        api_type=APIType.IDENTITY,
        parameters={"did": "string"},
        request_body={
            "data": "string",
            "signature": "string"
        }
    ),
    
    # =========================================================================
    # SERVICES
    # =========================================================================
    APIEndpoint(
        method="GET",
        path="/identities/{did}/services",
        description="List identity services",
        api_type=APIType.IDENTITY,
        parameters={"did": "string"}
    ),
    APIEndpoint(
        method="POST",
        path="/identities/{did}/services",
        description="Add service to identity",
        api_type=APIType.IDENTITY,
        parameters={"did": "string"},
        request_body={"type": "string", "endpoint": "string"}
    ),
    APIEndpoint(
        method="DELETE",
        path="/identities/{did}/services/{serviceId}",
        description="Delete service",
        api_type=APIType.IDENTITY,
        parameters={"did": "string", "serviceId": "string"}
    ),
]


# =============================================================================
# ISSUER API ENDPOINTS
# =============================================================================

ISSUER_API_ENDPOINTS: List[APIEndpoint] = [
    # =========================================================================
    # ISSUANCE OFFERS
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/issuance/offers",
        description="Create issuance offer",
        api_type=APIType.ISSUER,
        request_body={
            "credential": "object",
            "issuerDid": "string",
            "offerLifetime": "number"
        }
    ),
    APIEndpoint(
        method="GET",
        path="/issuance/offers/{offerId}",
        description="Get issuance offer",
        api_type=APIType.ISSUER,
        parameters={"offerId": "string"}
    ),
    APIEndpoint(
        method="DELETE",
        path="/issuance/offers/{offerId}",
        description="Delete issuance offer",
        api_type=APIType.ISSUER,
        parameters={"offerId": "string"}
    ),
    
    # =========================================================================
    # CREDENTIALS
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/issuance/credentials",
        description="Issue credential",
        api_type=APIType.ISSUER,
        request_body={
            "credential": "object",
            "issuerDid": "string",
            "proofType": "string",  # JWT, LD_PROOF
            "privateKey": "string"
        }
    ),
    APIEndpoint(
        method="GET",
        path="/issuance/credentials/{credId}",
        description="Get issued credential",
        api_type=APIType.ISSUER,
        parameters={"credId": "string"}
    ),
    
    # =========================================================================
    # ISSUER METADATA
    # =========================================================================
    APIEndpoint(
        method="GET",
        path="/issuer/metadata",
        description="Get issuer metadata",
        api_type=APIType.ISSUER
    ),
    APIEndpoint(
        method="POST",
        path="/issuer/metadata",
        description="Update issuer metadata",
        api_type=APIType.ISSUER,
        request_body={"name": "string", "styles": "object"}
    ),
    
    # =========================================================================
    # ISSUER KEYS
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/issuer/key",
        description="Add issuer key",
        api_type=APIType.ISSUER,
        request_body={
            "keyType": "string",
            "algorithm": "string",
            "seed": "string"
        }
    ),
    APIEndpoint(
        method="GET",
        path="/issuer/keys/{keyId}",
        description="Get issuer key",
        api_type=APIType.ISSUER,
        parameters={"keyId": "string"}
    ),
    APIEndpoint(
        method="DELETE",
        path="/issuer/keys/{keyId}",
        description="Delete issuer key",
        api_type=APIType.ISSUER,
        parameters={"keyId": "string"}
    ),
    
    # =========================================================================
    # CREDENTIAL STATUS
    # =========================================================================
    APIEndpoint(
        method="GET",
        path="/credentials/status/{credentialId}",
        description="Check credential status",
        api_type=APIType.ISSUER,
        parameters={"credentialId": "string"}
    ),
    APIEndpoint(
        method="POST",
        path="/credentials/revoke",
        description="Revoke credential",
        api_type=APIType.ISSUER,
        request_body={"credentialId": "string"}
    ),
]


# =============================================================================
# VERIFIER API ENDPOINTS
# =============================================================================

VERIFIER_API_ENDPOINTS: List[APIEndpoint] = [
    # =========================================================================
    # PRESENTATIONS
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/verifier/presentations",
        description="Verify presentation",
        api_type=APIType.VERIFIER,
        request_body={"presentation": "object", "challenge": "string"}
    ),
    APIEndpoint(
        method="GET",
        path="/verifier/presentations/{presId}",
        description="Get verification result",
        api_type=APIType.VERIFIER,
        parameters={"presId": "string"}
    ),
    
    # =========================================================================
    # POLICIES
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/verifier/policies",
        description="Create verification policy",
        api_type=APIType.VERIFIER,
        request_body={
            "name": "string",
            "constraints": "object",
            "trustedIssuers": ["string"]
        }
    ),
    APIEndpoint(
        method="GET",
        path="/verifier/policies",
        description="List policies",
        api_type=APIType.VERIFIER
    ),
    APIEndpoint(
        method="GET",
        path="/verifier/policies/{policyId}",
        description="Get policy",
        api_type=APIType.VERIFIER,
        parameters={"policyId": "string"}
    ),
    APIEndpoint(
        method="PUT",
        path="/verifier/policies/{policyId}",
        description="Update policy",
        api_type=APIType.VERIFIER,
        parameters={"policyId": "string"},
        request_body={"name": "string", "constraints": "object"}
    ),
    APIEndpoint(
        method="DELETE",
        path="/verifier/policies/{policyId}",
        description="Delete policy",
        api_type=APIType.VERIFIER,
        parameters={"policyId": "string"}
    ),
    
    # =========================================================================
    # VERIFIER METADATA
    # =========================================================================
    APIEndpoint(
        method="GET",
        path="/verifier/metadata",
        description="Get verifier metadata",
        api_type=APIType.VERIFIER
    ),
    
    # =========================================================================
    # VALIDATION
    # =========================================================================
    APIEndpoint(
        method="POST",
        path="/verifier/validate",
        description="Validate credentials against policy",
        api_type=APIType.VERIFIER,
        request_body={
            "credentials": ["object"],
            "policyId": "string"
        }
    ),
]


# =============================================================================
# ALL ENDPOINTS
# =============================================================================

ALL_ENDPOINTS = (
    WALLET_API_ENDPOINTS +
    IDENTITY_API_ENDPOINTS +
    ISSUER_API_ENDPOINTS +
    VERIFIER_API_ENDPOINTS
)


def get_endpoints_by_api(api_type: APIType) -> List[APIEndpoint]:
    """Get endpoints by API type"""
    return [e for e in ALL_ENDPOINTS if e.api_type == api_type]


def get_endpoint_count() -> Dict[str, int]:
    """Get endpoint count by API"""
    return {
        "wallet": len(WALLET_API_ENDPOINTS),
        "identity": len(IDENTITY_API_ENDPOINTS),
        "issuer": len(ISSUER_API_ENDPOINTS),
        "verifier": len(VERIFIER_API_ENDPOINTS),
        "total": len(ALL_ENDPOINTS)
    }


# =============================================================================
# SUMMARY TABLE
# =============================================================================

"""
WaltID API Summary:

| API | Base Path | Endpoints | Description |
|-----|----------|----------|-------------|
| Wallet API | /wallet-api/v1 | 17 | Wallet, keys, credentials, presentations, OIDC |
| Identity API | /identity-api/v1 | 12 | DID management, signing, verification |
| Issuer API | /issuer-api/v1 | 14 | Credential issuance, status, revocation |
| Verifier API | /verifier-api/v1 | 10 | Presentation verification, policies |
|-----|----------|----------|-------------|
| TOTAL | | 53 | All endpoints |
"""


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example():
    """Example usage"""
    
    # Get all endpoints
    print(f"Total endpoints: {len(ALL_ENDPOINTS)}")
    
    # Get by API type
    wallet_endpoints = get_endpoints_by_api(APIType.WALLET)
    print(f"Wallet endpoints: {len(wallet_endpoints)}")
    
    # Get counts
    counts = get_endpoint_count()
    print(counts)


if __name__ == "__main__":
    example()