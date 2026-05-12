"""
WaltID Integration - Issue Verified Credentials

Endpoints for issuing Verifiable Credentials using WaltID.

Reference:
- https://github.com/walt-id/waltid-identity
- https://docs.walt.id/identity/wallet-api

Features:
- Create wallet
- Issue credential
- Verify credential
- Present credential
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid
import hashlib
import json
import requests


# =============================================================================
# WALLET CONFIG
# =============================================================================

class WalletConfig:
    """WaltID wallet configuration"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.api_key: str = ""
    
    @property
    def wallet_url(self) -> str:
        return f"{self.base_url}/wallet-api/v1"
    
    @property
    def identity_url(self) -> str:
        return f"{self.base_url}/identity-api/v1"
    
    @property
    def issuer_url(self) -> str:
        return f"{self.base_url}/issuer-api/v1"


# =============================================================================
# VERIFIABLE CREDENTIAL TYPES
# =============================================================================

class CredentialStatus(Enum):
    Active = "active"
    Revoked = "revoked"
    Expired = "expired"
    Suspended = "suspended"


class CredentialType(Enum):
    # W3C Standard
    VerifiableCredential = "VerifiableCredential"
    
    # Custom Types
    AgentCredential = "AgentCredential"
    IdentityCredential = "IdentityCredential"
    SkillCredential = "SkillCredential"
    EmploymentCredential = "EmploymentCredential"
    EducationCredential = "EducationCredential"
    MembershipCredential = "MembershipCredential"
    KYC_credential = "KYCCredential"


@dataclass
class CredentialSubject:
    """Subject of the credential"""
    
    id: str  # DID of the subject
    type: str  # Type of credential
    claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VerifiableCredential:
    """W3C Verifiable Credential"""
    
    # Context
    context: List[str] = field(default_factory=lambda: [
        "https://www.w3.org/2018/credentials/v1"
    ])
    
    # Type
    type: List[str] = field(default_factory=list)
    
    # Issuer
    issuer: str = ""  # DID of issuer
    
    # Issuance date
    issuance_date: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )
    
    # Expiration date
    expiration_date: str = field(
        default_factory=lambda: (
            datetime.utcnow() + timedelta(days=365)
        ).isoformat() + "Z"
    )
    
    # Status
    credential_status: str = ""
    status: CredentialStatus = CredentialStatus.Active
    
    # Subject
    credential_subject: CredentialSubject = field(
        default_factory=CredentialSubject
    )
    
    # Proof
    proof: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    canonical_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )
    version: str = "1.0"
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-LD format"""
        return {
            "@context": self.context,
            "type": self.type,
            "issuer": self.issuer,
            "issuanceDate": self.issuance_date,
            "expirationDate": self.expiration_date,
            "credentialSubject": {
                "id": self.credential_subject.id,
                "type": self.credential_subject.type,
                **self.credential_subject.claims
            },
            "credentialStatus": {
                "id": self.credential_status,
                "type": "CredentialStatusList2020"
            },
            "proof": self.proof
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


# =============================================================================
# WALLET ENDPOINTS
# =============================================================================

@dataclass
class WaltIDClient:
    """WaltID wallet client"""
    
    config: WalletConfig = field(default_factory=WalletConfig)
    
    # =================================================================
    # WALLET MANAGEMENT
    # =================================================================
    
    def create_wallet(self, owner: str) -> Dict[str, Any]:
        """Create a new wallet"""
        response = requests.post(
            f"{self.config.wallet_url}/wallets",
            json={"owner": owner}
        )
        return response.json()
    
    def get_wallet(self, wallet_id: str) -> Dict[str, Any]:
        """Get wallet by ID"""
        response = requests.get(
            f"{self.config.wallet_url}/wallets/{wallet_id}"
        )
        return response.json()
    
    def list_credentials(self, wallet_id: str) -> List[VerifiableCredential]:
        """List credentials in wallet"""
        response = requests.get(
            f"{self.config.wallet_url}/wallets/{wallet_id}/credentials"
        )
        data = response.json()
        return [VerifiableCredential(**c) for c in data]
    
    # =================================================================
    # CREDENTIAL ISSUANCE
    # =================================================================
    
    def issue_credential(
        self,
        issuer_did: str,
        subject_did: str,
        credential_type: str,
        claims: Dict[str, Any],
        private_key_jwt: str = ""
    ) -> VerifiableCredential:
        """Issue a new verifiable credential"""
        
        # Create credential
        credential = VerifiableCredential(
            type=["VerifiableCredential", credential_type],
            issuer=issuer_did,
            credential_subject=CredentialSubject(
                id=subject_did,
                type=credential_type,
                claims=claims
            )
        )
        
        # Sign credential
        response = requests.post(
            f"{self.config.issuer_url}/credentials/issue",
            json={
                "credential": credential.to_dict(),
                "issuerDid": issuer_did,
                "proofType": "JWT",
                "privateKey": private_key_jwt
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            credential.proof = data.get("proof", {})
        
        return credential
    
    def issue_agent_credential(
        self,
        issuer_did: str,
        subject_did: str,
        skills: List[str],
        metadata: Dict[str, Any]
    ) -> VerifiableCredential:
        """Issue an Agent credential"""
        return self.issue_credential(
            issuer_did=issuer_did,
            subject_did=subject_did,
            credential_type="AgentCredential",
            claims={
                "skills": skills,
                "metadata": metadata,
                "entity_type": "SoftwareApplication",
                "owner_type": "Person"
            }
        )
    
    def issue_skill_credential(
        self,
        issuer_did: str,
        subject_did: str,
        skill_name: str,
        skill_level: str,
        evidence: Dict[str, Any]
    ) -> VerifiableCredential:
        """Issue a Skill credential"""
        return self.issue_credential(
            issuer_did=issuer_did,
            subject_did=subject_did,
            credential_type="SkillCredential",
            claims={
                "skill_name": skill_name,
                "skill_level": skill_level,
                "evidence": evidence
            }
        )
    
    def issue_employment_credential(
        self,
        issuer_did: str,
        subject_did: str,
        organization: str,
        role: str,
        start_date: str,
        end_date: Optional[str] = None
    ) -> VerifiableCredential:
        """Issue an Employment credential"""
        return self.issue_credential(
            issuer_did=issuer_did,
            subject_did=subject_did,
            credential_type="EmploymentCredential",
            claims={
                "organization": organization,
                "role": role,
                "start_date": start_date,
                "end_date": end_date or ""
            }
        )
    
    # =================================================================
    # CREDENTIAL VERIFICATION
    # =================================================================
    
    def verify_credential(
        self,
        credential: VerifiableCredential
    ) -> Dict[str, Any]:
        """Verify a credential"""
        response = requests.post(
            f"{self.config.identity_url}/credentials/verify",
            json=credential.to_dict()
        )
        return response.json()
    
    def check_credential_status(
        self,
        credential_id: str
    ) -> CredentialStatus:
        """Check if credential is valid"""
        response = requests.get(
            f"{self.config.issuer_url}/credentials/status/{credential_id}"
        )
        if response.status_code == 200:
            data = response.json()
            return CredentialStatus(data.get("status", "active"))
        return CredentialStatus.Revoked
    
    def revoke_credential(self, credential_id: str) -> bool:
        """Revoke a credential"""
        response = requests.post(
            f"{self.config.issuer_url}/credentials/revoke",
            json={"credentialId": credential_id}
        )
        return response.status_code == 200
    
    # =================================================================
    # CREDENTIAL PRESENTATION
    # =================================================================
    
    def create_presentation(
        self,
        wallet_id: str,
        credentials: List[VerifiableCredential],
        verifier_did: str,
        challenge: str
    ) -> Dict[str, Any]:
        """Create a credential presentation"""
        response = requests.post(
            f"{self.config.wallet_url}/presentations/create",
            json={
                "walletId": wallet_id,
                "credentials": [c.to_dict() for c in credentials],
                "verifierDid": verifier_did,
                "challenge": challenge
            }
        )
        return response.json()
    
    def verify_presentation(
        self,
        presentation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify a presentation"""
        response = requests.post(
            f"{self.config.identity_url}/presentations/verify",
            json=presentation
        )
        return response.json()


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example():
    """Example usage"""
    
    # Create client
    client = WaltIDClient()
    
    # Issue agent credential
    credential = client.issue_agent_credential(
        issuer_did="did:waltid:issuer",
        subject_did="did:waltid:agent123",
        skills=["coding", "data-analysis"],
        metadata={"version": "1.0", "platform": "AGenNext"}
    )
    
    print(credential.to_json())
    
    # Verify
    result = client.verify_credential(credential)
    print(result)


if __name__ == "__main__":
    example()