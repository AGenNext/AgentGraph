"""Docker Agent SDK - Container and deployment content writer."""

from typing import Optional, List
import os

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig


class DockerAgent(BaseAgent):
    """Docker & container content specialist.
    
    Capabilities:
    - Dockerfile generation
    - Docker Compose configs
    - Kubernetes manifests  
    - DevOps documentation
    - Deployment guides
    
    Tools: docker, kubectl, docker-compose
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            agent_id="docker-devops-writer",
            name="Docker DevOps Writer",
            description="Docker & K8s specialist - Dockerfiles, manifests, DevOps",
            capabilities=[
                "dockerfile_content",
                "docker_compose", 
                "kubernetes_yaml",
                "devops_docs",
                "deployment_guides",
            ],
            skills=["docker", "kubernetes", "devops", "ci-cd", "containers"],
            api_key=api_key or os.getenv("LLM_API_KEY"),
        )
        
        self.llm_config = LLMConfig.from_env()
        self._llm = None
    
    def _get_port(self) -> int:
        return 8005
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        if "dockerfile" in ct:
            return self._dockerfile_content(request)
        elif "compose" in ct:
            return self._docker_compose(request)
        elif "k8s" in ct or "kubernetes" in ct:
            return self._k8s_content(request)
        else:
            return self._devops_docs(request)
    
    def _dockerfile_content(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f"""# Dockerfile for {request.topic}

FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python", "main.py"]""",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "dockerfile", "skill": "docker"},
        )
    
    def _docker_compose(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f"""services:
  app:
    build: .
    ports:
      - "8000:8000"
    restart: unless-stopped
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
""",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "compose", "skill": "docker-compose"},
        )
    
    def _k8s_content(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {request.topic.lower().replace(' ', '-')}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {request.topic.lower().replace(' ', '-')}
  template:
    spec:
      containers:
      - name: app
        image: {request.topic.lower().replace(' ', '-'):latest}
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: {request.topic.lower().replace(' ', '-')}
spec:
  selector:
    app: {request.topic.lower().replace(' ', '-')}
  ports:
  - port: 80
    targetPort: 8000
""",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "kubernetes", "skill": "kubernetes"},
        )
    
    def _devops_docs(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f"""# DevOps: {request.topic}

## Prerequisites
- Docker 20.10+
- kubectl

## Deploy
```bash
kubectl apply -f k8s/
```
""",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "docs", "skill": "devops"},
        )