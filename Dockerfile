# Stage 1: Python backend
FROM python:3.11-slim as backend
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

# Stage 2: Next.js frontend
FROM node:20-alpine as frontend
WORKDIR /app
COPY agennext-ui/package.json agennext-ui/tsconfig.json agennext-ui/next.config.js ./
RUN npm install
COPY agennext-ui/lib ./lib
COPY agennext-ui/components ./components
COPY agennext-ui/hooks ./hooks
COPY agennext-ui/types ./types
COPY agennext-ui/app ./app
RUN npm run build
EXPOSE 3000

# Final stage
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm
COPY --from=backend /app /app
COPY --from=frontend /app/.next /frontend/.next
WORKDIR /app
EXPOSE 8000 3000
CMD ["sh", "-c", "npm install -g serve && serve /frontend/.next/standalone & uvicorn main:app --host 0.0.0.0 --port 8000"]
