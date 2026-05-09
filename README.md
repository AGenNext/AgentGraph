# AGenNext Agent Registry

![Alpha](https://img.shields.io/badge/Status-ALPHA-red)
![Version](https://img.shields.io/badge/Version-0.1.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## ⚠️ ALPHA - Not for Production

Enterprise Multi-Agent Team Platform with support for:

- **OpenAI SDK** - Agents, Assistants, Fine-tuning
- **Microsoft Agent Framework** - Azure AI Agents, Copilot
- **Google ADK** - Gemini, Vertex AI, Grounded Generation
- **Salesforce Agent SDK** - Einstein Agents
- **LangChain/LangGraph** - RAG, Workflows, Orchestration
- **AWS Bedrock** - Claude, Titan, Llama, Command
- **Anthropic** - Claude Models
- **A2A Protocol** - Agent-to-Agent Communication

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/AGenNext/AGenNext-Enterprise.git
cd AGenNext-Enterprise

# Install
pip install -r requirements.txt

# Run UI
python ui/examples.py chat

# Or with Docker
docker-compose up
```

---

## 📦 What's Included

| Module | Description |
|--------|-------------|
| `agents/` | Provider clients for all SDKs |
| `ui/` | UI builders (Gradio, Streamlit) |
| `platform-ui/` | Platform UI spec |
| `.github/` | CI/CD workflows |

---

## 🔧 Supported Providers

| Provider | Auth Methods |
|----------|-------------|
| OpenAI | api_key, oauth |
| Anthropic | api_key |
| Google | api_key, gcp_service_account |
| Microsoft | azure_ad, managed_identity |
| AWS Bedrock | iam |
| Custom | openai-compatible |

---

## 🎯 Features

- Multi-provider support
- Agent role management (Supervisor, Worker, Router)
- UI toolkits for every SDK
- Runnable examples
- CI/CD with Docker
- Security scanning

---

## 📖 Documentation

- [PROJECTS.md](PROJECTS.md) - Roadmap & milestones
- [platform-ui/SPEC.md](platform-ui/SPEC.md) - UI specification
- [DOCKER_README.md](DOCKER_README.md) - Docker setup
- [memory.yaml](memory.yaml) - Project memory (YAML)
- [memory.json](memory.json) - Project memory (JSON)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Platform UI                    │
├─────────────────────────────────────────┤
│  LangGraph Orchestration                │
├─────────────────────────────────────────┤
│  OpenAI │ Google │ Microsoft │ LangChain │
│  Anthropic │ AWS Bedrock │ Salesforce│
├─────────────────────────────────────────┤
│        A2A Protocol                   │
└─────────────────────────────────────────┘
```

---

## 🐳 Docker

```bash
# Build
docker build -t agennext/agent-registry .

# Run
docker run -p 7860:7860 agennext/agent-registry

# Or use GHCR
docker pull ghcr.io/agennext/agent-registry:latest
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Submit PR

**Status:** ALPHA - Feedback welcome

---

## 📞 Support

- Issues: [GitHub Issues](https://github.com/AGenNext/AGenNext-Enterprise/issues)

---

*Last updated: 2026-05-08*
