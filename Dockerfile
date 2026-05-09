FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn pydantic aiohttp psycopg2-binary
COPY main.py .
COPY api_registry/ ./api_registry/
COPY a2a/ ./a2a/
COPY agents/ ./agents/
COPY config.py .
COPY core/ ./core/
COPY orchestrator/ ./orchestrator/
COPY examples/ ./examples/
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
