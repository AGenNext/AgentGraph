"""CrewAI Agent SDK - Multi-agent AI crew framework."""

from typing import Optional, List, Callable, Any
import os

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig


class ToolCallHooks:
    """Pre/post tool call hooks."""
    def __init__(self):
        self.pre = []
        self.post = []
    def on_before_tool(self, h): self.pre.append(h)
    def on_after_tool(self, h): self.post.append(h)


class CrewAIAgent(BaseAgent):
    """CrewAI specialist.
    
    Capabilities:
    - Crew definitions
    - Agent definitions with roles
    - Task definitions
    - Process configs (sequential, hierarchical)
    - Custom tools
    - Memory/metrics
    
    Tools: search, scrapping, code, file_read, csv_writer
    Skills: multi-agent, crew-orchestration, role-playing, task-delegation
    """
    
    def __init__(self, api_key: Optional[str] = None, enable_hooks: bool = False):
        super().__init__(
            agent_id="crewai-writer",
            name="CrewAI Writer",
            description="CrewAI - crew orchestration, roles, tasks",
            capabilities=[
                "crew_definition",
                "agent_definition",
                "task_definition",
                "process_config",
                "tool_integration",
                "memory_config",
            ],
            skills=["multi-agent", "crew-orchestration", "role-playing", "task-delegation"],
            api_key=api_key or os.getenv("LLM_API_KEY"),
        )
        
        self.llm_config = LLMConfig.from_env()
        self._llm = None
        
        # Tool call hooks
        self._hooks = ToolCallHooks() if enable_hooks else None
    
    @property
    def pre_tool_call_hook(self):
        return self._hooks.on_before_tool if self._hooks else None
    
    @property
    def post_tool_call_hook(self):
        return self._hooks.on_after_tool if self._hooks else None
    
    def _get_port(self) -> int:
        return 8015
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        if "crew" in ct:
            return self._crew_definition(request)
        elif "agent" in ct:
            return self._agent_definition(request)
        elif "task" in ct:
            return self._task_definition(request)
        elif "process" in ct:
            return self._process_config(request)
        else:
            return self._crew_definition(request)
    
    def _crew_definition(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""CrewAI Crew: {request.topic}"""

from crewai import Crew, Agent, Task, Process

# Define agents
researcher = Agent(
    role="Researcher",
    goal="Research {{topic}} thoroughly",
    backstory="Expert researcher for {{topic}}",
    llm=llm,
)

writer = Agent(
    role="Content Writer",
    goal="Write compelling content about {{topic}}",
    backstory="Professional writer",
    llm=llm,
)

# Define tasks
research_task = Task(
    description="Research {{topic}}",
    agent=researcher,
)

write_task = Task(
    description="Write article about {{topic}}",
    agent=writer,
    expected_output="Full article",
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True,
)

# Execute
result = crew.kickoff(inputs={{"topic": "{request.topic}"}})
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "crew", "skill": "crew-orchestration"},
        )
    
    def _agent_definition(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""CrewAI Agent: {request.topic}"""

from crewai import Agent
from crewai.tools import SerperDevTool, BrowserwiseTool

# Define agent with role
agent = Agent(
    role="{request.topic} Expert",
    goal=f"Be the best {{topic}} expert",
    backstory=f"""You are a renowned {request.topic} specialist.
You have decades of experience.""",
    llm=llm,
    
    # Tools
    tools=[SerperDevTool(), BrowserwiseTool()],
    
    # Memory
    memory=True,
    verbose=True,
)

# Use with function calling
# agent.invoke({{"topic": "AI"}})
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "agent", "skill": "role-playing"},
        )
    
    def _task_definition(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""CrewAI Task: {request.topic}"""

from crewai import Task

# Create task
task = Task(
    description=f"Research {{topic}}: {request.topic}",
    agent=agent,
    
    # Output
    expected_output="Comprehensive research report",
    output_file="report.md",
    
    # Async
    async_execution=False,
)

# With context
task_with_context = Task(
    description="Analyze {{topic}} data",
    agent=analyst_agent,
    context=[research_task],  # Depends on context
)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "task", "skill": "task-definition"},
        )
    
    def _process_config(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""CrewAI Process: {request.topic}"""

from crewai import Crew, Process

# Sequential (one after another)
sequential_crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.sequential,
)

# Hierarchical (manager assigns)
hierarchical_crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.hierarchical,
    manager_agent=manager,  # Specify manager
    steps=[step1, step2],  # Define steps
)

# With memory
crew_with_memory = Crew(
    agents=agents,
    tasks=tasks,
    memory=True,
    short_term_memory=True,
    long_term_memory=True,
    entity_memory=True,
    # Use external storage
)

# With metrics
crew_with_metrics = Crew(
    agents=agents,
    tasks=tasks,
    metrics=metrics,  # Track performance
)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "process-config", "skill": "crew-orchestration"},
        )