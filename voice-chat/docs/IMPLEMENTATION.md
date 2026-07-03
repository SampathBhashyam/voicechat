# Implementation Details

Last verified date: 2026-07-03
Tested OS: macOS

## Key Modules

- `src/voicechat/orchestrator/session.py`
- `src/voicechat/agent/client.py`
- `src/voicechat/adapters/interfaces.py`
- `src/voicechat/adapters/stt.py`
- `src/voicechat/adapters/tts.py`
- `src/voicechat/audio/io.py`
- `src/voicechat/mock_server/app.py`

## Concurrency Model

- `asyncio` driven orchestration.
- TTS playback launched in task context.
- Barge-in calls `cancel_tts_if_playing()` to interrupt playback task.

## Error Handling

- Agent REST errors are surfaced via `httpx` exceptions.
- Playback gracefully no-ops if `sounddevice` is unavailable.
- Optional adapters raise explicit `NotImplementedError` for unfinished runtime wiring.
