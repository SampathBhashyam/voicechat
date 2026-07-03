from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from voicechat.adapters.interfaces import STTEngine, TTSEngine
from voicechat.agent.client import AgentClient
from voicechat.audio.io import AudioOutput

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class SessionOrchestrator:
    stt: STTEngine
    tts: TTSEngine
    agent_client: AgentClient
    audio_out: AudioOutput
    session_id: str
    barge_in_policy: str = "stop"

    def __post_init__(self) -> None:
        self._tts_task: asyncio.Task[None] | None = None

    async def handle_audio_chunk(self, audio_chunk: bytes) -> str | None:
        events = await self.stt.transcribe(audio_chunk)
        final_events = [e for e in events if e.is_final and e.text.strip()]
        if not final_events:
            return None

        transcript = final_events[-1].text.strip()
        logger.info("stt.final %s", transcript)
        return await self.handle_transcript(transcript)

    async def handle_transcript(self, transcript: str) -> str:
        if self.barge_in_policy == "stop":
            await self.cancel_tts_if_playing()

        reply = await self.agent_client.ask(session_id=self.session_id, text=transcript)
        logger.info("agent.reply %s", reply)

        self._tts_task = asyncio.create_task(self._speak(reply))
        return reply

    async def _speak(self, text: str) -> None:
        audio = await self.tts.synthesize(text)
        await self.audio_out.play_wav_bytes(audio)

    async def cancel_tts_if_playing(self) -> None:
        if self._tts_task and not self._tts_task.done():
            logger.info("barge_in.cancel_tts")
            self._tts_task.cancel()
            try:
                await self._tts_task
            except asyncio.CancelledError:
                pass
            finally:
                self._tts_task = None

    async def shutdown(self) -> None:
        await self.cancel_tts_if_playing()
