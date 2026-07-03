# VoiceChat Implementation Checklist

Last updated: 2026-07-03 (America/Chicago)

Status legend: `[ ]` pending, `[~]` in progress, `[x]` done, `[!]` blocked

## 1) Project Setup

- [x] Create repository structure for app, docs, tests, and config files.
- [x] Add Python packaging/dependency files.
- [x] Add environment variable template and runtime configuration defaults.

## 2) Core App Implementation

- [x] Implement audio input/output abstraction for duplex operation.
- [x] Implement VAD gate for speech start/stop detection.
- [x] Implement STT adapter interface and default adapter.
- [x] Implement mock agent REST client.
- [x] Implement TTS adapter interface and default adapter.
- [x] Implement session orchestrator with barge-in interruption handling.
- [x] Implement CLI entrypoint and command-line options.

## 3) Mock Agent Service

- [x] Implement FastAPI mock endpoint: `POST /agent/respond`.
- [x] Add mock service startup command and local validation.

## 4) Documentation

- [x] Create root `README.md`.
- [x] Create `docs/ARCHITECTURE.md`.
- [x] Create `docs/IMPLEMENTATION.md`.
- [x] Create `docs/FRAMEWORKS.md` with official framework links.
- [x] Create `docs/BUILD_AND_RUN.md`.
- [x] Create `docs/DOCKER.md`.
- [x] Create `docs/DEBUGGING.md`.

## 5) Containerization and Debugging

- [x] Add `Dockerfile`.
- [x] Add `docker-compose.yml` for `voice-app` and `mock-agent`.
- [x] Add `.vscode/launch.json` debug profile with breakpoint workflow.

## 6) Testing and Verification

- [x] Add unit tests for orchestrator and adapters.
- [x] Add integration test for `STT stub -> REST mock -> TTS stub`.
- [!] Run test suite and capture results.
- [!] Run local app smoke test path and capture results.

## 7) Spec Compliance and Closure

- [x] Verify deliverables against `SPEC.md` sections 14-19.
- [x] Update this checklist with completion notes.

## Completion Notes

- Completed scaffolding and implementation for v1 mock-first architecture.
- Added all requested docs, Docker/Compose files, and VS Code debug profile.
- Added `jetson_8gb` runtime profile defaults in app config and docs.
- Added `config/jetson-8gb.env` preset and CLI `--profile` switch.
- Performed docs QA pass and added beginner-friendly Python onboarding guide.
- Added unit and integration tests in `tests/`.
- Validation run completed:
- `python3 -m compileall src tests` passed.
- Blocked validations:
- `pytest` execution blocked because dependency install requires network access/approval.
- App smoke run blocked for same reason (`fastapi`/runtime deps missing locally).
