"""LangChain Agent SDK - LLM agent framework."""

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


class LangChainAgent(BaseAgent):
    """LangChain agent specialist.
    
    Capabilities:
    - Agent definitions (ReAct, OpenAI Functions, Tool former)
    - Chain creation
    - Tool integration
    - Memory management
    - Output parsers
    
    Tools: SerpAPI, DALL-E, Calculator, PythonREPL, Search
    Skills: chain-building, tool-use, memory, output-parsing
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            agent_id="langchain-writer",
            name="LangChain Agent Writer",
            description="LangChain - agents, chains, tools, memory",
            capabilities=[
                "agent_definition",
                "chain_creation",
                "tool_integration",
                "memory_management",
                "output_parsing",
                "prompt_templates",
            ],
            skills=["chain-building", "tool-use", "memory", "llm-ops"],
            api_key=api_key or os.getenv("LLM_API_KEY"),
        )
        
        self.llm_config = LLMConfig.from_env()
        self._llm = None
    
    def _get_port(self) -> int:
        return 8009
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        if "agent" in ct:
            return self._agent_def(request)
        elif "chain" in ct:
            return self._chain_create(request)
        elif "tool" in ct:
            return self._tool_integration(request)
        elif "memory" in ct:
            return self._memory_mgmt(request)
        elif "parser" in ct:
            return self._output_parser(request)
        else:
            return self._prompt_template(request)
    
    def _agent_def(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""LangChain Agent: {request.topic}"""

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

llm = ChatOpenAI(model="gpt-4", temperature=0)

@tool
def {request.topic.lower().replace(' ', '_')}(input: str) -> str:
    """Tool for {request.topic}."""
    return f"Result for: {{input}}"

tools = [{request.topic.lower().replace(' ', '_')}]

# Create agent
from langchain import hub
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm, tools, prompt)

# Run
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = agent_executor.invoke({{"input": "Your task"}})
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "agent-definition", "skill": "chain-building"},
        )
    
    def _chain_create(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""LangChain Chain: {request.topic}"""

from langchain import LLMChain, PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write about {{topic}}",
)

chain = LLMChain(llm=llm, prompt=prompt)

# Run
result = chain.run(topic="{request.topic}")
print(result)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "chain", "skill": "chain-building"},
        )
    
    def _tool_integration(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""LangChain Tool: {request.topic}"""

from langchain_core.tools import tool, Tool

# Using @tool decorator
@tool
def {request.topic.lower().replace(' ', '_')}(query: str) -> str:
    """Process {request.topic}."""
    return f"Processed: {{query}}"

# Or use structured Tool
structured_tool = Tool(
    name="{request.topic.replace(' ', '')}",
    func=my_func,
    description="Description of what it does",
)

# Use with agent
tools = [structured_tool]
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "tool-integration", "skill": "tool-use"},
        )
    
    def _memory_mgmt(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""LangChain Memory: {request.topic}"""

from langchain.memory import ConversationBufferMemory
from langchain import ConversationChain

# Buffer memory
memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True,
)

# Chat with history
chain = ConversationChain(llm=llm, memory=memory)
response = chain.predict(input="Hello")
print(response)

# Other options:
# - ConversationKGMemory
# - EntityMemory  
# - ReadOnlyMemory
# - WindowIndexedScratchPad
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "memory", "skill": "memory"},
        )
    
    def _output_parser(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""LangChain Output Parser: {request.topic}"""

from langchain.output_parsers import CommaSeparatedListOutputParser

# Parse list
parser = CommaSeparatedListOutputParser()
result = parser.parse("item1, item2, item3")

# Structured output
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

schemas = [
    ResponseSchema(name="answer", type="string", description="The answer"),
]
output_parser = StructuredOutputParser(response_schemas=schemas)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "output-parser", "skill": "llm-ops"},
        )
    
    def _prompt_template(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''"""Prompt Template: {request.topic}"""

from langchain import PromptTemplate

template = """You are {{role}}.
Task: {{task}}
Context: {{context}}
Answer: """

prompt = PromptTemplate(
    input_variables=["role", "task", "context"],
    template=template,
)

formatted = prompt.format(
    role="Expert",
    task="{request.topic}",
    context="Relevant info",
)
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "prompt-template", "skill": "llm-ops"},
        )