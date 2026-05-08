"""Azure AI Foundry Agent SDK - Microsoft's AI platform."""

from typing import Optional
import os

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig


class AzureAIFoundryAgent(BaseAgent):
    """Azure AI Foundry (formerly Azure AI Studio) specialist.
    
    Capabilities:
    - Model deployment configs
    - Prompt flow creation
    - Evaluation configs
    - Grounding configs
    - Connection definitions
    
    Tools: Azure OpenAI, Azure AI Search, Azure AI Storage
    Skills: prompt-engineering, evaluation, grounding, deployment
    """
    
    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        super().__init__(
            agent_id="azure-ai-foundry-writer",
            name="Azure AI Foundry Writer",
            description="Azure AI Foundry - deployments, prompt flows, evaluations",
            capabilities=[
                "deployment_config",
                "prompt_flow",
                "evaluation_config",
                "grounding_config",
                "connection_def",
            ],
            skills=["prompt-engineering", "evaluation", " grounding", "deployment", "azure"],
            api_key=api_key or os.getenv("AZURE_OPENAI_KEY"),
        )
        
        self.endpoint = endpoint or os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
        self.llm_config = LLMConfig.from_env()
        self._llm = None
    
    def _get_port(self) -> int:
        return 8013
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        if "deployment" in ct or "config" in ct:
            return self._deployment_config(request)
        elif "flow" in ct or "prompt" in ct:
            return self._prompt_flow(request)
        elif "evaluation" in ct or "eval" in ct:
            return self._evaluation_config(request)
        elif "ground" in ct:
            return self._grounding_config(request)
        else:
            return self._deployment_config(request)
    
    def _deployment_config(request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''# Deployment Config: {request.topic}

$schema: https://azureml境外schema/v2.0/schemas/llm/v2/component.yaml
component_type: llm
version: 1.0.0
name: {request.topic.lower().replace(' ', '_')}
display_name: {request.topic}

settings:
  model: gpt-4
  temperature: 0.7
  max_tokens: 2000
  api_base: ${{azure_endpoint}}
  api_version: "2024-02-01"

resources:
  instance_count: 1
  instance_type: Standard_E4ds_v4

provisioning:
  state: Succeeded
  mode: Manual
''',
            agent_id="azure-ai-foundry-writer",
            quality_score=0.85,
            metadata={"type": "deployment", "skill": "deployment"},
        )
    
    def _prompt_flow(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''# Prompt Flow: {request.topic}

nodes:
  - id: llm_1
    type: LLM
    source: ${{nodes.llm_1.input}}
    provider: AzureOpenAI
    connection: aoai_connection
    api: chat
    name: chat
    
  - id: input_1
    type: Input
    port: input
    
  - id: output_1
    type: Output
    source: ${{nodes.llm_1.output}}

edges:
  - from: input_1
    to: llm_1
  - from: llm_1
    to: output_1

# Flow definition YAML above
# Deploy via: az ml flow create
''',
            agent_id="azure-ai-foundry-writer",
            quality_score=0.85,
            metadata={"type": "prompt-flow", "skill": "prompt-engineering"},
        )
    
    def _evaluation_config(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''# Evaluation Config: {request.topic}

evaluation_config:
  name: {request.topic}_eval
  metrics:
    - gpt_similarity
    - accuracy
    - relevance
    
dataset:
  path: ./data/eval_data.jsonl
  
flow:
  path: ./prompt_flow/
  
run_settings:
  eval_type: pair wise
  num_workers: 4

# Run evaluation
# az ml evaluate --flow ./flow --eval-config config.yaml
''',
            agent_id="azure-ai-foundry-writer",
            quality_score=0.85,
            metadata={"type": "evaluation", "skill": "evaluation"},
        )
    
    def _grounding_config(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''# Grounding Config: {request.topic}

index:
  type: AzureAISearch
  connection: search_connection
  index_name: {request.topic.lower().replace(' ', '_')}_index
  field_mapping:
    content: content
    title: title
    url: url

chunking:
  strategy: parent
  chunk_size: 1024
  overlap: 100

# Use in prompt flow
grounding:
  index: ${{index}}
  source_type: AzureAISearch
  allow_list: [allowed_domain.com]
  block_list: [blocked.com]
''',
            agent_id="azure-ai-foundry-writer",
            quality_score=0.85,
            metadata={"type": "grounding", "skill": "grounding"},
        )