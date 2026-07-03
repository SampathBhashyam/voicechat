# Moshi S2S Extension Test Project

Last verified: 2026-07-03

This extension project packages a **Moshi (Kyutai Labs) speech-to-speech test stack** for GPU execution on your Windows desktop (NVIDIA 32GB VRAM) using Docker.

## What this project contains

- `Dockerfile`: GPU-ready image for Moshi server runtime.
- `docker-compose.gpu.yml`: starts a Moshi server container with NVIDIA GPU access.
- `.env.example`: runtime environment template.
- `scripts/run-local.sh`: local convenience wrapper.
- `MOSHI_S2S_CHECKLIST.md`: live project task checklist.

## Intended runtime target

- Host: Windows desktop with NVIDIA GPU (32GB VRAM)
- Container runtime: Docker Desktop + NVIDIA GPU support

## Prerequisites (Windows host)

1. Install Docker Desktop with WSL2 backend.
2. Install recent NVIDIA GPU driver.
3. Confirm Docker GPU visibility:

```bash
docker run --rm --gpus all nvidia/cuda:12.4.1-runtime-ubuntu22.04 nvidia-smi
```

## Quick start

1. Copy env file:

```bash
cp .env.example .env
```

2. Set your Hugging Face token in `.env` if model access is gated.

3. Build and run:

```bash
docker compose -f docker-compose.gpu.yml up --build
```

4. Check logs:

```bash
docker compose -f docker-compose.gpu.yml logs -f moshi-server
```

## Notes

- This project is intentionally isolated from the main app so we can benchmark S2S feasibility separately.
- macOS M4 Air local execution is not the target path here; use your Windows GPU host for realistic testing.
- First model download can be large and slow.

## Next integration step

After this server is stable, wire the main `VoiceChat` app to call this S2S service endpoint over LAN.
