# AGenNext AgentGraph

> Protocol-native control plane for enterprise AI agents: A2A messaging, registry discovery, trust scoring, governance, identity, authorization, and a public GitHub Pages landing site.

[![Platform](https://img.shields.io/badge/AGenNext-AgentGraph-blue)](https://github.com/AGenNext/AgentGraph)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org)

## Overview

AgentGraph is the AGenNext platform for building, discovering, coordinating, and governing AI agents. It combines a FastAPI backend, a Next.js frontend, and a protocol runtime inspired by [AGenNext Protocols](https://github.com/AGenNext/AGenNext-Protocols).

## Implemented Protocol Runtime

| Module | Path | Purpose |
|---|---|---|
| A2A Runtime | `agennext.a2a` | JSON-RPC task submission, messaging, task lookup, and agent card lookup |
| Registry | `agennext.registry` | Register and discover agents by capability or skill |
| Trust | `agennext.trust` | Track trust scores, successes, failures, endorsements, and delegation decisions |
| Governance | `agennext.governance` | Evaluate agent actions against review/deny policies and risk levels |
| Agent ID | `agennext.agentid` | Lightweight agent identity and token issuance primitives |
| Agent DID | `agennext.agentdid` | DID-style identity document creation and resolution |
| AuthZen | `agennext.authzen` | Authorization decision primitives for sensitive actions |

## Runtime API

The protocol routes are installed through `agennext.runtime_api`.

```python
from agennext.runtime_api import install_protocol_routes

install_protocol_routes(app)
```

This exposes:

| Endpoint | Description |
|---|---|
| `POST /rpc` | JSON-RPC endpoint for A2A runtime methods |
| `GET /agents/cards` | List available agent cards |
| `GET /agents/cards/{agent_id}` | Fetch a single agent card |

### Example JSON-RPC request

```bash
curl -X POST http://localhost:8000/rpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tasks/submit",
    "params": {
      "message": {"role": "user", "content": "Write a launch brief"}
    }
  }'
```

Supported runtime methods:

- `agents/list`
- `agents/get`
- `tasks/submit`
- `tasks/sendMessage`
- `tasks/get`
- `tasks/list`

## Landing Page

The frontend now includes a public landing page at `agennext-ui/app/page.tsx`.

Run locally:

```bash
cd agennext-ui
npm install
npm run dev
```

## GitHub Pages

A GitHub Pages deployment workflow is included at `.github/workflows/deploy-pages.yml`.

After merging to `main`:

1. Open repository Settings.
2. Go to Pages.
3. Set Source to GitHub Actions.
4. Push to `main` or run the workflow manually.

Expected site URL:

```text
https://agennext.github.io/AgentGraph/
```

## Backend Quick Start

```bash
pip install fastapi uvicorn pydantic aiohttp psycopg2-binary
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Quick Start

```bash
cd agennext-ui
npm install
npm run dev
```

## Tests

Protocol tests live in `tests/test_protocol_runtime.py`.

```bash
pip install pytest
pytest tests/test_protocol_runtime.py
```

## Current Status

Implemented:

- A2A protocol runtime foundation
- Registry, trust, governance, identity, DID, and AuthZen primitives
- FastAPI protocol route installer
- Landing page
- GitHub Pages deployment workflow
- Initial protocol unit tests

Still recommended before production use:

- Install the protocol routes directly in `main.py`
- Add CI to run Python and frontend tests
- Replace in-memory protocol stores with persistent storage
- Add real cryptographic token signing and verification
- Add authentication middleware for write endpoints
- Add more integration tests around FastAPI `/rpc`

## Related Repositories

- [AGenNext Protocols](https://github.com/AGenNext/AGenNext-Protocols)
- [openagx](https://github.com/openagx)

## License

MIT License - See [LICENSE](LICENSE).
