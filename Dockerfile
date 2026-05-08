FROM python:3.11-slim

LABEL maintainer="content-team@agenext.io"
LABEL description="Multi-SDK Content Writing Team - 48+ LLM providers with LangGraph A2A"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 writer && chown -R writer:writer /app
USER writer

# Expose ports
# 8000: Main API
# 8001-8014: SDK agents
EXPOSE 8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010 8011 8012 8013 8014

# Environment variables (can be overridden)
ENV PYTHONUNBUFFERED=1
ENV A2A_HOST=0.0.0.0
ENV A2A_PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["python", "main.py", "--mode", "server"]