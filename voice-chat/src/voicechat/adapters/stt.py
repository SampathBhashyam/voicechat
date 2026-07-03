from __future__ import annotations

import logging
from dataclasses import dataclass

from .interfaces import STTEngine, TranscriptEvent

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class MockSTTEngine(STTEngine):
    """Mock STT adapter used for local plumbing and tests."""

    canned_text: str = "what is the weather today"

    async def transcribe(self, audio_chunk: bytes) -> list[TranscriptEvent]:
        if not audio_chunk:
            return []
        logger.debug("mock_stt.transcribe bytes=%d", len(audio_chunk))
        return [TranscriptEvent(text=self.canned_text, is_final=True)]


class FasterWhisperSTTEngine(STTEngine):
    """Optional adapter. Requires installing voicechat[stt]."""

    def __init__(self, model_size: str = "small") -> None:
        try:
            from faster_whisper import WhisperModel  # type: ignore
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "faster-whisper is not installed. Install with: pip install '.[stt]'"
            ) from exc
        self._model = WhisperModel(model_size, device="cpu", compute_type="int8")

    async def transcribe(self, audio_chunk: bytes) -> list[TranscriptEvent]:
        # Binary audio decoding path is intentionally deferred for v1.
        # Keep adapter boundary stable while mock mode drives integration.
        raise NotImplementedError("Raw byte decoding pipeline not yet implemented for faster-whisper adapter")
