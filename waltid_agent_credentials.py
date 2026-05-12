"""
WaltID Integration - Agent Credentials

Connect AGenNext enterprise agents with WaltID Verified Credentials.

Reference:
- https://github.com/walt-id/waltid-identity

Schema.org Mapping:
- SoftwareApplication (Agent) → AgentCredential
- Person (Owner) → IdentityCredential  
- Organization → MembershipCredential
- Action → ActionCredential
- Skill → SkillCredential
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from waltid_endpoints import (
    WaltIDClient,
    VerifiableCredential,
    CredentialSubject,
    CredentialType,
    CredentialStatus
)
from base_entity import Entity


# =============================================================================
# AGENT CREDENTIALS
# =============================================================================

@dataclass
class AgentCredentialData:
    """Agent-specific credential data"""
    
    # Agent info
    agent_name: str = ""
    agent_type: str = "SoftwareApplication"
    agent_version: str = "1.0"
    
    # Capabilities
    capabilities: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    
    # Owner info
    owner_id: str = ""
    owner_name: str = ""
    owner_did: str = ""  # WaltID DID
    
    # Organization
    organization_id: str = ""
    organization_name: str = ""
    organization_did: str = ""
    
    # Metadata
    platform: str = "AGenNext"
    runtime: str = ""
    status: str = "active"


@dataclass
class AgentCredentialManager:
    """Manage agent credentials with WaltID"""
    
    client: WaltIDClient = field(default_factory=WaltIDClient)
    issuer_did: str = "did:waltid:agennext"
    
    def issue_agent_credential(
        self,
        agent: Entity,
        agent_data: AgentCredentialData,
        private_key: str = ""
    ) -> VerifiableCredential:
        """Issue credential for an agent"""
        
        credential = self.client.issue_agent_credential(
            issuer_did=self.issuer_did,
            subject_did=f"did:waltid:agent:{agent.canonical_id}",
            skills=agent_data.skills,
            metadata={
                "agent_name": agent_data.agent_name,
                "agent_type": agent_data.agent_type,
                "platform": agent_data.platform,
                "owner_did": agent_data.owner_did,
                "organization_did": agent_data.organization_did,
                "capabilities": agent_data.capabilities,
                "version": agent_data.agent_version
            }
        )
        
        return credential
    
    def issue_owner_identity(
        self,
        person: Entity,
        name: str,
        email: str,
        private_key: str = ""
    ) -> VerifiableCredential:
        """Issue identity credential for agent owner"""
        
        credential = self.client.issue_credential(
            issuer_did=self.issuer_did,
            subject_did=f"did:waltid:person:{person.canonical_id}",
            credential_type="IdentityCredential",
            claims={
                "name": name,
                "email": email,
                "entity_type": "Person"
            },
            private_key_jwt=private_key
        )
        
        return credential
    
    def issue_skill_credential(
        self,
        agent: Entity,
        skill_name: str,
        skill_level: str,
        evidence: Dict[str, Any],
        private_key: str = ""
    ) -> VerifiableCredential:
        """Issue credential for agent skill"""
        
        credential = self.client.issue_skill_credential(
            issuer_did=self.issuer_did,
            subject_did=f"did:waltid:agent:{agent.canonical_id}",
            skill_name=skill_name,
            skill_level=skill_level,
            evidence=evidence
        )
        
        return credential
    
    def issue_employment_credential(
        self,
        person: Entity,
        organization: str,
        role: str,
        start_date: str,
        private_key: str = ""
    ) -> VerifiableCredential:
        """Issue employment credential"""
        
        credential = self.client.issue_employment_credential(
            issuer_did=self.issuer_did,
            subject_did=f"did:waltid:person:{person.canonical_id}",
            organization=organization,
            role=role,
            start_date=start_date
        )
        
        return credential
    
    def verify_agent(
        self,
        credential: VerifiableCredential
    ) -> Dict[str, Any]:
        """Verify agent credential"""
        return self.client.verify_credential(credential)
    
    def revoke_agent_credential(
        self,
        credential: VerifiableCredential
    ) -> bool:
        """Revoke agent credential"""
        return self.client.revoke_credential(
            credential.canonical_id
        )


# =============================================================================
# SCHEMA.ORG INTEGRATION
# =============================================================================

"""
Schema.org → WaltID Credential Mapping:

| Schema.org Type | Credential Type | DID Format |
|---------------|--------------|-----------|
| SoftwareApplication | AgentCredential | did:waltid:agent:{id} |
| Person | IdentityCredential | did:waltid:person:{id} |
| Organization | MembershipCredential | did:waltid:org:{id} |
| Place | LocationCredential | did:waltid:place:{id} |
| Event | AttendanceCredential | did:waltid:event:{id} |
| CreativeWork | CopyrightCredential | did:waltid:work:{id} |
| Action | ActionCredential | did:waltid:action:{id} |
| Intangible | LicenseCredential | did:waltid:license:{id} |
| Product | ProductCredential | did:waltid:product:{id} |
| MedicalEntity | MedicalCredential | did:waltid:medical:{id} |
"""


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example():
    """Example usage"""
    
    from skills_database import Skill
    
    # Create manager
    manager = AgentCredentialManager()
    
    # Sample agent data
    agent_data = AgentCredentialData(
        agent_name="CodingAgent",
        agent_type="SoftwareApplication",
        skills=["python", "javascript"],
        capabilities=["code-generation", "refactoring"],
        owner_name="John Doe",
        owner_did="did:waltid:person:123",
        organization_name="ACorp",
        organization_did="did:waltid:org:456"
    )
    
    # Issue credential
    from base_entity import Entity
    agent = Entity()
    credential = manager.issue_agent_credential(
        agent=agent,
        agent_data=agent_data
    )
    
    print(f"Issued: {credential.canonical_id}")
    
    # Verify
    result = manager.verify_agent(credential)
    print(f"Verified: {result}")


if __name__ == "__main__":
    example()