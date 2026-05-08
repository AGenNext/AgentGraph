"""
Enterprise Agent Orchestrator.

Agent ID, Owner & Sponsor are MANDATORY for every agent.
"""

from config import get_runtime

VALID_DOMAINS = ["company.com", "corp.com"]


def validate_email(email: str) -> bool:
    """Validate email format."""
    return "@" in email and any(email.endswith(d) for d in VALID_DOMAINS)


def validate_agent_id(agent_id: str) -> bool:
    """Validate agent ID format."""
    # AgentID Format: role-purpose-dept (e.g., assistant-sales-eastus)
    return len(agent_id) >= 5 and "-" in agent_id


def create_agent(
    agent_id: str,  # MANDATORY - now required
    name: str,
    role: str,
    config: dict = None,
    **options
):
    """
    Create an enterprise agent.
    
    MANDATORY: agent_id, owner, sponsor must be provided by IT admin.
    """
    from agents.roles import AgentRole, AgentRoleConfig, ROLE_DEFAULTS
    
    cfg = config or {}
    
    # MANDATORY: agent_id
    if not agent_id:
        raise ValueError("agent_id is REQUIRED - IT admin must assign agent ID")
    if not validate_agent_id(agent_id):
        raise ValueError("agent_id must be role-purpose-dept format (e.g., assistant-sales-eastus)")
    
    # MANDATORY: owner and sponsor
    owner = cfg.get("owner")
    sponsor = cfg.get("sponsor")
    
    if not owner:
        raise ValueError("owner is REQUIRED - IT admin must assign agent owner")
    if not sponsor:
        raise ValueError("sponsor is REQUIRED - IT admin must assign budget/sponsor")
    
    if not validate_email(owner):
        raise ValueError(f"owner must be valid email (@{VALID_DOMAINS})")
    if not validate_email(sponsor):
        raise ValueError(f"sponsor must be valid email (@{VALID_DOMAINS})")
    
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
            "agent_id": agent_id,  # Now in response
            "name": name,
            "role": role,
            "owner": owner,
            "sponsor": sponsor,
            "config": agent_config,
            "coordinator": coordinator,
        }
    
    raise ValueError(f"Unknown runtime: {runtime}")
