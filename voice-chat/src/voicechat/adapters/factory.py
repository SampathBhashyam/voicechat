from __future__ import annotations

from voicechat.adapters.interfaces import STTEngine, TTSEngine
from voicechat.adapters.stt import MockSTTEngine
from voicechat.adapters.tts import MockTTSEngine


def create_stt_engine(backend: str) -> STTEngine:
    if backend == "mock":
        return MockSTTEngine()
    raise ValueError(
        f"Unsupported STT backend '{backend}' in current build. "
        "Supported backends: mock"
    )


def create_tts_engine(backend: str) -> TTSEngine:
    if backend == "mock":
        return MockTTSEngine()
    raise ValueError(
        f"Unsupported TTS backend '{backend}' in current build. "
        "Supported backends: mock"
    )
