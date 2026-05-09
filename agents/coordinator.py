"""Team Coordinator Agent - orchestrates multi-agent collaboration."""

from typing import Optional
from dataclasses import field
from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from a2a.messages import AgentResult


class TeamCoordinator(BaseAgent):
    """Orchestrates multi-agent team collaboration."""
    
    def __init__(self):
        super().__init__(
            agent_id="team-coordinator",
            name="Team Coordinator",
            description="Orchestrates multi-agent team for content generation",
            capabilities=["coordinate_team", "delegate_tasks", "synthesize_results"],
            skills=["team-coordination", "task-delegation", "result-synthesis"],
        )
        self._team_members = {}
        self._results = []
    
    def _get_port(self) -> int:
        return 8000
    
    def register_team_member(self, agent: BaseAgent) -> None:
        """Register a team member."""
        self._team_members[agent.agent_id] = agent
    
    def _select_agents(self, request: ContentRequest) -> list[BaseAgent]:
        """Select appropriate agents based on content type."""
        selected = []
        
        content_type_mapping = {
            "blog": "openai-creative-writer",
            "storytelling": "openai-creative-writer",
            "creative": "openai-creative-writer",
            "sales": "salesforce-sales-writer",
            "marketing": "salesforce-sales-writer",
            "business": "salesforce-sales-writer", 
            "technical_docs": "microsoft-enterprise-writer",
            "enterprise": "microsoft-enterprise-writer",
            "documentation": "microsoft-enterprise-writer",
            "seo": "google-research-writer",
            "research": "google-research-writer",
            "factual": "google-research-writer",
        }
        
        # Map content type to lead agent
        lead_agent_id = content_type_mapping.get(
            request.content_type, "openai-creative-writer"
        )
        
        # Add lead agent
        if lead_agent_id in self._team_members:
            selected.append(self._team_members[lead_agent_id])
        
        # For multi-agent collaboration, add support agents
        if request.content_type in ["blog", "enterprise"]:
            # Add Google for SEO in blog posts
            if "google-research-writer" in self._team_members:
                selected.append(self._team_members["google-research-writer"])
        
        if request.content_type in ["sales", "marketing"]:
            # Add Microsoft for enterprise copy
            if "microsoft-enterprise-writer" in self._team_members:
                selected.append(self._team_members["microsoft-enterprise-writer"])
        
        # Default: use all available agents for complex requests
        if not selected and self._team_members:
            selected = list(self._team_members.values())
        
        return selected
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        """Coordinate team to generate content."""
        
        # Get available team members
        if not self._team_members:
            self._setup_default_team()
        
        # Select agents
        selected_agents = self._select_agents(request)
        
        if not selected_agents:
            return ContentResult(
                content="No team members available",
                agent_id=self.agent_id,
                quality_score=0.0,
                metadata={"error": "No agents"},
            )
        
        # Generate content in parallel
        results: list[AgentResult] = []
        
        for agent in selected_agents:
            try:
                result = agent._generate_content(request)
                results.append(
                    AgentResult(
                        agent_id=result.agent_id,
                        capability="content_generation",
                        content=result.content,
                        quality_score=result.quality_score,
                        metadata=result.metadata,
                    )
                )
            except Exception as e:
                results.append(
                    AgentResult(
                        agent_id=agent.agent_id,
                        capability="content_generation",
                        content=f"Error: {str(e)}",
                        quality_score=0.0,
                        metadata={"error": str(e)},
                    )
                )
        
        # Synthesize results
        synthesized = self._synthesize_results(results, request)
        
        return ContentResult(
            content=synthesized["content"],
            agent_id=self.agent_id,
            quality_score=synthesized["quality_score"],
            metadata={
                "agents_used": [r.agent_id for r in results],
                "individual_scores": [r.quality_score for r in results],
                "team_collaboration": True,
            },
        )
    
    def _setup_default_team(self) -> None:
        """Setup default team members."""
        from agents.openai_agent import OpenAIAgent
        from agents.salesforce_agent import SalesforceAgent
        from agents.microsoft_agent import MicrosoftAgent
        from agents.google_agent import GoogleAgent
        
        self.register_team_member(OpenAIAgent())
        self.register_team_member(SalesforceAgent())
        self.register_team_member(MicrosoftAgent())
        self.register_team_member(GoogleAgent())
    
    def _synthesize_results(
        self, 
        results: list[AgentResult], 
        request: ContentRequest
    ) -> dict:
        """Synthesize results from multiple agents."""
        
        if len(results) == 1:
            return {
                "content": results[0].content,
                "quality_score": results[0].quality_score,
            }
        
        # Sort by quality score
        sorted_results = sorted(results, key=lambda r: r.quality_score, reverse=True)
        
        # Take the best as base, combine insights
        best = sorted_results[0]
        
        synthesis = {
            "content": best.content,
            "quality_score": best.quality_score * 1.05,  # Team bonus
        }
        
        return synthesis
    
    async def coordinate_delegation(
        self,
        target_agent_id: str,
        capability: str,
        context: dict,
    ) -> AgentResult:
        """Coordinate task delegation to a specific agent."""
        
        if target_agent_id not in self._team_members:
            raise ValueError(f"Agent {target_agent_id} not found")
        
        agent = self._team_members[target_agent_id]
        return await agent.receive_delegated_task(capability, context)
    
    def get_team_status(self) -> dict:
        """Get team status."""
        
        return {
            "coordinator": self.agent_id,
            "team_size": len(self._team_members),
            "members": [
                {
                    "id": agent.agent_id,
                    "name": agent.name,
                    "capabilities": agent.capabilities,
                }
                for agent in self._team_members.values()
            ],
        }
    
    def can_delegate(self, capability: str) -> Optional[str]:
        """Find an agent that can handle a capability."""
        
        for agent in self._team_members.values():
            if agent.can_handle(capability):
                return agent.agent_id
        return None