"""Microsoft Enterprise Writer Agent."""

from typing import Optional, Callable, Any
import os
import time
import logging

from agents.base_agent import BaseAgent, ContentRequest, ContentResult

logger = logging.getLogger(__name__)


# === Middleware Hooks for Tool Calls ===
class ToolCallMiddleware:
    """Middleware hooks for pre/post tool call events."""
    
    def __init__(self):
        self.pre_tool_call_hooks: list[Callable] = []
        self.post_tool_call_hooks: list[Callable] = []
    
    def register_pre_tool_call_hook(self, hook: Callable[[str, dict], None]):
        """Register a hook to run BEFORE tool call.
        
        Args:
            hook: Callable that takes (tool_name, tool_input) and returns None
        """
        self.pre_tool_call_hooks.append(hook)
        logger.info(f"Registered pre-tool-call hook: {hook.__name__}")
    
    def register_post_tool_call_hook(self, hook: Callable[[str, dict, Any], None]):
        """Register a hook to run AFTER tool call.
        
        Args:
            hook: Callable that takes (tool_name, tool_input, tool_result) and returns None
        """
        self.post_tool_call_hooks.append(hook)
        logger.info(f"Registered post-tool-call hook: {hook.__name__}")
    
    def run_pre_tool_call_hooks(self, tool_name: str, tool_input: dict):
        """Run all pre-tool-call hooks."""
        for hook in self.pre_tool_call_hooks:
            try:
                hook(tool_name, tool_input)
            except Exception as e:
                logger.error(f"Pre-tool-call hook {hook.__name__} failed: {e}")
    
    def run_post_tool_call_hooks(self, tool_name: str, tool_input: dict, result: Any):
        """Run all post-tool-call hooks."""
        for hook in self.post_tool_call_hooks:
            try:
                hook(tool_name, tool_input, result)
            except Exception as e:
                logger.error(f"Post-tool-call hook {hook.__name__} failed: {e}")


class MicrosoftAgent(BaseAgent):
    """Enterprise content writer using Microsoft Azure OpenAI.

    Preferred Model: gpt-4 (Azure Deployment)
    
    Supports pre_tool_call_hook and post_tool_call_hook for middleware.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        deployment: Optional[str] = None,
        enable_middleware: bool = True,
    ):
        super().__init__(
            agent_id="microsoft-enterprise-writer",
            name="Microsoft Enterprise Writer",
            description="Enterprise content writer with Microsoft 365 integration",
            capabilities=["enterprise_content", "technical_docs", "m365_integration"],
            skills=["enterprise-writing", "technical-writing", "documentation"],
            api_key=api_key or os.getenv("AZURE_OPENAI_KEY"),
        )
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        self._client = None
        
        # Middleware hooks for tool calls
        self._middleware = ToolCallMiddleware() if enable_middleware else None
    
    @property
    def pre_tool_call_hook(self) -> Callable[[str, dict], None]:
        """Register pre-tool-call hook (runs before tool execution)."""
        return self._middleware.register_pre_tool_call_hook
    
    @property
    def post_tool_call_hook(self) -> Callable[[str, dict, Any], None]:
        """Register post-tool-call hook (runs after tool execution)."""
        return self._middleware.register_post_tool_call_hook
    
    def _execute_tool_with_middleware(self, tool_name: str, tool_input: dict, tool_func: Callable) -> Any:
        """Execute tool with pre/post hooks."""
        # Pre-tool-call hooks
        if self._middleware:
            self._middleware.run_pre_tool_call_hooks(tool_name, tool_input)
        
        start_time = time.time()
        result = tool_func(**tool_input)
        duration = int((time.time() - start_time) * 1000)
        
        # Post-tool-call hooks
        if self._middleware:
            self._middleware.run_post_tool_call_hooks(tool_name, tool_input, result)
        
        logger.info(f"Tool {tool_name} executed in {duration}ms")
        return result
    
    def _get_port(self) -> int:
        return 8003
    
    def _get_client(self):
        """Get or create Azure OpenAI client."""
        if self._client is None and self.api_key and self.endpoint:
            try:
                from azure.ai.openai import OpenAIClient
                from azure.identity import DefaultAzureCredential
                
                self._client = OpenAIClient(
                    endpoint=self.endpoint,
                    credential=DefaultAzureCredential(),
                )
            except ImportError:
                self._client = None
        return self._client
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        """Generate enterprise/technical content."""
        client = self._get_client()
        
        prompt = self._build_prompt(request)
        
        if client:
            try:
                response = client.completions.create(
                    model=self.deployment,
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=2000,
                )
                content = response.choices[0].text
                return ContentResult(
                    content=content,
                    agent_id=self.agent_id,
                    quality_score=0.92,
                    metadata={"deployment": self.deployment, "provider": "azure"},
                )
            except Exception:
                return self._mock_response(prompt, request)
        else:
            return self._mock_response(prompt, request)
    
    def _build_prompt(self, request: ContentRequest) -> str:
        """Build enterprise-focused prompt."""
        
        if request.content_type == "technical_docs":
            base = f"Write comprehensive technical documentation for: {request.topic}.\n"
            base += "Follow enterprise technical writing standards.\n"
        else:
            base = f"Write enterprise-grade {request.content_type} about: {request.topic}.\n"
        
        if request.context.get("audience"):
            base += f" Target audience: {request.context['audience']}.\n"
        
        if request.context.get("compliance"):
            base += f" Ensure compliance: {request.context['compliance']}.\n"
        
        return base
    
    def _mock_response(self, prompt: str, request: ContentRequest) -> ContentResult:
        """Mock response for demo mode."""
        
        if request.content_type == "technical_docs":
            template = f"""# Technical Documentation: {request.topic.title()}

## Overview

This document provides comprehensive technical documentation for **{request.topic}**.
It is designed for technical users and follows enterprise documentation standards.

## Prerequisites

- System requirements
- Access permissions
- Required dependencies

## Installation

```bash
# Install via package manager
pip install {request.topic.lower().replace(' ', '-')}
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable feature |
| timeout | int | 30 | Request timeout |
| retries | int | 3 | Retry attempts |

## API Reference

### `initialize(config)`

Initialize the component with configuration.

**Parameters:**
- `config` (dict): Configuration object

**Returns:**
- `bool`: Success status

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Connection timeout | Check network/firewall |
| Authentication | Verify credentials |

## Compliance Notes

This documentation follows enterprise compliance standards.

---

*Generated by {self.name} | Microsoft Azure*"""
        else:
            template = f"""# Enterprise Solution: {request.topic.title()}

## Executive Summary

This document presents our enterprise-grade solution for {request.topic}.

## Business Value

- **Scalability**: Enterprise-ready infrastructure
- **Security**: Full compliance and data protection
- **Integration**: Microsoft 365 ecosystem ready
- **Support**: 24/7 enterprise support

## Technical Architecture

```
┌─────────────────┐
│  Frontend       │
├─────────────────┤
│  API Gateway    │
├─────────────────┤
│  Azure Services │
├─────────────────┤
│  Data Layer    │
└─────────────────┘
```

## Implementation Roadmap

| Phase | Timeline | Deliverable |
|-------|----------|-------------|
| 1 | Week 1-2 | Setup & Config |
| 2 | Week 3-4 | Integration |
| 3 | Week 5-6 | Testing & Deploy |

## Support & Maintenance

- **Tiers**: Premium, Standard, Basic
- **SLA**: 99.9% uptime guarantee
- **Updates**: Monthly security patches

---

*Generated by {self.name} | Microsoft Enterprise*"""
        
        return ContentResult(
            content=template,
            agent_id=self.agent_id,
            quality_score=0.90,
            metadata={"provider": "azure", "enterprise": True},
        )