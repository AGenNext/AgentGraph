"""
LangChain SDK Client.

https://python.langchain.com/
"""

from typing import Optional, List, Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


class LangChainClient:
    """LangChain SDK client for agents."""
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        temperature: float = 0.7,
        **kwargs
    ):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=api_key,
            **kwargs
        )
        self.memory = ConversationBufferMemory(
            chat_history=[],
            return_messages=True
        )
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """Chat completion."""
        langchain_messages = []
        for msg in messages:
            if msg.get("role") == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
            else:
                langchain_messages.append(HumanMessage(content=msg["content"]))
        
        response = self.llm.invoke(langchain_messages)
        return response.content
    
    def complete(self, prompt: str, **kwargs) -> str:
        """Text completion."""
        return self.llm.invoke(prompt)
    
    def create_agent(
        self,
        agent_type: str = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        tools: Optional[List[Tool]] = None,
        system_message: Optional[str] = None
    ):
        """Create an agent."""
        return initialize_agent(
            tools=tools or [],
            llm=self.llm,
            agent=agent_type,
            memory=self.memory,
            verbose=True
        )
    
    def add_tool(self, name: str, func, description: str) -> Tool:
        """Add a tool."""
        return Tool(
            name=name,
            func=func,
            description=description
        )
    
    def get_memory(self) -> ConversationBufferMemory:
        """Get conversation memory."""
        return self.memory
    
    def clear_memory(self):
        """Clear conversation memory."""
        self.memory.clear()


def create_client(api_key: str, model: str = "gpt-4", **kwargs) -> LangChainClient:
    """Create LangChain client."""
    return LangChainClient(api_key=api_key, model=model, **kwargs)
