from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class TranscriptEvent:
    text: str
    is_final: bool


class STTEngine(Protocol):
    async def transcribe(self, audio_chunk: bytes) -> list[TranscriptEvent]:
        ...


class TTSEngine(Protocol):
    async def synthesize(self, text: str) -> bytes:
        ...
