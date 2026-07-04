from __future__ import annotations

import pytest

from voicechat.adapters.factory import create_stt_engine, create_tts_engine
from voicechat.adapters.stt import MockSTTEngine
from voicechat.adapters.tts import MockTTSEngine


def test_create_stt_engine_mock() -> None:
    engine = create_stt_engine("mock")
    assert isinstance(engine, MockSTTEngine)


def test_create_tts_engine_mock() -> None:
    engine = create_tts_engine("mock")
    assert isinstance(engine, MockTTSEngine)


@pytest.mark.parametrize("backend", ["whisper_cpp", "piper", "unknown"])
def test_create_stt_engine_unsupported(backend: str) -> None:
    with pytest.raises(ValueError):
        create_stt_engine(backend)


@pytest.mark.parametrize("backend", ["piper", "unknown"])
def test_create_tts_engine_unsupported(backend: str) -> None:
    with pytest.raises(ValueError):
        create_tts_engine(backend)
