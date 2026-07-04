# Build and Run

Last verified date: 2026-07-03
Tested OS: macOS

If you are new to Python tooling, read this first:
[PYTHON_BEGINNER_START.md](PYTHON_BEGINNER_START.md)

## Prerequisites

- Python 3.11 or newer.
- Terminal access.
- `git` installed if cloning fresh.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Environment

```bash
cp .env.example .env
```

`voicechat run-app` automatically loads `.env` from the project root.

Key variables:

- `VOICECHAT_AGENT_BASE_URL`
- `VOICECHAT_SESSION_ID`
- `VOICECHAT_BARGE_IN_POLICY`
- `VOICECHAT_RUNTIME_PROFILE` (`desktop` or `jetson_8gb`)
- `VOICECHAT_STT_BACKEND`
- `VOICECHAT_STT_MODEL`
- `VOICECHAT_TTS_BACKEND`
- `VOICECHAT_SAMPLE_RATE_HZ`
- `VOICECHAT_AUDIO_FRAME_MS`
- `VOICECHAT_TTS_CHUNK_CHARS`
- `VOICECHAT_MAX_INFLIGHT_REQUESTS`
- `VOICECHAT_DEBUG`

Current backend support in this build:

- STT: `mock`
- TTS: `mock`

## Jetson 8GB Profile Quick Start

Set the runtime profile for low-memory Jetson deployment:

```bash
export VOICECHAT_RUNTIME_PROFILE=jetson_8gb
export VOICECHAT_AGENT_BASE_URL=http://<windows-gpu-host-ip>:8001
```

Then run:

```bash
voicechat run-app --agent-base-url "$VOICECHAT_AGENT_BASE_URL" --debug
```

Using the preset file:

```bash
cp config/jetson-8gb.env .env
voicechat run-app --profile jetson_8gb --debug
```

Detailed tuning guide: [JETSON_8GB_PROFILE.md](JETSON_8GB_PROFILE.md)

## Run Mock Agent

```bash
voicechat run-mock-agent --host 127.0.0.1 --port 8001
```

## Run App

```bash
voicechat run-app --agent-base-url http://127.0.0.1:8001 --debug
```

## Run Tests

```bash
pytest -q
```

## Troubleshooting

- `No module named pytest`:
  - Activate your venv and install dev dependencies with `pip install -e '.[dev]'`.
- `voicechat: command not found`:
  - Use `source .venv/bin/activate`, then retry.
- Cannot connect to mock agent:
  - Confirm `voicechat run-mock-agent` is running on `127.0.0.1:8001`.
