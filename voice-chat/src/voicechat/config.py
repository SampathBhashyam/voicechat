from __future__ import annotations

import os
from dataclasses import dataclass

_PROFILE_DEFAULTS: dict[str, dict[str, str]] = {
    "desktop": {
        "stt_backend": "mock",
        "stt_model": "small",
        "tts_backend": "mock",
        "sample_rate_hz": "16000",
        "audio_frame_ms": "20",
        "tts_chunk_chars": "180",
        "max_inflight_requests": "2",
    },
    "jetson_8gb": {
        "stt_backend": "mock",
        "stt_model": "tiny.en-q5_1",
        "tts_backend": "mock",
        "sample_rate_hz": "16000",
        "audio_frame_ms": "20",
        "tts_chunk_chars": "120",
        "max_inflight_requests": "1",
    },
}


@dataclass(slots=True)
class AppConfig:
    agent_base_url: str = "http://127.0.0.1:8001"
    session_id: str = "local-session"
    barge_in_policy: str = "stop"
    runtime_profile: str = "desktop"
    stt_backend: str = "mock"
    stt_model: str = "small"
    tts_backend: str = "mock"
    sample_rate_hz: int = 16000
    audio_frame_ms: int = 20
    tts_chunk_chars: int = 180
    max_inflight_requests: int = 2
    debug: bool = False

    @classmethod
    def from_env(cls) -> "AppConfig":
        runtime_profile = os.getenv("VOICECHAT_RUNTIME_PROFILE", "desktop")
        defaults = _PROFILE_DEFAULTS.get(runtime_profile, _PROFILE_DEFAULTS["desktop"])

        return cls(
            agent_base_url=os.getenv("VOICECHAT_AGENT_BASE_URL", "http://127.0.0.1:8001"),
            session_id=os.getenv("VOICECHAT_SESSION_ID", "local-session"),
            barge_in_policy=os.getenv("VOICECHAT_BARGE_IN_POLICY", "stop"),
            runtime_profile=runtime_profile,
            stt_backend=os.getenv("VOICECHAT_STT_BACKEND", defaults["stt_backend"]),
            stt_model=os.getenv("VOICECHAT_STT_MODEL", defaults["stt_model"]),
            tts_backend=os.getenv("VOICECHAT_TTS_BACKEND", defaults["tts_backend"]),
            sample_rate_hz=int(os.getenv("VOICECHAT_SAMPLE_RATE_HZ", defaults["sample_rate_hz"])),
            audio_frame_ms=int(os.getenv("VOICECHAT_AUDIO_FRAME_MS", defaults["audio_frame_ms"])),
            tts_chunk_chars=int(os.getenv("VOICECHAT_TTS_CHUNK_CHARS", defaults["tts_chunk_chars"])),
            max_inflight_requests=int(
                os.getenv("VOICECHAT_MAX_INFLIGHT_REQUESTS", defaults["max_inflight_requests"])
            ),
            debug=os.getenv("VOICECHAT_DEBUG", "0") in {"1", "true", "TRUE"},
        )
