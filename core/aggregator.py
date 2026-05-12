"""Response aggregator for multi-agent results."""

from typing import List
from dataclasses import dataclass, field

from agents.base_agent import ContentResult


@dataclass
class AggregatedResponse:
    """Aggregated response from multiple agents."""
    
    results: list[ContentResult] = field(default_factory=list)
    agent_responses: dict[str, str] = field(default_factory=dict)
    primary_result: ContentResult = None
    
    def add_result(self, agent_id: str, result: ContentResult) -> None:
        """Add a result from an agent."""
        self.results.append(result)
        self.agent_responses[agent_id] = result.content


class ResponseAggregator:
    """Aggregates responses from multiple agents."""
    
    def __init__(self):
        self.responses: dict[str, AggregatedResponse] = {}
    
    def create_session(self, session_id: str) -> AggregatedResponse:
        """Create a new aggregation session."""
        session = AggregatedResponse()
        self.responses[session_id] = session
        return session
    
    def add_agent_result(
        self,
        session_id: str,
        agent_id: str,
        result: ContentResult,
    ) -> AggregatedResponse:
        """Add a result to the session."""
        session = self.responses.get(session_id)
        if not session:
            session = self.create_session(session_id)
        
        session.add_result(agent_id, result)
        
        # Update primary if this is the best result
        if not session.primary_result or result.quality_score > session.primary_result.quality_score:
            session.primary_result = result
        
        return session
    
    def get_aggregated_content(self, session_id: str) -> str:
        """Get the aggregated content for a session."""
        session = self.responses.get(session_id)
        if not session or not session.primary_result:
            return ""
        
        return session.primary_result.content
    
    def get_all_responses(self, session_id: str) -> dict[str, str]:
        """Get all agent responses for a session."""
        session = self.responses.get(session_id)
        return session.agent_responses if session else {}
    
    def get_best_agent(self, session_id: str) -> str:
        """Get the best performing agent for a session."""
        session = self.responses.get(session_id)
        if not session or not session.primary_result:
            return ""
        
        return session.primary_result.agent_id