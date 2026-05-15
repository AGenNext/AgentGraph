FROM python:3.11-slim as backend
WORKDIR /app

# Security: Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Install dependencies in one layer
RUN pip install --no-cache-dir fastapi uvicorn pydantic aiohttp surrealdb

# Copy files
COPY --chown=appuser:appgroup main.py .
COPY --chown=appuser:appgroup server.py .
COPY --chown=appuser:appgroup api_registry/ ./api_registry/
COPY --chown=appuser:appgroup a2a/ ./a2a/
COPY --chown=appuser:appgroup agents/ ./agents/
COPY --chown=appuser:appgroup config.py .
COPY --chown=appuser:appgroup core/ ./core/
COPY --chown=appuser:appgroup orchestrator/ ./orchestrator/
COPY --chown=appuser:appgroup examples/ ./examples/
COPY --chown=appuser:appgroup surreal/ ./surreal/

# Security: Switch to non-root user
USER appuser

EXPOSE 8000

# Production: Set UID/GID
ENV UID=1000 GID=1000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8000/health || exit 1

# Run with production settings
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
