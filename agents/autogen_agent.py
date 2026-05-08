"""Microsoft AutoGen Agent SDK - Multi-agent orchestration."""

from typing import Optional, List, Dict
import os

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig


class AutoGenAgent(BaseAgent):
    """Microsoft AutoGen (now AutoGen Studio) specialist.
    
    Capabilities:
    - Agent definitions (Conversational, Assistant, UserProxy)
    - Group chat configurations
    - Speaker selection policies
    - Nested chat patterns
    - Custom tool integration
    
    Tools: code_executor, websearch, file_read, serper
    Skills: multi-agent, orchestration, tool-use, code-execution
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            agent_id="autogen-writer",
            name="Microsoft AutoGen Writer",
            description="AutoGen - multi-agent orchestration, group chats",
            capabilities=[
                "agent_definition",
                "group_chat",
                "speaker_selection",
                "nested_chat",
                "tool_integration",
            ],
            skills=["multi-agent", "orchestration", "tool-use", "code-execution", "conversation"],
            api_key=api_key or os.getenv("LLM_API_KEY"),
        )
        
        self.llm_config = LLMConfig.from_env()
        self._llm = None
    
    def _get_port(self) -> int:
        return 8014
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        if "agent" in ct and "group" not in ct:
            return self._agent_def(request)
        elif "group" in ct:
            return self._group_chat(request)
        elif "speaker" in ct:
            return self._speaker_selection(request)
        elif "nested" in ct:
            return self._nested_chat(request)
        else:
            return self._tool_integration(request)
    
    def _agent_def(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""AutoGen Agent: {request.topic}"""

from autogen import ConversableAgent, UserProxyAgent, AssistantAgent

# Assistant agent (llm-based)
assistant = AssistantAgent(
    name="{request.topic.replace(' ', '_').lower()}_assistant",
    llm_config={{
        "model": "gpt-4",
        "api_key": "your-api-key",
    }},
    system_message="You are a helpful {request.topic} assistant.",
)

# User proxy (human in the loop)
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    code_execution_config={{"workdir": "coding"}},

# Start conversation
user_proxy.initiate_chat(
    assistant,
    message="Help me with {request.topic}"
)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "agent-definition", "skill": "multi-agent"},
        )
    
    def _group_chat(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""Group Chat: {request.topic}"""

from autogen import ConversableAgent, GroupChat, GroupChatManager

# Create multiple agents
researcher = ConversableAgent(name="Researcher", llm_config={{...}})
coder = ConversableAgent(name="Coder", llm_config={{...}})
writer = ConversableAgent(name="Writer", llm_config={{...}})

# Create group chat
group_chat = GroupChat(
    agents=[researcher, coder, writer],
    messages=[],
    max_round=5,
)

# Create manager
manager = GroupChatManager(
    groupchat=group_chat,
    name="manager",
)

# Initiate
user_proxy.initiate_chat(
    manager,
    message="Write code for {request.topic}, then document it"
)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "group-chat", "skill": "orchestration"},
        )
    
    def _speaker_selection(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""Speaker Selection: {request.topic}"""

from autogen import GroupChat, SpeakerSelection

# Round robin selection
round_robin = SpeakerSelection(
    algorithm="round_robin",
)

# LLM-based selection
llm_speaker = SpeakerSelection(
    algorithm="llm",
    llm=llm,
    prompt="Select the best agent for: {{task}}",
)

# Use in group chat
group_chat = GroupChat(
    agents=[agent1, agent2, agent3],
    speaker_selection=llm_speaker,
)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "speaker-selection", "skill": "orchestration"},
        )
    
    def _nested_chat(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""Nested Chat: {request.topic}"""

from autogen import ConversableAgent

# Agent that can delegate
manager_agent = ConversableAgent(
    name="manager",
    llm_config={{...}},
)

# Sub-agent
sub_agent = ConversableAgent(
    name="sub_{request.topic.replace(' ', '_').lower()}",
    llm_config={{...}},
)

# Nested chat via initiate_chat
manager_agent.initiate_chat(
    sub_agent,
    message=f"Help me with {request.topic}"
)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "nested-chat", "skill": "multi-agent"},
        )
    
    def _tool_integration(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""AutoGen Tool Integration: {request.topic}"""

from autogen import ConversableAgent, UserProxyAgent
from autogen.code_utils import create_python_executor
from autogen.agentchat import Tool

# Code execution tool
code_executor = create_python_executor()

# Custom tool
def web_search(query: str) -> str:
    return f"Results for: {{query}}"

tool = Tool(
    name="web_search",
    func=web_search,
    description="Search the web",
)

# Use with agent
agent = ConversableAgent(
    name="{request.topic.replace(' ', '_').lower()}",
    llm_config={{...}},
    tools=[tool, code_executor],
)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "tool-integration", "skill": "tool-use"},
        )