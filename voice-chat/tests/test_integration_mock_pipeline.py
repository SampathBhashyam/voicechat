from __future__ import annotations

import pytest
import httpx

from voicechat.adapters.tts import MockTTSEngine
from voicechat.agent.client import AgentClient
from voicechat.audio.io import AudioOutput
from voicechat.mock_server.app import app
from voicechat.orchestrator.session import SessionOrchestrator


class StubSTT:
    async def transcribe(self, audio_chunk: bytes):
        return []


class StubAudioOut(AudioOutput):
    def __init__(self) -> None:
        pass

    async def play_wav_bytes(self, wav_bytes: bytes) -> None:
        assert len(wav_bytes) > 0


@pytest.mark.asyncio
async def test_pipeline_with_asgi_mock_server() -> None:
    transport = httpx.ASGITransport(app=app)

    class LocalAgentClient(AgentClient):
        async def ask(self, session_id: str, text: str) -> str:
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.post(
                    "/agent/respond",
                    json={"session_id": session_id, "text": text, "timestamp": "2026-07-03T00:00:00Z"},
                )
                response.raise_for_status()
                return response.json()["reply_text"]

    orchestrator = SessionOrchestrator(
        stt=StubSTT(),
        tts=MockTTSEngine(),
        agent_client=LocalAgentClient(base_url="http://test"),
        audio_out=StubAudioOut(),
        session_id="integration",
    )

    reply = await orchestrator.handle_transcript("test question")
    assert reply == "Mock agent reply: test question"
    await orchestrator.shutdown()
