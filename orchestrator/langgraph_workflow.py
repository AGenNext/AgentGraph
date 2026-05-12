"""LangGraph Team Workflow - orchestrates multi-agent collaboration."""

from typing import TypedDict, Annotated, Sequence
from dataclasses import field

from langgraph.graph import StateGraph, END

from agents.base_agent import ContentRequest, ContentResult
from agents.coordinator import TeamCoordinator


# Team State Definition
class TeamState(TypedDict):
    """State shared across the multi-agent team."""
    
    # Input
    topic: str
    content_type: str
    style: str
    length: str
    
    # Agent outputs
    openai_result: Annotated[ContentResult, "OpenAI result"]
    salesforce_result: Annotated[ContentResult, "Salesforce result"]
    microsoft_result: Annotated[ContentResult, "Microsoft result"]
    google_result: Annotated[ContentResult, "Google result"]
    
    # Aggregated results
    all_results: list[ContentResult]
    selected_agents: list[str]
    
    # Final output
    synthesized_content: str
    quality_score: float
    
    # Metadata
    team_used: bool
    errors: list[str]


def create_workflow(coordinator: TeamCoordinator) -> StateGraph:
    """Create the LangGraph workflow for multi-agent team."""
    
    # Create graph
    graph = StateGraph(TeamState)
    
    # Add nodes
    graph.add_node("route", route_agent)
    graph.add_node("openai", call_openai_agent)
    graph.add_node("salesforce", call_salesforce_agent)
    graph.add_node("microsoft", call_microsoft_agent)
    graph.add_node("google", call_google_agent)
    graph.add_node("aggregate", aggregate_results)
    graph.add_node("synthesize", synthesize_team_results)
    graph.add_node("finalize", finalize_output)
    
    # Add edges
    graph.set_entry_point("route")
    
    # Conditional routing to agents
    graph.add_conditional_edges(
        "route",
        should_call_agent,
        {
            "openai": "openai",
            "salesforce": "salesforce", 
            "microsoft": "microsoft",
            "google": "google",
            "all": "aggregate",
        }
    )
    
    # Parallel agent calls to aggregation
    graph.add_edge("openai", "aggregate")
    graph.add_edge("salesforce", "aggregate")
    graph.add_edge("microsoft", "aggregate")
    graph.add_edge("google", "aggregate")
    
    # Aggregation to synthesis
    graph.add_edge("aggregate", "synthesize")
    
    # Synthesis to finalize
    graph.add_edge("synthesize", "finalize")
    
    # Finalize to end
    graph.add_edge("finalize", END)
    
    return graph.compile()


# Node Functions
def route_agent(state: TeamState) -> TeamState:
    """Route to appropriate agents based on content type."""
    
    content_type = state["content_type"]
    selected = []
    
    # Map content type to agents
    agent_mapping = {
        "blog": ["openai"],
        "storytelling": ["openai"],
        "creative": ["openai"],
        "sales": ["salesforce"],
        "marketing": ["salesforce"],
        "business": ["salesforce"],
        "technical_docs": ["microsoft"],
        "enterprise": ["microsoft"],
        "documentation": ["microsoft"],
        "seo": ["google"],
        "research": ["google"],
        "factual": ["google"],
        # Multi-agent types
        "comprehensive": ["openai", "salesforce", "microsoft", "google"],
        "campaign": ["salesforce", "google"],
    }
    
    selected = agent_mapping.get(content_type, ["openai"])
    state["selected_agents"] = selected
    
    return state


def should_call_agent(state: TeamState) -> str:
    """Determine which agent to call."""
    
    selected = state.get("selected_agents", [])
    
    if not selected or "all" in selected:
        return "all"
    
    return selected[0] if selected else "openai"


def call_openai_agent(state: TeamState) -> TeamState:
    """Call OpenAI agent."""
    from agents.openai_agent import OpenAIAgent
    
    try:
        agent = OpenAIAgent()
        request = ContentRequest(
            topic=state["topic"],
            content_type=state["content_type"],
            style=state["style"],
            length=state["length"],
        )
        result = agent._generate_content(request)
        state["openai_result"] = result
    except Exception as e:
        state.setdefault("errors", []).append(f"OpenAI: {str(e)}")
    
    return state


def call_salesforce_agent(state: TeamState) -> TeamState:
    """Call Salesforce agent."""
    from agents.salesforce_agent import SalesforceAgent
    
    try:
        agent = SalesforceAgent()
        request = ContentRequest(
            topic=state["topic"],
            content_type=state["content_type"],
            style=state["style"],
            length=state["length"],
        )
        result = agent._generate_content(request)
        state["salesforce_result"] = result
    except Exception as e:
        state.setdefault("errors", []).append(f"Salesforce: {str(e)}")
    
    return state


def call_microsoft_agent(state: TeamState) -> TeamState:
    """Call Microsoft agent."""
    from agents.microsoft_agent import MicrosoftAgent
    
    try:
        agent = MicrosoftAgent()
        request = ContentRequest(
            topic=state["topic"],
            content_type=state["content_type"],
            style=state["style"],
            length=state["length"],
        )
        result = agent._generate_content(request)
        state["microsoft_result"] = result
    except Exception as e:
        state.setdefault("errors", []).append(f"Microsoft: {str(e)}")
    
    return state


def call_google_agent(state: TeamState) -> TeamState:
    """Call Google agent."""
    from agents.google_agent import GoogleAgent
    
    try:
        agent = GoogleAgent()
        request = ContentRequest(
            topic=state["topic"],
            content_type=state["content_type"],
            style=state["style"],
            length=state["length"],
        )
        result = agent._generate_content(request)
        state["google_result"] = result
    except Exception as e:
        state.setdefault("errors", []).append(f"Google: {str(e)}")
    
    return state


def aggregate_results(state: TeamState) -> TeamState:
    """Aggregate results from all agents."""
    
    results = []
    
    if "openai_result" in state and state["openai_result"]:
        results.append(state["openai_result"])
    if "salesforce_result" in state and state["salesforce_result"]:
        results.append(state["salesforce_result"])
    if "microsoft_result" in state and state["microsoft_result"]:
        results.append(state["microsoft_result"])
    if "google_result" in state and state["google_result"]:
        results.append(state["google_result"])
    
    state["all_results"] = results
    state["team_used"] = len(results) > 1
    
    return state


def synthesize_team_results(state: TeamState) -> TeamState:
    """Synthesize results from multiple agents."""
    
    results = state.get("all_results", [])
    
    if not results:
        state["synthesized_content"] = "No content generated"
        state["quality_score"] = 0.0
        return state
    
    # Sort by quality score
    sorted_results = sorted(results, key=lambda r: r.quality_score, reverse=True)
    
    # Use best result
    best = sorted_results[0]
    
    # If multiple agents used, synthesize
    if len(results) > 1:
        # Add team header
        team_notes = f"\n\n---\n*Content generated by multi-agent team ({len(results)} agents)*\n"
        
        # Add scores from all agents
        scores_note = f"*Quality scores: " + ", ".join(
            f"{r.agent_id.split('-')[0]}: {r.quality_score:.2f}" 
            for r in sorted_results
        ) + "*"
        
        state["synthesized_content"] = best.content + team_notes + scores_note
    else:
        state["synthesized_content"] = best.content
    
    # Calculate average quality with team bonus
    avg_score = sum(r.quality_score for r in results) / len(results)
    state["quality_score"] = min(avg_score * 1.1, 1.0)  # 10% team bonus
    
    return state


def finalize_output(state: TeamState) -> TeamState:
    """Finalize output."""
    
    # Ensure we have content
    if not state.get("synthesized_content"):
        state["synthesized_content"] = "Content generation failed"
    
    if not state.get("quality_score"):
        state["quality_score"] = 0.0
    
    return state


# Convenience function
def run_team_workflow(
    topic: str,
    content_type: str = "blog",
    style: str = "professional",
    length: str = "medium",
) -> dict:
    """Run the team workflow."""
    
    initial_state = TeamState(
        topic=topic,
        content_type=content_type,
        style=style,
        length=length,
        openai_result=None,
        salesforce_result=None,
        microsoft_result=None,
        google_result=None,
        all_results=[],
        selected_agents=[],
        synthesized_content="",
        quality_score=0.0,
        team_used=False,
        errors=[],
    )
    
    graph = create_workflow(None)
    result = graph.invoke(initial_state)
    
    return {
        "content": result["synthesized_content"],
        "quality_score": result["quality_score"],
        "team_used": result["team_used"],
        "errors": result.get("errors", []),
    }