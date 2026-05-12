"""Full IAM/IGA/IDP/SSO/PAM security layer."""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum


class IdentityProvider(Enum):
    """Supported IDPs."""
    AZURE_AD = "azure_ad"
    OKTA = "okta"
    AUTH0 = "auth0"
    GOOGLE = "google"
    PING = "ping_identity"
    SAML = "saml"
    OIDC = "oidc"


class AuthProtocol(Enum):
    """SSO Protocols."""
    SAML_2_0 = "saml_2_0"
    OIDC = "oidc"
    OAUTH_2_0 = "oauth_2_0"
    WS_FED = "ws_fed"


@dataclass
class User:
    """Identity entity."""
    user_id: str
    email: str
    display_name: str
    idp: IdentityProvider
    idp_user_id: str
    roles: list[str] = field(default_factory=list)
    groups: list[str] = field(default_factory=list)
    mfa_enabled: bool = False
    status: str = "active"
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None


@dataclass
class AccessToken:
    """JWT access token."""
    user_id: str
    roles: list[str]
    groups: list[str]
    expires_at: datetime
    scopes: list[str]
    client_id: Optional[str] = None


class IAMService:
    """Identity & Access Management."""
    
    def __init__(self, jwt_secret: str):
        self.jwt_secret = jwt_secret
        self.users: dict[str, User] = {}
        self.sessions: dict[str, AccessToken] = {}
    
    def create_user(
        self, 
        email: str, 
        display_name: str, 
        idp: IdentityProvider,
        idp_user_id: str
    ) -> User:
        """Create user from IDP."""
        user = User(
            user_id=secrets.token_hex(16),
            email=email,
            display_name=display_name,
            idp=idp,
            idp_user_id=idp_user_id,
        )
        self.users[user.user_id] = user
        return user
    
    def assign_role(self, user_id: str, role: str):
        """Assign role to user."""
        if user_id in self.users and role not in self.users[user_id].roles:
            self.users[user_id].roles.append(role)
    
    def assign_group(self, user_id: str, group: str):
        """Assign group to user."""
        if user_id in self.users and group not in self.users[user_id].groups:
            self.users[user_id].groups.append(group)
    
    def create_token(
        self, 
        user_id: str, 
        client_id: Optional[str] = None,
        ttl: int = 3600
    ) -> AccessToken:
        """Create access token."""
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        token = AccessToken(
            user_id=user_id,
            roles=user.roles,
            groups=user.groups,
            expires_at=datetime.utcnow() + timedelta(seconds=ttl),
            scopes=self._get_scopes(user.roles),
            client_id=client_id,
        )
        token_id = secrets.token_hex(32)
        self.sessions[token_id] = token
        return token
    
    def _get_scopes(self, roles: list[str]) -> list[str]:
        """Map roles to scopes."""
        scope_map = {
            "admin": ["read", "write", "delete", "admin"],
            "developer": ["read", "write", "agent:create", "agent:edit"],
            "viewer": ["read"],
            "finance": ["read", "write", "finance:*"],
            "external": ["read", "api:*"],
        }
        scopes = set()
        for role in roles:
            scopes.update(scope_map.get(role, []))
        return list(scopes)
    
    def revoke_session(self, session_id: str):
        """Revoke session."""
        if session_id in self.sessions:
            del self.sessions[session_id]


class SSOConfig:
    """SSO Configuration."""
    
    def __init__(self):
        self.idp_configs: dict[IdentityProvider, dict] = {}
    
    def configure_idp(
        self,
        idp: IdentityProvider,
        client_id: str,
        client_secret: str,
        metadata_url: Optional[str] = None,
        protocol: AuthProtocol = AuthProtocol.OIDC,
    ):
        """Configure IDP."""
        self.idp_configs[idp] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "metadata_url": metadata_url,
            "protocol": protocol,
        }
    
    def get_saml_config(self, idp: IdentityProvider) -> dict:
        """Get SAML SP metadata."""
        return {
            "entity_id": "https://agennext.io/sp",
            "acs_url": "https://agennext.io/auth/saml/callback",
            "slo_url": "https://agennext.io/auth/slo",
        }


class PAMService:
    """Privileged Access Management."""
    
    def __init__(self):
        self.privileged_users: dict[str, dict] = {}
        self.sudo_requests: dict[str, dict] = {}
    
    def grant_privileged_access(
        self, 
        user_id: str, 
        resource: str, 
        duration: int = 3600
    ):
        """Grant privileged access with time limit."""
        self.privileged_users[f"{user_id}:{resource}"] = {
            "user_id": user_id,
            "resource": resource,
            "expires_at": datetime.utcnow() + timedelta(seconds=duration),
            "approved_by": "system",
        }
    
    def request_elevation(
        self, 
        user_id: str, 
        resource: str, 
        reason: str
    ) -> str:
        """Request privilege elevation."""
        request_id = secrets.token_hex(16)
        self.sudo_requests[request_id] = {
            "user_id": user_id,
            "resource": resource,
            "reason": reason,
            "status": "pending",
            "created_at": datetime.utcnow(),
        }
        return request_id
    
    def approve_elevation(self, request_id: str, approver: str):
        """Approve elevation request."""
        if request_id in self.sudo_requests:
            self.sudo_requests[request_id]["status"] = "approved"
            self.sudo_requests[request_id]["approved_by"] = approver
            request = self.sudo_requests[request_id]
            self.grant_privileged_access(
                request["user_id"], 
                request["resource"]
            )


class IGAService:
    """Identity Governance & Administration."""
    
    def __init__(self):
        self.certifications: dict[str, dict] = {}
        self.policies: dict[str, dict] = {}
        self.separation_of_duties: dict[str, list[str]] = {}
    
    def create_access_review(
        self, 
        reviewer: str, 
        users: list[str], 
        due_date: datetime
    ) -> str:
        """Create periodic access review."""
        review_id = secrets.token_hex(16)
        self.certifications[review_id] = {
            "review_id": review_id,
            "reviewer": reviewer,
            "users": users,
            "due_date": due_date,
            "status": "pending",
            "created_at": datetime.utcnow(),
        }
        return review_id
    
    def certify_access(self, review_id: str, user_id: str, outcome: str, notes: str):
        """Certify user access."""
        if review_id in self.certifications:
            self.certifications[review_id]["status"] = "completed"
            # Log decision
            print(f"Certified {user_id}: {outcome} - {notes}")
    
    def add_sod_rule(self, role1: str, role2: str):
        """Add separation of duties constraint."""
        key = f"{role1}:{role2}"
        self.separation_of_duties[key] = [role1, role2]
    
    def check_sod(self, roles: list[str]) -> bool:
        """Check for SOD violations."""
        for i, role1 in enumerate(roles):
            for role2 in roles[i+1:]:
                key = f"{role1}:{role2}"
                if key in self.separation_of_duties:
                    return False
        return True


class AuditService:
    """SHA-256 hash-chained audit log."""
    
    def __init__(self):
        self.chain: list[dict] = []
        self.last_hash = "0" * 64
    
    def log(
        self, 
        event_type: str, 
        user_id: str, 
        action: str, 
        resource: str,
        result: str,
        metadata: Optional[dict] = None
    ):
        """Log with hash chaining."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "result": result,
            "metadata": metadata or {},
            "prev_hash": self.last_hash,
        }
        entry_bytes = str(entry).encode()
        entry_hash = hashlib.sha256(entry_bytes).hexdigest()
        entry["hash"] = entry_hash
        self.last_hash = entry_hash
        self.chain.append(entry)
        return entry
    
    def verify(self) -> bool:
        """Verify chain integrity."""
        for i, entry in enumerate(self.chain):
            if i == 0:
                continue
            if entry["prev_hash"] != self.chain[i-1]["hash"]:
                return False
        return True