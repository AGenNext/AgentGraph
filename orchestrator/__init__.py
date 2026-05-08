"""
Enterprise Agent Orchestrator.

Owner & Sponsor are MANDATORY for every agent creation.
"""

from config import get_runtime


# Valid domains for owner/sponsor
VALID_DOMAINS = ["company.com", "corp.com"]


def validate_email(email: str) -> bool:
    """Validate email format."""
    return "@" in email and any(email.endswith(d) for d in VALID_DOMAINS)


def create_agent(
    name: str,
    role: str,
    config: dict = None,
    **options
):
    """
    Create an enterprise agent.
    
    MANDATORY: owner and sponsor must be provided.
    """
    from agents.roles import AgentRole, AgentRoleConfig, ROLE_DEFAULTS
    
    cfg = config or {}
    
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
            "name": name,
            "role": role,
            "owner": owner,
            "sponsor": sponsor,
            "config": agent_config,
            "coordinator": coordinator,
        }
    
    raise ValueError(f"Unknown runtime: {runtime}")
