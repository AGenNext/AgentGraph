"""
Enterprise Agent Orchestrator.

Agent ID = Identity (SSO email, Service Account, or M2M token)
Owner/Sponsor also uses same identity types.
"""

from config import get_runtime


def is_valid_identity(value: str) -> bool:
    """
    Validate identity - can be agent_id, owner, or sponsor.
    
    Valid identities:
    - SSO user: user@company.com
    - Service account: sa-*@project.iam.gserviceaccount.com
    - M2M token: m2m-*
    """
    if not value:
        return False
    
    # Email format
    if "@" in value:
        return value.endswith(("company.com", "corp.com", "iam.gserviceaccount.com"))
    
    # Service account: sa-name (starts with sa-)
    if value.startswith("sa-"):
        return len(value) > 3
    
    # M2M token: m2m-*
    if value.startswith("m2m-"):
        return len(value) > 4
    
    return False


def create_agent(
    agent_id: str,  # Now: must be identity
    name: str,
    role: str,
    config: dict = None,
    **options
):
    """
    Create enterprise agent.
    
    agent_id = identity that represents this agent:
    - user@company.com (SSO)
    - sa-name@project.iam.gserviceaccount.com (service account)
    - m2m-token-id (M2M)
    """
    from agents.roles import AgentRole, AgentRoleConfig, ROLE_DEFAULTS
    
    cfg = config or {}
    
    # agent_id IS the identity
    if not agent_id or not is_valid_identity(agent_id):
        raise ValueError(
            "agent_id REQUIRED - use identity: user@email, sa-name@project, or m2m-token"
        )
    
    # Owner (who owns) - also identity
    owner = cfg.get("owner")
    if not owner or not is_valid_identity(owner):
        raise ValueError("owner REQUIRED: user@email, sa-name@project, or m2m-token")
    
    # Sponsor (budget) - also identity
    sponsor = cfg.get("sponsor")
    if not sponsor or not is_valid_identity(sponsor):
        raise ValueError("sponsor REQUIRED: user@email, sa-name@project, or m2m-token")
    
    role_enum = AgentRole(role)
    defaults = ROLE_DEFAULTS.get(role_enum, {})
    
    agent_config = AgentRoleConfig(
        role=role_enum,
        owner=owner,
        sponsor=sponsor,
        reports_to=cfg.get("reports_to"),
        priority=cfg.get("priority", 1),
        projects=cfg.get("projects", []),
        products=cfg.get("products", []),
        groups=cfg.get("groups", []),
        engages_with=cfg.get("engages_with", []),
        manages=cfg.get("manages", []),
        employee_email=cfg.get("employee_email"),
        it_admin_defaults=cfg.get("it_admin_defaults", {}),
        employee_overrides=cfg.get("employee_overrides", {}),
        orchestrator=cfg.get("orchestrator", defaults.get("orchestrator", "langgraph")),
        llm=cfg.get("llm") or defaults.get("llm"),
    )
    
    runtime = get_runtime()
    
    if runtime == "langgraph":
        from .langgraph_workflow import TeamCoordinator
        coordinator = TeamCoordinator(agents=[name])
        return {
            "agent_id": agent_id,  # This IS the identity
            "name": name,
            "role": role,
            "owner": owner,
            "sponsor": sponsor,
            "config": agent_config,
            "coordinator": coordinator,
        }
    
    raise ValueError(f"Unknown runtime: {runtime}")
