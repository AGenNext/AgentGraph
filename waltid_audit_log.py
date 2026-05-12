"""
WaltID Immutable Audit Log

Immutable audit log for all WaltID credential operations.

Reference:
- https://github.com/walt-id/waltid-identity

Features:
- All operations are logged immutably
- Cryptographic hashing for integrity
- Chain-based linking (blockchain-style)
- Tamper detection
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid
import hashlib
import json
import secrets


# =============================================================================
# AUDIT OPERATIONS
# =============================================================================

class AuditOperation(Enum):
    """All audit operations"""
    WALLET_CREATE = "WALLET_CREATE"
    WALLET_DELETE = "WALLET_DELETE"
    KEY_ADD = "KEY_ADD"
    KEY_DELETE = "KEY_DELETE"
    CREDENTIAL_ISSUE = "CREDENTIAL_ISSUE"
    CREDENTIAL_REVOKE = "CREDENTIAL_REVOKE"
    CREDENTIAL_VERIFY = "CREDENTIAL_VERIFY"
    PRESENTATION_CREATE = "PRESENTATION_CREATE"
    PRESENTATION_VERIFY = "PRESENTATION_VERIFY"
    IDENTITY_CREATE = "IDENTITY_CREATE"
    IDENTITY_UPDATE = "IDENTITY_UPDATE"
    IDENTITY_DELETE = "IDENTITY_DELETE"
    SIGN = "SIGN"
    VERIFY = "VERIFY"
    OFFER_CREATE = "OFFER_CREATE"
    POLICY_CREATE = "POLICY_CREATE"
    POLICY_UPDATE = "POLICY_UPDATE"


@dataclass
class AuditEntry:
    """Immutable audit log entry"""
    
    # Unique ID
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Timestamp
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    
    # Operation
    operation: AuditOperation = AuditOperation.WALLET_CREATE
    
    # Actor (DID or API key)
    actor: str = ""
    
    # Target (DID, credential ID, etc.)
    target: str = ""
    
    # Details
    details: Dict[str, Any] = field(default_factory=dict)
    
    # Previous entry hash (chain)
    previous_hash: str = ""
    
    # This entry hash
    entry_hash: str = ""
    
    # Signature
    signature: str = ""
    
    def compute_hash(self) -> str:
        """Compute hash of this entry"""
        data = {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp,
            "operation": self.operation.value,
            "actor": self.actor,
            "target": self.target,
            "details": self.details,
            "previous_hash": self.previous_hash
        }
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()
    
    def sign(self, private_key: str = "") -> str:
        """Sign the entry"""
        self.entry_hash = self.compute_hash()
        self.signature = hashlib.sha256(
            f"{self.entry_hash}{private_key}".encode()
        ).hexdigest()
        return self.signature
    
    def verify(self) -> bool:
        """Verify entry integrity"""
        expected_hash = self.compute_hash()
        return self.entry_hash == expected_hash
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict"""
        return {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp,
            "operation": self.operation.value,
            "actor": self.actor,
            "target": self.target,
            "details": self.details,
            "previous_hash": self.previous_hash,
            "entry_hash": self.entry_hash,
            "signature": self.signature
        }


@dataclass
class AuditLog:
    """Immutable audit log chain"""
    
    entries: List[AuditEntry] = field(default_factory=list)
    initial_hash: str = field(default_factory=lambda: secrets.token_hex(32))
    
    def get_latest_hash(self) -> str:
        """Get hash of latest entry"""
        if not self.entries:
            return self.initial_hash
        return self.entries[-1].entry_hash
    
    def add_entry(
        self,
        operation: AuditOperation,
        actor: str,
        target: str,
        details: Dict[str, Any] = None,
        private_key: str = ""
    ) -> AuditEntry:
        """Add new audit entry"""
        
        entry = AuditEntry(
            operation=operation,
            actor=actor,
            target=target,
            details=details or {},
            previous_hash=self.get_latest_hash()
        )
        
        # Sign entry
        entry.sign(private_key)
        
        # Add to chain
        self.entries.append(entry)
        
        return entry
    
    def verify_chain(self) -> bool:
        """Verify entire chain integrity"""
        expected_prev = self.initial_hash
        
        for entry in self.entries:
            # Check previous hash
            if entry.previous_hash != expected_prev:
                return False
            
            # Verify entry
            if not entry.verify():
                return False
            
            expected_prev = entry.entry_hash
        
        return True
    
    def get_entries_by_actor(self, actor: str) -> List[AuditEntry]:
        """Get all entries by actor"""
        return [e for e in self.entries if e.actor == actor]
    
    def get_entries_by_target(self, target: str) -> List[AuditEntry]:
        """Get all entries for target"""
        return [e for e in self.entries if e.target == target]
    
    def get_entries_by_operation(
        self,
        operation: AuditOperation
    ) -> List[AuditEntry]:
        """Get entries by operation type"""
        return [e for e in self.entries if e.operation == operation]
    
    def export_json(self) -> str:
        """Export to JSON"""
        return json.dumps(
            [e.to_dict() for e in self.entries],
            indent=2
        )


# =============================================================================
# WALLET AUDIT LOG
# =============================================================================

@dataclass
class WaltIDAuditLog:
    """WaltID-specific audit log"""
    
    # Main audit log
    audit_log: AuditLog = field(default_factory=AuditLog)
    
    # Issuer DID
    issuer_did: str = ""
    
    # =================================================================
    # WALLET OPERATIONS
    # =================================================================
    
    def log_wallet_create(
        self,
        actor: str,
        wallet_id: str,
        owner: str
    ) -> AuditEntry:
        """Log wallet creation"""
        return self.audit_log.add_entry(
            operation=AuditOperation.WALLET_CREATE,
            actor=actor,
            target=wallet_id,
            details={"owner": owner}
        )
    
    def log_wallet_delete(
        self,
        actor: str,
        wallet_id: str
    ) -> AuditEntry:
        """Log wallet deletion"""
        return self.audit_log.add_entry(
            operation=AuditOperation.WALLET_DELETE,
            actor=actor,
            target=wallet_id
        )
    
    # =================================================================
    # KEY OPERATIONS
    # =================================================================
    
    def log_key_add(
        self,
        actor: str,
        wallet_id: str,
        key_id: str,
        key_type: str
    ) -> AuditEntry:
        """Log key addition"""
        return self.audit_log.add_entry(
            operation=AuditOperation.KEY_ADD,
            actor=actor,
            target=key_id,
            details={"wallet": wallet_id, "key_type": key_type}
        )
    
    def log_key_delete(
        self,
        actor: str,
        key_id: str
    ) -> AuditEntry:
        """Log key deletion"""
        return self.audit_log.add_entry(
            operation=AuditOperation.KEY_DELETE,
            actor=actor,
            target=key_id
        )
    
    # =================================================================
    # CREDENTIAL OPERATIONS
    # =================================================================
    
    def log_credential_issue(
        self,
        actor: str,
        credential_id: str,
        subject_did: str,
        credential_type: str
    ) -> AuditEntry:
        """Log credential issuance"""
        return self.audit_log.add_entry(
            operation=AuditOperation.CREDENTIAL_ISSUE,
            actor=actor,
            target=credential_id,
            details={
                "subject_did": subject_did,
                "credential_type": credential_type,
                "issuer_did": self.issuer_did
            }
        )
    
    def log_credential_revoke(
        self,
        actor: str,
        credential_id: str
    ) -> AuditEntry:
        """Log credential revocation"""
        return self.audit_log.add_entry(
            operation=AuditOperation.CREDENTIAL_REVOKE,
            actor=actor,
            target=credential_id
        )
    
    def log_credential_verify(
        self,
        actor: str,
        credential_id: str,
        verified: bool
    ) -> AuditEntry:
        """Log credential verification"""
        return self.audit_log.add_entry(
            operation=AuditOperation.CREDENTIAL_VERIFY,
            actor=actor,
            target=credential_id,
            details={"verified": verified}
        )
    
    # =================================================================
    # PRESENTATION OPERATIONS
    # =================================================================
    
    def log_presentation_create(
        self,
        actor: str,
        presentation_id: str,
        credentials: List[str]
    ) -> AuditEntry:
        """Log presentation creation"""
        return self.audit_log.add_entry(
            operation=AuditOperation.PRESENTATION_CREATE,
            actor=actor,
            target=presentation_id,
            details={"credentials": credentials}
        )
    
    def log_presentation_verify(
        self,
        actor: str,
        presentation_id: str,
        verified: bool
    ) -> AuditEntry:
        """Log presentation verification"""
        return self.audit_log.add_entry(
            operation=AuditOperation.PRESENTATION_VERIFY,
            actor=actor,
            target=presentation_id,
            details={"verified": verified}
        )
    
    # =================================================================
    # IDENTITY OPERATIONS
    # =================================================================
    
    def log_identity_create(
        self,
        actor: str,
        did: str,
        method: str
    ) -> AuditEntry:
        """Log identity creation"""
        return self.audit_log.add_entry(
            operation=AuditOperation.IDENTITY_CREATE,
            actor=actor,
            target=did,
            details={"method": method}
        )
    
    def log_identity_update(
        self,
        actor: str,
        did: str
    ) -> AuditEntry:
        """Log identity update"""
        return self.audit_log.add_entry(
            operation=AuditOperation.IDENTITY_UPDATE,
            actor=actor,
            target=did
        )
    
    def log_identity_delete(
        self,
        actor: str,
        did: str
    ) -> AuditEntry:
        """Log identity deletion"""
        return self.audit_log.add_entry(
            operation=AuditOperation.IDENTITY_DELETE,
            actor=actor,
            target=did
        )
    
    # =================================================================
    # SIGNING OPERATIONS
    # =================================================================
    
    def log_sign(
        self,
        actor: str,
        did: str,
        data_hash: str
    ) -> AuditEntry:
        """Log signing operation"""
        return self.audit_log.add_entry(
            operation=AuditOperation.SIGN,
            actor=actor,
            target=did,
            details={"data_hash": data_hash}
        )
    
    def log_verify(
        self,
        actor: str,
        did: str,
        signature: str,
        verified: bool
    ) -> AuditEntry:
        """Log verification operation"""
        return self.audit_log.add_entry(
            operation=AuditOperation.VERIFY,
            actor=actor,
            target=did,
            details={"signature": signature, "verified": verified}
        )
    
    # =================================================================
    # QUERY METHODS
    # =================================================================
    
    def get_credential_history(
        self,
        credential_id: str
    ) -> List[AuditEntry]:
        """Get full history for a credential"""
        return self.audit_log.get_entries_by_target(credential_id)
    
    def get_identity_history(
        self,
        did: str
    ) -> List[AuditEntry]:
        """Get full history for an identity"""
        return self.audit_log.get_entries_by_target(did)
    
    def get_wallet_history(
        self,
        wallet_id: str
    ) -> List[AuditEntry]:
        """Get full history for a wallet"""
        return self.audit_log.get_entries_by_target(wallet_id)
    
    def get_all_issued_credentials(
        self
    ) -> List[AuditEntry]:
        """Get all issued credentials"""
        return self.audit_log.get_entries_by_operation(
            AuditOperation.CREDENTIAL_ISSUE
        )
    
    def get_all_revoked_credentials(
        self
    ) -> List[AuditEntry]:
        """Get all revoked credentials"""
        return self.audit_log.get_entries_by_operation(
            AuditOperation.CREDENTIAL_REVOKE
        )
    
    def verify(self) -> bool:
        """Verify audit log integrity"""
        return self.audit_log.verify_chain()


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example():
    """Example usage"""
    
    # Create audit log
    audit = WaltIDAuditLog(issuer_did="did:waltid:agennext")
    
    # Log operations
    audit.log_wallet_create(
        actor="admin",
        wallet_id="wallet123",
        owner="did:waltid:person:456"
    )
    
    audit.log_credential_issue(
        actor="issuer",
        credential_id="cred789",
        subject_did="did:waltid:agent:abc",
        credential_type="AgentCredential"
    )
    
    audit.log_credential_verify(
        actor="verifier",
        credential_id="cred789",
        verified=True
    )
    
    # Verify chain
    print(f"Chain valid: {audit.verify()}")
    
    # Get credential history
    history = audit.get_credential_history("cred789")
    print(f"Credential history: {len(history)} entries")
    
    # Export
    print(audit.audit_log.export_json())


if __name__ == "__main__":
    example()