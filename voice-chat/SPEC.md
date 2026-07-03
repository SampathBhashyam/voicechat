# Voice Layer App Spec (v1)

## 1. Document Status

- Status: Draft for review
- Owner: VoiceChat project
- Date: 2026-07-03
- Scope: Python desktop/CLI app on macOS using Bluetooth headphones

## 2. Problem Statement

Build a lightweight, full-duplex voice layer on top of an AI agent:

- Convert user speech to text (STT) using open-source, established frameworks.
- Send text to an agent endpoint over REST (mocked for now).
- Speak the agent response with TTS (open-source).
- Support hands-free interaction through a Bluetooth headset on Mac.

## 3. Goals

- End-to-end loop: `Mic -> STT -> REST agent -> TTS -> Headphones`.
- App can listen while speaking (barge-in capable).
- User speech can interrupt ongoing TTS playback.
- Low-latency, lightweight runtime suitable for local development on macOS.
- Modular architecture so STT/TTS/agent transport can be swapped later.
- Mock-first integration for agent endpoint; production URL to be added later.
- Provide rich, maintainable project documentation in Markdown for users and developers.
- Provide containerized local deployment with Docker and Docker Compose.
- Provide first-class local debugging support through VS Code launch profiles.

## 4. Non-Goals (v1)

- Production auth/security hardening.
- Cloud dependencies for core loop.
- Multi-user sessions.
- Voice biometrics or speaker identification.
- GUI-heavy frontend (CLI-first is acceptable for v1).

## 5. Platform and Constraints

- OS: macOS (developer machine).
- Audio device: Bluetooth headset as default input/output route.
- Language: Python 3.11+.
- Framework preference: open-source, stable, lightweight.
- Must run locally with minimal setup and predictable dependencies.

## 6. Candidate Technical Stack (v1 decision)

- STT: `faster-whisper` (small model default), with pluggable adapter interface.
- TTS: `Piper` (local inference), with pluggable adapter interface.
- Audio I/O: `sounddevice` + `numpy` (streaming capture/playback).
- VAD/barge-in: `webrtcvad`.
- REST client/server: `FastAPI` + `uvicorn` + `httpx`.
- Concurrency: `asyncio` + producer/consumer queues.

Rationale:

- All components are open source and commonly used.
- Practical balance between quality and local runtime footprint.
- Clear migration path if later replaced with other STT/TTS engines.

## 7. High-Level Architecture

Components:

- `AudioInput`: captures microphone frames from Bluetooth device.
- `VADGate`: detects speech start/stop and segmentation.
- `STTEngine`: incremental transcription of active speech segments.
- `AgentClient`: POSTs transcript to REST endpoint (mock for now).
- `TTSEngine`: synthesizes agent text to PCM chunks.
- `AudioOutput`: streams TTS audio to Bluetooth headphones.
- `SessionOrchestrator`: state machine + interruption + cancellation.

Data flow:

1. Mic frames enter `AudioInput`.
2. `VADGate` marks speech boundaries.
3. `STTEngine` emits partial/final text.
4. Final text sent to `AgentClient` via REST.
5. Agent response text streamed/chunked to `TTSEngine`.
6. `AudioOutput` plays chunks while app remains in listening mode.
7. On barge-in, orchestrator cancels/ducks TTS and prioritizes user speech.

## 8. Full-Duplex Requirements

- Duplex mode is always on during active session.
- If user starts speaking while TTS is playing, detect with VAD within target 200 ms.
- If barge-in is detected, stop or duck TTS immediately (configurable policy, default = stop).
- After interruption, start new STT capture without requiring manual reset.
- Prevent feedback loops by defaulting to Bluetooth headset I/O.

## 9. REST Contract (Mock v1)

Request:

- `POST /agent/respond`
- JSON: `{ "session_id": "...", "text": "...", "timestamp": "..." }`

Response (mock v1):

- JSON: `{ "reply_text": "..." }`

Future-ready note:

- Contract should allow streaming/SSE upgrade later without breaking client abstraction.

## 10. Functional Requirements

- Start/stop session from CLI command.
- Select or auto-detect Bluetooth audio devices.
- Show partial STT text in terminal.
- Send final transcript to mock REST endpoint.
- Speak returned text using TTS.
- Allow interruption at any time by user speech.
- Recover from transient errors without process restart where possible.

## 11. Reliability and Performance Targets (v1)

- STT partial latency: < 700 ms from speech chunk.
- End-of-utterance to final text: < 1000 ms.
- REST round-trip (mock local): < 200 ms.
- TTS time-to-first-audio: < 800 ms.
- Barge-in response (speech detected to TTS stop): < 250 ms.
- Crash-free 30-minute continuous session in local testing.

## 12. Observability

- Structured logs for audio device selection.
- Structured logs for STT partial/final events.
- Structured logs for REST request/response timing.
- Structured logs for TTS synthesis/playback timing.
- Structured logs for barge-in/cancellation events.
- Optional `--debug` mode for verbose timing traces.

## 13. Security and Privacy (v1 baseline)

- No persistent raw-audio storage by default.
- Transcripts logged only in debug mode (or redacted).
- Agent endpoint URL and tokens via env vars when production URL is added.

## 14. Deliverables

- Python app source with modular adapters.
- Local mock agent server endpoint.
- CLI runner for end-to-end session.
- Configuration file/template for device + model settings.
- Root `README.md` suitable for Git hosting.
- Full documentation set in Markdown (`docs/*.md`), including architecture and implementation detail.
- Dockerfile(s) and `docker-compose.yml` for local containerized execution.
- VS Code debug configuration (`.vscode/launch.json`) for running the app with breakpoints.

## 15. Execution Plan

1. Finalize and approve this spec.
2. Build skeleton modules and interface contracts.
3. Implement audio capture/playback pipeline.
4. Integrate STT adapter.
5. Add mock REST agent server + client.
6. Integrate TTS adapter and playback queue.
7. Implement full-duplex orchestration and barge-in logic.
8. Add logging, retries, and graceful shutdown.
9. Add Docker and Docker Compose packaging for local run workflows.
10. Add project docs, framework links, and debugging docs.
11. Add VS Code debug profile and verify breakpoint workflow.
12. Run validation tests and record baseline metrics.

## 16. Documentation Requirements (Required)

Required docs:

- `README.md` (root):
- Project purpose, architecture summary, quick start, build/start commands, troubleshooting, known limitations.
- `docs/ARCHITECTURE.md`:
- High-level design, component interactions, state model, duplex/barge-in flow.
- `docs/IMPLEMENTATION.md`:
- Module-by-module implementation details, interfaces, threading/async model, error handling.
- `docs/FRAMEWORKS.md`:
- Framework selection rationale and links to official framework documentation.
- `docs/BUILD_AND_RUN.md`:
- Local Python setup, dependency install, run commands, environment variables.
- `docs/DOCKER.md`:
- Docker image build, Docker Compose usage, logs, rebuild flow.
- `docs/DEBUGGING.md`:
- VS Code debug setup, launch profile usage, attaching breakpoints, common debug scenarios.

Framework links to include in docs:

- faster-whisper: `https://github.com/SYSTRAN/faster-whisper`
- Piper TTS: `https://github.com/rhasspy/piper`
- sounddevice: `https://python-sounddevice.readthedocs.io/`
- webrtcvad (Python): `https://github.com/wiseman/py-webrtcvad`
- FastAPI: `https://fastapi.tiangolo.com/`
- Uvicorn: `https://www.uvicorn.org/`
- HTTPX: `https://www.python-httpx.org/`
- NumPy: `https://numpy.org/`

Documentation quality bar:

- Every setup/run/debug command must be copy/paste ready.
- All assumptions and platform caveats must be explicit.
- Docs must include a "last verified date" and tested OS context.
- Cross-link related docs to reduce duplication.

## 17. Containerization and Runtime Requirements (Required)

- Provide Dockerfile for the app and mock REST server (single or split services).
- Provide `docker-compose.yml` with at least:
- `voice-app` service.
- `mock-agent` service.
- Environment variable wiring for agent URL and app settings.
- Support running mock end-to-end flow via Compose.
- Document host audio constraints on macOS Docker and required fallback behavior.
- Ensure non-container local mode remains supported for Bluetooth headset testing.

## 18. VS Code Debug Requirements (Required)

- Provide `.vscode/launch.json` with debug profile(s) to run app entrypoint.
- Debug profile must support stopping at breakpoints in orchestrator flow.
- Include environment variables and args needed for mock endpoint integration.
- Include one documented sample breakpoint path (for example, barge-in handler).
- Provide debug instructions in `docs/DEBUGGING.md`.

## 19. Review, Fix, and Test Process (Required)

1. Spec review:
   - Conduct structured review against goals, constraints, and latency targets.
   - Collect review comments in a checklist (ambiguity, feasibility, missing edge cases).
2. Spec fixes:
   - Update spec to resolve review comments before implementation starts.
   - Mark each review comment as resolved with a concrete change.
3. Implementation verification:
   - Unit tests for orchestration, adapter interfaces, and error paths.
   - Integration test for full mock pipeline: `audio stub -> STT stub -> REST mock -> TTS stub`.
   - Manual Bluetooth headset test on macOS for duplex and interruption behavior.
   - Documentation review for completeness, accuracy, and command validity.
   - Docker/Compose smoke test for startup and service connectivity.
   - VS Code debug smoke test confirming breakpoints are hit.
4. Exit criteria:
   - All critical review comments resolved.
   - Tests pass.
   - End-to-end demo works locally with mock endpoint.
   - Documentation set is complete and navigable.
   - Containerized startup works as documented.
   - VS Code debug profile works as documented.

## 20. Open Items for Next Revision

- Final production agent URL and auth requirements.
- Streaming response protocol decision (JSON vs SSE/chunked).
- Final STT/TTS model choices after benchmark on target hardware.
- Decision on wake word vs push-to-talk fallback behavior.

## 21. Review Notes and Fixes Applied (2026-07-03)

1. Review comment: Full-duplex bullets were ambiguous and implied manual interpretation.
   - Fix: Rewrote full-duplex requirements into explicit trigger/action statements.
2. Review comment: Logging scope was underspecified.
   - Fix: Converted observability into explicit event-level log requirements.
3. Review comment: Review process did not define acceptance flow clearly.
   - Fix: Converted review/fix/test process into ordered phases with concrete exit criteria.
4. Review comment: Documentation and runtime operations requirements were incomplete.
   - Fix: Added dedicated sections for Markdown docs, framework links, Docker/Compose, and VS Code debugging requirements.
