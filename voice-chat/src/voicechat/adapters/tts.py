from __future__ import annotations

import logging
import wave
from dataclasses import dataclass
from io import BytesIO

import numpy as np

from .interfaces import TTSEngine

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class MockTTSEngine(TTSEngine):
    """Generates a short tone so playback path can be tested without external binaries."""

    sample_rate: int = 16000
    duration_seconds: float = 0.6

    async def synthesize(self, text: str) -> bytes:
        logger.debug("mock_tts.synthesize chars=%d", len(text))
        t = np.linspace(0, self.duration_seconds, int(self.sample_rate * self.duration_seconds), endpoint=False)
        signal = (0.2 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

        pcm16 = (signal * 32767).astype(np.int16)
        with BytesIO() as bio:
            with wave.open(bio, "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(self.sample_rate)
                wav.writeframes(pcm16.tobytes())
            return bio.getvalue()


class PiperTTSEngine(TTSEngine):
    """Placeholder adapter boundary for Piper CLI integration in next revision."""

    async def synthesize(self, text: str) -> bytes:
        raise NotImplementedError("Piper adapter wiring is not implemented in v1 mock")
