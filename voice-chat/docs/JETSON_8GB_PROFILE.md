# Jetson 8GB Runtime Profile

Last verified date: 2026-07-03
Target hardware: Jetson class device with 8GB unified memory

## Purpose

This profile is for running `voice-chat` as a lightweight voice endpoint on Jetson while offloading heavy model inference (agent/S2S) to a remote GPU server.

## Profile Name

Set:

```bash
VOICECHAT_RUNTIME_PROFILE=jetson_8gb
```

## Recommended Settings

- `VOICECHAT_STT_BACKEND=whisper_cpp`
- `VOICECHAT_STT_MODEL=tiny.en-q5_1`
- `VOICECHAT_TTS_BACKEND=piper`
- `VOICECHAT_SAMPLE_RATE_HZ=16000`
- `VOICECHAT_AUDIO_FRAME_MS=20`
- `VOICECHAT_TTS_CHUNK_CHARS=120`
- `VOICECHAT_MAX_INFLIGHT_REQUESTS=1`

## Resource Limits (Operational Guidance)

- Keep RAM headroom of at least 1.5GB free for OS/audio/network stability.
- Avoid running large local speech-to-speech models on 8GB for production-like latency.
- Keep only one in-flight query path per session (`MAX_INFLIGHT_REQUESTS=1`).
- Prefer small quantized STT models and low-overhead local TTS.
- Offload heavy agent reasoning and S2S to desktop/server GPU over LAN.

## Quick Start Example

```bash
cp .env.example .env
```

Edit `.env`:

```bash
VOICECHAT_RUNTIME_PROFILE=jetson_8gb
VOICECHAT_AGENT_BASE_URL=http://<windows-gpu-host-ip>:8001
VOICECHAT_DEBUG=1
```

Run:

```bash
voicechat run-app --agent-base-url http://<windows-gpu-host-ip>:8001 --debug
```

Preset file workflow:

```bash
set -a
source config/jetson-8gb.env
set +a
voicechat run-app --profile jetson_8gb --agent-base-url "$VOICECHAT_AGENT_BASE_URL" --debug
```

## Notes

- This profile sets runtime defaults in `voicechat.config.AppConfig`.
- `--profile jetson_8gb` sets `VOICECHAT_RUNTIME_PROFILE` for the current run.
- Any explicit environment variable overrides profile defaults.
- For Bluetooth headset validation on Jetson, run in host mode instead of Docker.
