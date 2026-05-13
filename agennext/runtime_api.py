"""FastAPI route installer for the AgentGraph protocol runtime."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI

from a2a.card import get_agent_card, get_all_agent_cards
from agennext.a2a.runtime import create_default_runtime


def install_protocol_routes(app: FastAPI) -> None:
    """Install protocol runtime routes on an existing FastAPI app."""
    runtime = create_default_runtime()

    @app.post("/rpc")
    async def protocol_rpc(payload: dict[str, Any]) -> dict[str, Any]:
        return await runtime.handle(payload)

    @app.get("/agents/cards")
    async def list_agent_cards() -> dict[str, Any]:
        return {"agents": [card.model_dump() for card in get_all_agent_cards()]}

    @app.get("/agents/cards/{agent_id}")
    async def get_agent_card_route(agent_id: str) -> dict[str, Any]:
        card = get_agent_card(agent_id)
        if not card:
            return {"error": {"code": 404, "message": "Agent card not found"}}
        return {"agent": card.model_dump()}
