"""GitHub Agent SDK - Repository and developer workflow content."""

from typing import Optional, List
import os

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig, PROVIDERS


class GitHubAgent(BaseAgent):
    """GitHub content specialist.
    
    Capabilities:
    - README documentation
    - PR descriptions
    - Commit messages
    - GitHub Actions workflows
    - Issue templates
    - CONTBIDING guides
    
    Tools: gh CLI, git, GitHub API
    Skills: markdown, yaml, ci-cd
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            agent_id="github-dev-writer",
            name="GitHub Developer Writer",
            description="GitHub - READMEs, PRs, Actions, issues",
            capabilities=[
                "readme_docs",
                "pr_descriptions", 
                "commit_messages",
                "github_actions",
                "issue_templates",
                "contributing_docs",
            ],
            skills=["markdown", "yaml", "ci-cd", "documentation", "git"],
            api_key=api_key or os.getenv("GITHUB_TOKEN") or os.getenv("LLM_API_KEY"),
        )
        
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.llm_config = LLMConfig.from_env()
        self._llm = None
    
    def _get_port(self) -> int:
        return 8006
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        if "readme" in ct:
            return self._readme(request)
        elif "pr" in ct:
            return self._pr_desc(request)
        elif "action" in ct or "workflow" in ct:
            return self._action(request)
        elif "issue" in ct:
            return self._issue(request)
        else:
            return self._contributing(request)
    
    def _readme(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f"""# {request.topic}

[![CI](https://github.com/org/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/org/repo/actions)
[![License](https://img.shields.io/github/license/org/repo.svg)](LICENSE)

{request.topic} - Brief description here.

## Features

- Feature one
- Feature two

## Quick Start

```bash
pip install {request.topic.lower().replace(' ', '-')}
```

## Documentation

See [docs/](docs/) for full guide.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT - see [LICENSE](LICENSE).
""",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "readme", "skill": "documentation"},
        )
    
    def _pr_desc(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f"""## {request.topic}

### Summary
Describe changes here.

### Changes
- [ ] Change one

### Testing
```bash
pytest tests/
```

### Related Issues
Closes #000
""",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "pr-description", "skill": "documentation"},
        )
    
    def _action(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f"""name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install -e .
    - run: pytest
""",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "github-action", "skill": "ci-cd"},
        )
    
    def _issue(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f"""## {request.topic}

### Steps to reproduce
1. 
2. 

### Expected behavior


### Actual behavior


### Environment
- OS:
- Version:

### Labels
- bug
- enhancement
""",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "issue-template", "skill": "documentation"},
        )
    
    def _contributing(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f"""# Contributing to {request.topic}

## Setup

```bash
git clone https://github.com/org/repo.git
pip install -e ".[dev]"
```

## Testing

```bash
pytest -v
```

## Pull Request Process

1. Fork
2. Create branch
3. Make changes
4. Submit PR
""",
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "contributing", "skill": "documentation"},
        )