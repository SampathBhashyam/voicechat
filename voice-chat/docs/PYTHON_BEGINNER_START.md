# Python Beginner Start Guide

Last verified date: 2026-07-03
Tested OS: macOS (Apple Silicon)

This guide is for first-time Python users.

## 1) Check Python is Installed

Run:

```bash
python3 --version
```

Expected: `Python 3.11` or newer.

If not installed, install Python 3.11+ and rerun the command.

## 2) Go to the Project Folder

```bash
cd /Users/sampath/Dev/VoiceChat/voice-chat
```

## 3) Create a Virtual Environment

A virtual environment keeps project packages isolated from system Python.

```bash
python3 -m venv .venv
```

## 4) Activate the Virtual Environment

```bash
source .venv/bin/activate
```

When active, your shell prompt usually shows `(.venv)`.

## 5) Install Project Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

## 6) Confirm the CLI Is Available

```bash
voicechat --help
```

If `voicechat` is not found, use:

```bash
python -m voicechat.cli.main --help
```

## 7) Run the Mock Agent (Terminal 1)

```bash
voicechat run-mock-agent --host 127.0.0.1 --port 8001
```

## 8) Run the App (Terminal 2)

Open a second terminal, activate `.venv` again, then run:

```bash
voicechat run-app --agent-base-url http://127.0.0.1:8001 --debug
```

Type text into the prompt to simulate STT input and get a mock response.

## 9) Run Tests

```bash
pytest -q
```

## Common Errors

- `No module named ...`
  - Cause: virtual environment not active or install did not complete.
  - Fix: activate `.venv` and rerun install command.
- `voicechat: command not found`
  - Cause: shell not using `.venv` binaries.
  - Fix: run `source .venv/bin/activate` and retry.
- `Connection refused` to `127.0.0.1:8001`
  - Cause: mock agent is not running.
  - Fix: start `voicechat run-mock-agent` in another terminal.

## Deactivate Environment When Done

```bash
deactivate
```
