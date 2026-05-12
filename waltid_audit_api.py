"""
WaltID Audit Log REST API

REST API for immutable audit log operations.

Reference:
- https://github.com/walt-id/waltid-identity
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid
import json
from waltid_audit_log import (
    WaltIDAuditLog,
    AuditOperation,
    AuditEntry,
    AuditLog
)
from base_entity import Entity


# =============================================================================
# API MODELS
# =============================================================================

@dataclass
class AuditRequest:
    """Audit log API request"""
    operation: str
    actor: str
    target: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditResponse:
    """Audit log API response"""
    entry_id: str
    timestamp: str
    operation: str
    status: str
    entry_hash: str
    signature: str


@dataclass
class AuditChainStatus:
    """Chain verification status"""
    is_valid: bool
    entry_count: int
    latest_hash: str
    verified_at: str


# =============================================================================
# API ENDPOINTS
# =============================================================================

class AuditAPI:
    """Audit log REST API"""
    
    def __init__(self, issuer_did: str = ""):
        self.audit = WaltIDAuditLog(issuer_did=issuer_did)
    
    # =========================================================================
    # WALLET ENDPOINTS
    # =========================================================================
    
    def create_wallet(
        self,
        actor: str,
        wallet_id: str,
        owner: str
    ) -> AuditResponse:
        """POST /audit/wallets - Create wallet entry"""
        
        entry = self.audit.log_wallet_create(
            actor=actor,
            wallet_id=wallet_id,
            owner=owner
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="created",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def delete_wallet(
        self,
        actor: str,
        wallet_id: str
    ) -> AuditResponse:
        """DELETE /audit/wallets/{id} - Delete wallet entry"""
        
        entry = self.audit.log_wallet_delete(
            actor=actor,
            wallet_id=wallet_id
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="deleted",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def get_wallet_history(
        self,
        wallet_id: str
    ) -> List[Dict[str, Any]]:
        """GET /audit/wallets/{id}/history - Get wallet history"""
        
        entries = self.audit.get_wallet_history(wallet_id)
        
        return [e.to_dict() for e in entries]
    
    # =========================================================================
    # KEY ENDPOINTS
    # =========================================================================
    
    def add_key(
        self,
        actor: str,
        wallet_id: str,
        key_id: str,
        key_type: str
    ) -> AuditResponse:
        """POST /audit/keys - Add key entry"""
        
        entry = self.audit.log_key_add(
            actor=actor,
            wallet_id=wallet_id,
            key_id=key_id,
            key_type=key_type
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="added",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def delete_key(
        self,
        actor: str,
        key_id: str
    ) -> AuditResponse:
        """DELETE /audit/keys/{id} - Delete key entry"""
        
        entry = self.audit.log_key_delete(
            actor=actor,
            key_id=key_id
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="deleted",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    # =========================================================================
    # CREDENTIAL ENDPOINTS
    # =========================================================================
    
    def issue_credential(
        self,
        actor: str,
        credential_id: str,
        subject_did: str,
        credential_type: str
    ) -> AuditResponse:
        """POST /audit/credentials - Issue credential entry"""
        
        entry = self.audit.log_credential_issue(
            actor=actor,
            credential_id=credential_id,
            subject_did=subject_did,
            credential_type=credential_type
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="issued",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def revoke_credential(
        self,
        actor: str,
        credential_id: str
    ) -> AuditResponse:
        """POST /audit/credentials/revoke - Revoke credential"""
        
        entry = self.audit.log_credential_revoke(
            actor=actor,
            credential_id=credential_id
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="revoked",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def verify_credential(
        self,
        actor: str,
        credential_id: str,
        verified: bool
    ) -> AuditResponse:
        """POST /audit/credentials/verify - Verify credential"""
        
        entry = self.audit.log_credential_verify(
            actor=actor,
            credential_id=credential_id,
            verified=verified
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="verified" if verified else "failed",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def get_credential_history(
        self,
        credential_id: str
    ) -> List[Dict[str, Any]]:
        """GET /audit/credentials/{id}/history - Get credential history"""
        
        entries = self.audit.get_credential_history(credential_id)
        
        return [e.to_dict() for e in entries]
    
    # =========================================================================
    # PRESENTATION ENDPOINTS
    # =========================================================================
    
    def create_presentation(
        self,
        actor: str,
        presentation_id: str,
        credentials: List[str]
    ) -> AuditResponse:
        """POST /audit/presentations - Create presentation entry"""
        
        entry = self.audit.log_presentation_create(
            actor=actor,
            presentation_id=presentation_id,
            credentials=credentials
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="created",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def verify_presentation(
        self,
        actor: str,
        presentation_id: str,
        verified: bool
    ) -> AuditResponse:
        """POST /audit/presentations/verify - Verify presentation"""
        
        entry = self.audit.log_presentation_verify(
            actor=actor,
            presentation_id=presentation_id,
            verified=verified
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="verified" if verified else "failed",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    # =========================================================================
    # IDENTITY ENDPOINTS
    # =========================================================================
    
    def create_identity(
        self,
        actor: str,
        did: str,
        method: str
    ) -> AuditResponse:
        """POST /audit/identities - Create identity entry"""
        
        entry = self.audit.log_identity_create(
            actor=actor,
            did=did,
            method=method
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="created",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def update_identity(
        self,
        actor: str,
        did: str
    ) -> AuditResponse:
        """PUT /audit/identities/{did} - Update identity"""
        
        entry = self.audit.log_identity_update(
            actor=actor,
            did=did
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="updated",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def delete_identity(
        self,
        actor: str,
        did: str
    ) -> AuditResponse:
        """DELETE /audit/identities/{did} - Delete identity"""
        
        entry = self.audit.log_identity_delete(
            actor=actor,
            did=did
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="deleted",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def get_identity_history(
        self,
        did: str
    ) -> List[Dict[str, Any]]:
        """GET /audit/identities/{did}/history - Get identity history"""
        
        entries = self.audit.get_identity_history(did)
        
        return [e.to_dict() for e in entries]
    
    # =========================================================================
    # SIGNING ENDPOINTS
    # =========================================================================
    
    def sign_data(
        self,
        actor: str,
        did: str,
        data_hash: str
    ) -> AuditResponse:
        """POST /audit/sign - Log signing"""
        
        entry = self.audit.log_sign(
            actor=actor,
            did=did,
            data_hash=data_hash
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="signed",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    def verify_signature(
        self,
        actor: str,
        did: str,
        signature: str,
        verified: bool
    ) -> AuditResponse:
        """POST /audit/verify - Log verification"""
        
        entry = self.audit.log_verify(
            actor=actor,
            did=did,
            signature=signature,
            verified=verified
        )
        
        return AuditResponse(
            entry_id=entry.entry_id,
            timestamp=entry.timestamp,
            operation=entry.operation.value,
            status="verified" if verified else "failed",
            entry_hash=entry.entry_hash,
            signature=entry.signature
        )
    
    # =========================================================================
    # CHAIN ENDPOINTS
    # =========================================================================
    
    def verify_chain(self) -> AuditChainStatus:
        """GET /audit/verify - Verify chain integrity"""
        
        is_valid = self.audit.verify()
        latest_entry = self.audit.audit_log.entries[-1] if self.audit.audit_log.entries else None
        
        return AuditChainStatus(
            is_valid=is_valid,
            entry_count=len(self.audit.audit_log.entries),
            latest_hash=latest_entry.entry_hash if latest_entry else "",
            verified_at=datetime.utcnow().isoformat()
        )
    
    def get_chain_status(self) -> Dict[str, Any]:
        """GET /audit/status - Get chain status"""
        
        return {
            "entry_count": len(self.audit.audit_log.entries),
            "is_valid": self.audit.verify(),
            "latest_hash": (
                self.audit.audit_log.entries[-1].entry_hash 
                if self.audit.audit_log.entries else ""
            ),
            "initial_hash": self.audit.audit_log.initial_hash,
            "issued_credentials": len(
                self.audit.get_all_issued_credentials()
            ),
            "revoked_credentials": len(
                self.audit.get_all_revoked_credentials()
            )
        }
    
    def export_log(self) -> str:
        """GET /audit/export - Export audit log"""
        
        return self.audit.audit_log.export_json()
    
    def import_log(self, json_data: str) -> bool:
        """POST /audit/import - Import audit log"""
        
        try:
            data = json.loads(json_data)
            for entry_data in data:
                entry = AuditEntry(
                    entry_id=entry_data.get("entry_id", ""),
                    timestamp=entry_data.get("timestamp", ""),
                    operation=AuditOperation(
                        entry_data.get("operation", "WALLET_CREATE")
                    ),
                    actor=entry_data.get("actor", ""),
                    target=entry_data.get("target", ""),
                    details=entry_data.get("details", {}),
                    previous_hash=entry_data.get("previous_hash", ""),
                    entry_hash=entry_data.get("entry_hash", ""),
                    signature=entry_data.get("signature", "")
                )
                self.audit.audit_log.entries.append(entry)
            return True
        except Exception:
            return False


# =============================================================================
# API ENDPOINTS SUMMARY
# =============================================================================

"""
Audit API Endpoints:

| Method | Path | Description |
|--------|------|-------------|
| POST | /audit/wallets | Create wallet entry |
| DELETE | /audit/wallets/{id} | Delete wallet entry |
| GET | /audit/wallets/{id}/history | Get wallet history |
| POST | /audit/keys | Add key entry |
| DELETE | /audit/keys/{id} | Delete key entry |
| POST | /audit/credentials | Issue credential |
| POST | /audit/credentials/revoke | Revoke credential |
| POST | /audit/credentials/verify | Verify credential |
| GET | /audit/credentials/{id}/history | Credential history |
| POST | /audit/presentations | Create presentation |
| POST | /audit/presentations/verify | Verify presentation |
| POST | /audit/identities | Create identity |
| PUT | /audit/identities/{did} | Update identity |
| DELETE | /audit/identities/{did} | Delete identity |
| GET | /audit/identities/{did}/history | Identity history |
| POST | /audit/sign | Log signing |
| POST | /audit/verify | Log verification |
| GET | /audit/verify | Verify chain |
| GET | /audit/status | Get chain status |
| GET | /audit/export | Export log |
| POST | /audit/import | Import log |
"""


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example():
    """Example usage"""
    
    # Create API
    api = AuditAPI(issuer_did="did:waltid:agennext")
    
    # Create wallet
    resp = api.create_wallet(
        actor="admin",
        wallet_id="wallet123",
        owner="did:waltid:person:456"
    )
    print(f"Wallet: {resp.status}")
    
    # Issue credential
    resp = api.issue_credential(
        actor="issuer",
        credential_id="cred789",
        subject_did="did:waltid:agent:abc",
        credential_type="AgentCredential"
    )
    print(f"Credential: {resp.status}")
    
    # Verify credential
    resp = api.verify_credential(
        actor="verifier",
        credential_id="cred789",
        verified=True
    )
    print(f"Verified: {resp.status}")
    
    # Get chain status
    status = api.get_chain_status()
    print(f"Chain valid: {status.get('is_valid')}")
    print(f"Entries: {status.get('entry_count')}")


if __name__ == "__main__":
    example()