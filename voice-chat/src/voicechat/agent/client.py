from __future__ import annotations

import logging
from datetime import UTC, datetime

import httpx

logger = logging.getLogger(__name__)


class AgentClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    async def ask(self, session_id: str, text: str) -> str:
        payload = {
            "session_id": session_id,
            "text": text,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        logger.debug("agent.request base_url=%s text_len=%d", self._base_url, len(text))
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{self._base_url}/agent/respond", json=payload)
            response.raise_for_status()
        data = response.json()
        reply_text = data.get("reply_text", "")
        logger.debug("agent.response text_len=%d", len(reply_text))
        return reply_text
