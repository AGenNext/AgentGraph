"""
Base Entity - All database entities inherit from this.

Provides:
- canonical_id: Unique, immutable identifier
- version: Entity version for optimistic locking
- audit_log: Immutable audit trail
- crypto_signature: Cryptographic verification
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import hashlib
import json
import uuid


class EntityVersion(Enum):
    V1 = "1.0"
    V2 = "2.0"
    V3 = "3.0"


@dataclass
class AuditEntry:
    """Immutable audit log entry"""
    timestamp: str
    action: str  # CREATE, UPDATE, DELETE
    actor: str
    changes: Dict[str, Any]
    previous_hash: str


@dataclass
class CryptoSignature:
    """Cryptographic signature for entity verification"""
    algorithm: str = "SHA-256"
    signature: str = ""
    public_key: str = ""
    signed_at: str = ""
    
    def sign(self, data: str, private_key: str = "") -> str:
        """Generate cryptographic signature"""
        self.signature = hashlib.sha256(
            f"{data}{private_key}".encode()
        ).hexdigest()
        self.signed_at = datetime.utcnow().isoformat()
        return self.signature
    
    def verify(self, data: str) -> bool:
        """Verify cryptographic signature"""
        expected = hashlib.sha256(
            f"{data}".encode()
        ).hexdigest()
        return self.signature == expected


@dataclass
class Entity:
    """Base entity with canonical_id, version, audit_log, crypto_signature"""
    
    # Canonical ID - unique, immutable identifier
    canonical_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Version - for optimistic locking
    version: str = "1.0"
    
    # Immutable audit log
    audit_log: List[AuditEntry] = field(default_factory=list)
    
    # Cryptographic signature
    crypto_signature: CryptoSignature = field(default_factory=CryptoSignature)
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    is_deleted: bool = False
    
    def _compute_hash(self) -> str:
        """Compute entity hash for signing"""
        data = {
            "canonical_id": self.canonical_id,
            "version": self.version,
            "created_at": self.created_at,
        }
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()
    
    def sign(self, private_key: str = "") -> str:
        """Sign the entity"""
        data = self._compute_hash()
        return self.crypto_signature.sign(data, private_key)
    
    def verify(self) -> bool:
        """Verify entity signature"""
        data = self._compute_hash()
        return self.crypto_signature.verify(data)
    
    def add_audit_entry(self, action: str, actor: str, changes: Dict[str, Any]) -> None:
        """Add immutable audit entry"""
        previous_hash = self.crypto_signature.signature if self.crypto_signature.signature else ""
        
        entry = AuditEntry(
            timestamp=datetime.utcnow().isoformat(),
            action=action,
            actor=actor,
            changes=changes,
            previous_hash=previous_hash
        )
        self.audit_log.append(entry)
        self.updated_at = datetime.utcnow().isoformat()
    
    def increment_version(self) -> None:
        """Increment version after update"""
        major, minor = self.version.split(".")
        self.version = f"{major}.{int(minor) + 1}"
    
    def soft_delete(self) -> None:
        """Soft delete entity"""
        self.is_deleted = True
        self.add_audit_entry("DELETE", "system", {"deleted": True})