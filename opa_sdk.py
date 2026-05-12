"""
Open Policy Agent (OPA) SDK

Python SDK for OPA policy decisions.

Reference:
- https://www.openpolicyagent.org/
- https://www.openpolicyagent.org/docs/latest/

Features:
- Policy evaluation
- Policy management
- Bundle support
- Status queries
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid
import requests
import json


# =============================================================================
# OPA CONFIG
# =============================================================================

@dataclass
class OPAConfig:
    """OPA server configuration"""
    
    base_url: str = "http://localhost:8181"
    token: str = ""
    
    @property
    def policies_url(self) -> str:
        return f"{self.base_url}/v1/policies"
    
    @property
    def data_url(self) -> str:
        return f"{self.base_url}/v1/data"
    
    @property
    def status_url(self) -> str:
        return f"{self.base_url}/v1/status"


# =============================================================================
# POLICY TYPES
# =============================================================================

class PolicyEffect(Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass
class Policy:
    """OPA policy"""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    module_name: str = ""
    code: str = ""
    
    # Metadata (from base_entity)
    canonical_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class PolicyInput:
    """Policy evaluation input"""
    
    subject: Dict[str, Any] = field(default_factory=dict)
    action: Dict[str, Any] = field(default_factory=dict)
    resource: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "input": {
                "subject": self.subject,
                "action": self.action,
                "resource": self.resource,
                "context": self.context
            }
        }


@dataclass
class PolicyResult:
    """Policy evaluation result"""
    
    decision_id: str
    effect: PolicyEffect
    allowed: bool
    
    # Optional data
    obligations: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    
    @property
    def is_allowed(self) -> bool:
        return self.allowed
    
    @property
    def is_deny(self) -> bool:
        return not self.allowed


# =============================================================================
# OPA CLIENT
# =============================================================================

@dataclass
class OPASDK:
    """OPA Python SDK"""
    
    config: OPAConfig = field(default_factory=OPAConfig)
    
    # =================================================================
    # POLICY MANAGEMENT
    # =================================================================
    
    def list_policies(self) -> List[Dict[str, Any]]:
        """List all policies"""
        response = requests.get(
            self.config.policies_url,
            headers=self._auth_headers()
        )
        if response.status_code == 200:
            return response.json().get("result", [])
        return []
    
    def get_policy(self, policy_id: str) -> Optional[Dict[str, Any]]:
        """Get policy by ID"""
        response = requests.get(
            f"{self.config.policies_url}/{policy_id}",
            headers=self._auth_headers()
        )
        if response.status_code == 200:
            return response.json().get("result")
        return None
    
    def create_policy(
        self,
        module_name: str,
        code: str
    ) -> Optional[str]:
        """Create new policy"""
        response = requests.put(
            f"{self.config.policies_url}/{module_name}",
            data=code,
            headers={
                **self._auth_headers(),
                "Content-Type": "text/plain"
            }
        )
        if response.status_code in [200, 201]:
            return module_name
        return None
    
    def delete_policy(self, policy_id: str) -> bool:
        """Delete policy"""
        response = requests.delete(
            f"{self.config.policies_url}/{policy_id}",
            headers=self._auth_headers()
        )
        return response.status_code in [200, 204]
    
    # =================================================================
    # DATA ENDPOINTS
    # =================================================================
    
    def set_data(
        self,
        path: str,
        data: Dict[str, Any]
    ) -> bool:
        """Set data at path"""
        response = requests.put(
            f"{self.config.data_url}/{path}",
            json=data,
            headers=self._auth_headers()
        )
        return response.status_code in [200, 201]
    
    def get_data(self, path: str) -> Optional[Dict[str, Any]]:
        """Get data at path"""
        response = requests.get(
            f"{self.config.data_url}/{path}",
            headers=self._auth_headers()
        )
        if response.status_code == 200:
            return response.json().get("result")
        return None
    
    def delete_data(self, path: str) -> bool:
        """Delete data at path"""
        response = requests.delete(
            f"{self.config.data_url}/{path}",
            headers=self._auth_headers()
        )
        return response.status_code in [200, 204]
    
    # =================================================================
    # POLICY EVALUATION
    # =================================================================
    
    def evaluate(
        self,
        policy_path: str,
        input_data: Dict[str, Any]
    ) -> PolicyResult:
        """Evaluate policy"""
        
        response = requests.post(
            f"{self.config.data_url}/{policy_path}",
            json=input_data,
            headers=self._auth_headers()
        )
        
        if response.status_code != 200:
            return PolicyResult(
                decision_id=str(uuid.uuid4()),
                effect=PolicyEffect.DENY,
                allowed=False,
                error=response.text
            )
        
        result = response.json()
        result_data = result.get("result", {})
        
        # Extract decision
        effect = result_data.get("effect", "deny")
        allowed = effect == "allow"
        
        return PolicyResult(
            decision_id=str(uuid.uuid4()),
            effect=PolicyEffect.ALLOW if allowed else PolicyEffect.DENY,
            allowed=allowed,
            obligations=result_data.get("obligations", []),
            metrics=result_data.get("metrics", {})
        )
    
    def evaluate_agent(
        self,
        agent_data: Dict[str, Any],
        action: str,
        resource: Dict[str, Any]
    ) -> PolicyResult:
        """Evaluate agent action"""
        
        input_data = {
            "input": {
                "subject": agent_data,
                "action": {"name": action},
                "resource": resource,
                "context": agent_data.get("context", {})
            }
        }
        
        return self.evaluate("agents/allow", input_data)
    
    def evaluate_credential(
        self,
        credential_data: Dict[str, Any],
        operation: str
    ) -> PolicyResult:
        """Evaluate credential operation"""
        
        input_data = {
            "input": {
                "subject": credential_data,
                "action": {"name": operation},
                "resource": {},
                "context": {}
            }
        }
        
        return self.evaluate("credentials/allow", input_data)
    
    def evaluate_identity(
        self,
        identity_data: Dict[str, Any],
        resource: Dict[str, Any]
    ) -> PolicyResult:
        """Evaluate identity access"""
        
        input_data = {
            "input": {
                "subject": identity_data,
                "action": {"name": "access"},
                "resource": resource,
                "context": {}
            }
        }
        
        return self.evaluate("identities/allow", input_data)
    
    # =================================================================
    # STATUS
    # =================================================================
    
    def get_status(self) -> Optional[Dict[str, Any]]:
        """Get OPA status"""
        response = requests.get(
            self.config.status_url,
            headers=self._auth_headers()
        )
        if response.status_code == 200:
            return response.json().get("result")
        return None
    
    # =================================================================
    # BUNDLES
    # =================================================================
    
    def upload_bundle(self, bundle_path: str) -> bool:
        """Upload policy bundle"""
        response = requests.post(
            f"{self.base_url}/v1/bundles",
            headers=self._auth_headers()
        )
        return response.status_code in [200, 201]
    
    def download_bundle(self, bundle_name: str) -> Optional[Dict[str, Any]]:
        """Download policy bundle"""
        response = requests.get(
            f"{self.base_url}/v1/bundles/{bundle_name}",
            headers=self._auth_headers()
        )
        if response.status_code == 200:
            return response.json()
        return None
    
    # =================================================================
    # HELPERS
    # =================================================================
    
    def _auth_headers(self) -> Dict[str, str]:
        """Get auth headers"""
        if self.config.token:
            return {
                "Authorization": f"Bearer {self.config.token}",
                "Content-Type": "application/json"
            }
        return {"Content-Type": "application/json"}


# =============================================================================
# PRE-BUILT POLICIES
# =============================================================================

AGENT_POLICY = '''
package agents

default allow = false

# Allow authenticated agents
allow {
    input.subject.verified == true
    input.action.name == "execute"
    input.resource.allowed == true
}

# Allow skill execution
allow {
    input.subject.type == "SoftwareApplication"
    input.action.name == "execute_skill"
    input.subject.skills[_] == input.action.skill
}

# Deny by default
allow {
    not input.subject.verified
    input.action.name == "execute"
}
'''

CREDENTIAL_POLICY = '''
package credentials

default allow = false

# Allow issue
allow {
    input.action.name == "issue"
    input.subject.type == "Organization"
    input.subject.authorized == true
}

# Allow verify
allow {
    input.action.name == "verify"
    input.subject.status == "active"
}

# Allow revoke
allow {
    input.action.name == "revoke"
    input.subject.role == "admin"
}
'''

IDENTITY_POLICY = '''
package identities

default allow = false

# Allow read
allow {
    input.action.name == "read"
    input.subject.id == input.resource.owner
}

# Allow update
allow {
    input.action.name == "update"
    input.subject.id == input.resource.owner
}

# Allow delete
allow {
    input.action.name == "delete"
    input.subject.role == "admin"
}
'''


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example():
    """Example usage"""
    
    # Create client
    client = OPASDK(config=OPAConfig())
    
    # Note: Requires OPA server running
    # client.create_policy("agents.rego", AGENT_POLICY)
    # client.create_policy("credentials.rego", CREDENTIAL_POLICY)
    # client.create_policy("identities.rego", IDENTITY_POLICY)
    
    # Example evaluation input
    input_data = {
        "input": {
            "subject": {
                "id": "did:waltid:agent:123",
                "type": "SoftwareApplication",
                "verified": True,
                "skills": ["python", "javascript"]
            },
            "action": {
                "name": "execute_skill",
                "skill": "python"
            },
            "resource": {
                "allowed": True
            },
            "context": {}
        }
    }
    
    print("OPA SDK initialized")
    print(f"Agent policy:\n{AGENT_POLICY[:100]}...")


if __name__ == "__main__":
    example()