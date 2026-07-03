# Debugging

Last verified date: 2026-07-03
Tested OS: macOS + VS Code Python extension

## VS Code Debug Profiles

Profiles are in `.vscode/launch.json`:

- `VoiceChat: Run Mock Agent`
- `VoiceChat: Run App (Mock)`

## Breakpoint Workflow

1. Set breakpoint in `src/voicechat/orchestrator/session.py` inside `handle_transcript`.
2. Start `VoiceChat: Run Mock Agent`.
3. Start `VoiceChat: Run App (Mock)`.
4. Enter text in terminal prompt.
5. Debugger should stop at breakpoint before REST call or TTS task creation.

## Troubleshooting

- If imports fail, select project venv interpreter in VS Code.
- If REST connection fails, verify mock agent is running on `127.0.0.1:8001`.
- If breakpoints are not hit, ensure you started the app via a VS Code launch profile (not an external shell process).
