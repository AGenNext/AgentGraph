from agennext.a2a.runtime import A2ARuntime
from agennext.registry import AgentRegistry, RegistryEntry
from agennext.trust import TrustDecision, TrustProtocol
from agennext.governance import AgentGovernanceProtocol, GovernanceDecision, GovernanceRequest, RiskLevel
from agennext.agentid import AgentIdentity, AgentIdentityProtocol
from agennext.agentdid import AgentDIDProtocol
from agennext.authzen import AuthorizationDecision, AuthorizationRequest, AuthZenProtocol


def test_registry_discovery_by_capability():
    registry = AgentRegistry()
    registry.register(RegistryEntry(agent_id="writer", name="Writer", endpoint="http://writer", capabilities=["write"]))
    assert registry.discover(capability="write")[0].agent_id == "writer"


def test_trust_protocol_decisions():
    trust = TrustProtocol()
    assert trust.evaluate("agent-a") == TrustDecision.REVIEW
    for _ in range(7):
        trust.record_success("agent-a")
    assert trust.evaluate("agent-a") == TrustDecision.ALLOW


def test_governance_requires_review_for_high_risk():
    governance = AgentGovernanceProtocol()
    result = governance.evaluate(GovernanceRequest(actor_id="agent-a", action="deploy", resource="prod", risk=RiskLevel.HIGH))
    assert result.decision == GovernanceDecision.REVIEW


def test_identity_token_and_did():
    identity = AgentIdentity(agent_id="agent-a", name="Agent A")
    token = AgentIdentityProtocol().issue_token(identity)
    assert AgentIdentityProtocol().validate_token(token)
    did = AgentDIDProtocol().create(identity.agent_id)
    assert did.did == "did:agennext:agent-a"


def test_authzen_denies_sensitive_action():
    decision = AuthZenProtocol().authorize(AuthorizationRequest(subject="agent-a", action="delete", resource="prod"))
    assert decision == AuthorizationDecision.DENY


async def test_a2a_runtime_submit_task():
    runtime = A2ARuntime()
    response = await runtime.handle({
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tasks/submit",
        "params": {"message": {"role": "user", "content": "hello"}},
    })
    assert response["result"]["status"] == "completed"
