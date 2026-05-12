# Dockerize Schema.org Platform

## Dockerfile

```dockerfile
# Schema.org Platform - Dockerfile
# Build: docker build -t schema-org-platform .
# Run: docker run -p 8000:8000 schema-org-platform

FROM python:3.11-slim

LABEL maintainer="schema-org@platform.dev"
LABEL description="Schema.org Implementation Platform"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace/project

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000 5432 6379

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV SCHEMA_VERSION=30.0

# Default command
CMD ["python", "-m", "schema_org_server"]
```

## Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Schema.org API Server
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=surrealdb://memory:server/
      - REDIS_URL=redis://redis:6379
      - SCHEMA_VERSION=30.0
    depends_on:
      - surrealdb
      - redis
    volumes:
      - ./data:/data

  # SurrealDB Database
  surrealdb:
    image: surrealdb/surrealdb:latest
    ports:
      - "8000:8000"
    command: start --user root --pass root memory
    volumes:
      - surrealdb_data:/persist

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Schema.org Graph Engine
  graph:
    build: .
    command: python -m schema_org_graph
    depends_on:
      - surrealdb

  # Time Search Service
  search:
    build: .
    command: python -m time_search
    depends_on:
      - surrealdb
      - redis

volumes:
  surrealdb_data:
  redis_data:
```

## Build & Run

```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## Container Structure

```
┌─────────────────────────────────────────┐
│  Schema.org Platform Container          │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐            │
│  │   API   │  │  Graph   │            │
│  │ Server  │  │ Engine  │            │
│  └────┬────┘  └────┬────┘            │
│       │            │                  │
│  ┌────┴────────────┴────┐           │
│  │   SurrealDB Engine    │           │
│  │   (In-Memory)        │           │
│  └─────────────────────┘           │
└─────────────────────────────────────────┘
```

## Schema.org Services

| Service | Port | Description |
|---------|------|-------------|
| API Server | 8000 | REST API |
| SurrealDB | 8000 | Database |
| Graph Engine | 8001 | Graph queries |
| Time Search | 8002 | Time-based search |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| SCHEMA_VERSION | 30.0 | Schema.org version |
| DATABASE_URL | surrealdb://memory | Database URL |
| REDIS_URL | redis://localhost:6379 | Cache URL |
| LOG_LEVEL | INFO | Logging level |
| MAX_CONNECTIONS | 100 | DB connections |
| CACHE_TTL | 3600 | Cache TTL (seconds) |

## Health Checks

```yaml
# Docker Compose healthchecks
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

Reference: https://docs.docker.com | https://surrealdb.com/docs