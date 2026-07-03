# Moshi S2S Extension Checklist

Last updated: 2026-07-03 (America/Chicago)

Status legend: `[ ]` pending, `[~]` in progress, `[x]` done, `[!]` blocked

## 1) Project Scaffolding

- [x] Create isolated extension project directory under `extensions/`.
- [x] Add project README with target host and run workflow.

## 2) Docker Packaging

- [x] Add GPU-ready Dockerfile for Moshi runtime.
- [x] Add runtime startup script for `moshi.server`.
- [x] Add `.env.example` for model repo and token config.

## 3) Compose Orchestration

- [x] Add `docker-compose.gpu.yml` with NVIDIA GPU reservation.
- [x] Expose service ports and environment-driven runtime configuration.

## 4) Verification

- [x] Validate file structure and command syntax consistency.
- [!] Build Docker image locally.
- [!] Start Moshi container and confirm server boot logs.
- [!] Run functional S2S request test against running container.

## 5) Integration Readiness

- [x] Document next step to wire VoiceChat app to Moshi endpoint.

## Notes

- Build/run verification steps are blocked in this environment because Docker runtime and external model downloads are not available here.
- Local validation completed:
- `bash -n scripts/run-local.sh` passed.
- `docker compose -f docker-compose.gpu.yml config` passed after creating `.env` from `.env.example`.
