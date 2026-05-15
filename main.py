"""Compatibility entrypoint for the FastAPI app.

The repository now treats SurrealDB as the canonical database path.
`server.py` contains the active API implementation, and this module
re-exports its ASGI app so existing `main:app` references keep working.
"""

from server import app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
