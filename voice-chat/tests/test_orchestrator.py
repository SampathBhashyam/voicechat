from __future__ import annotations

import asyncio

import pytest

from voicechat.adapters.interfaces import TranscriptEvent
from voicechat.orchestrator.session import SessionOrchestrator


class StubSTT:
    async def transcribe(self, audio_chunk: bytes) -> list[TranscriptEvent]:
        return [TranscriptEvent(text="hello", is_final=True)] if audio_chunk else []


class SlowTTS:
    async def synthesize(self, text: str) -> bytes:
        await asyncio.sleep(0.5)
        return b"RIFF...."


class StubAgentClient:
    async def ask(self, session_id: str, text: str) -> str:
        return f"reply:{text}"


class StubAudioOut:
    def __init__(self) -> None:
        self.play_count = 0

    async def play_wav_bytes(self, wav_bytes: bytes) -> None:
        self.play_count += 1


@pytest.mark.asyncio
async def test_handle_audio_chunk_returns_reply() -> None:
    orchestrator = SessionOrchestrator(
        stt=StubSTT(),
        tts=SlowTTS(),
        agent_client=StubAgentClient(),
        audio_out=StubAudioOut(),
        session_id="test",
    )

    reply = await orchestrator.handle_audio_chunk(b"audio")
    assert reply == "reply:hello"


@pytest.mark.asyncio
async def test_barge_in_cancels_tts_task() -> None:
    orchestrator = SessionOrchestrator(
        stt=StubSTT(),
        tts=SlowTTS(),
        agent_client=StubAgentClient(),
        audio_out=StubAudioOut(),
        session_id="test",
    )

    _ = await orchestrator.handle_transcript("first")
    await asyncio.sleep(0.05)

    await orchestrator.cancel_tts_if_playing()

    # If cancel succeeded, second request should continue normally.
    reply = await orchestrator.handle_transcript("second")
    assert reply == "reply:second"
    await orchestrator.shutdown()
