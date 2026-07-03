# Architecture

Last verified date: 2026-07-03
Tested OS: macOS

## High-Level Flow

`Microphone -> STT -> REST Agent -> TTS -> Headphones`

Current v1 implementation uses mock STT text input to validate orchestration and integration.

## Components

- `SessionOrchestrator`: controls request flow and barge-in cancellation.
- `AgentClient`: sends transcript to `/agent/respond`.
- `STTEngine` interface: pluggable STT adapters.
- `TTSEngine` interface: pluggable TTS adapters.
- `AudioOutput`: WAV playback abstraction.
- `mock_server`: FastAPI endpoint returning deterministic mock replies.

## Duplex/Barge-In

- On new transcript while TTS task is active, orchestrator applies policy (`stop` default).
- Active TTS task is cancelled before issuing the next agent call.
