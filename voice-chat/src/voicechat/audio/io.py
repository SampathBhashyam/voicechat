from __future__ import annotations

import logging
import wave
from io import BytesIO

import numpy as np

logger = logging.getLogger(__name__)


class AudioOutput:
    def __init__(self) -> None:
        try:
            import sounddevice as sd  # type: ignore
        except Exception:  # pragma: no cover - environment dependent
            sd = None
        self._sd = sd

    async def play_wav_bytes(self, wav_bytes: bytes) -> None:
        with wave.open(BytesIO(wav_bytes), "rb") as wav:
            channels = wav.getnchannels()
            sample_rate = wav.getframerate()
            audio = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16)
            if channels > 1:
                audio = audio.reshape(-1, channels)

        if self._sd is None:  # pragma: no cover - environment dependent
            logger.info("sounddevice unavailable, skipping audio playback")
            return

        logger.debug("audio_out.play frames=%d sample_rate=%d", len(audio), sample_rate)
        self._sd.play(audio, sample_rate)
        self._sd.wait()
