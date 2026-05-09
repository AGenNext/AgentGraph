# AGenNext Agent Registry - Docker Image
# Status: ALPHA

FROM python:3.11-slim

LABEL maintainer="AGenNext <info@agennext.io>"
LABEL version="0.1.0"
LABEL description="Enterprise Multi-Agent Team Platform"

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agents/ /app/agents/
COPY ui/ /app/ui/
COPY examples/ /app/examples/
COPY platform-ui/ /app/platform-ui/
COPY *.md /app/
COPY *.json /app/
COPY *.yaml /app/

# Expose ports
EXPOSE 7860 8501

# Default command
CMD ["python", "ui/examples.py", "chat"]

# Healthcheck for container health
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

