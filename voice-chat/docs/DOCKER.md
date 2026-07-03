# Docker and Compose

Last verified date: 2026-07-03
Tested OS: macOS

## Build

```bash
docker build -t voicechat:local .
```

## Compose Up

```bash
docker compose up --build
```

Services:

- `mock-agent`: FastAPI mock endpoint on port `8001`
- `voice-app`: interactive app container

## Notes for macOS Audio

- Docker on macOS does not provide simple direct Bluetooth audio passthrough for this workflow.
- Use container mode for service plumbing and integration.
- Use host local mode (`voicechat run-app`) for Bluetooth headset audio validation.
