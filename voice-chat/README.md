# VoiceChat

Last verified date: 2026-07-03
Tested OS: macOS (Apple Silicon)

VoiceChat is a lightweight Python app that provides a full-duplex voice-layer scaffold:

- STT -> REST agent -> TTS
- Barge-in interruption policy
- Mock-first local development path
- Containerized mock services and VS Code debugging support

## Quick Start

New to Python? Start here first: [Python Beginner Start Guide](docs/PYTHON_BEGINNER_START.md)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

Start mock agent:

```bash
voicechat run-mock-agent --host 127.0.0.1 --port 8001
```

In another terminal:

```bash
voicechat run-app --agent-base-url http://127.0.0.1:8001 --debug
```

Type text in the app prompt to simulate finalized STT transcripts.

## Repo Layout

- `src/voicechat/`: app source
- `tests/`: unit and integration tests
- `docs/`: high-level and implementation docs
- `config/`: environment presets (including Jetson profile)
- `.vscode/`: debug launch profiles
- `Dockerfile`, `docker-compose.yml`: container workflows

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Implementation](docs/IMPLEMENTATION.md)
- [Frameworks](docs/FRAMEWORKS.md)
- [Python Beginner Start Guide](docs/PYTHON_BEGINNER_START.md)
- [Build and Run](docs/BUILD_AND_RUN.md)
- [Jetson 8GB Profile](docs/JETSON_8GB_PROFILE.md)
- [Docker](docs/DOCKER.md)
- [Debugging](docs/DEBUGGING.md)

## Known Limitations (v1)

- Real microphone-to-STT streaming is scaffolded; default run path is mock STT input.
- Piper and faster-whisper adapters are boundary stubs, not full runtime integration yet.
- Docker on macOS is for service/runtime plumbing; Bluetooth audio testing should be local host mode.
