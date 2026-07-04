from __future__ import annotations

import argparse
import asyncio
import logging
import os

import uvicorn
from dotenv import load_dotenv

from voicechat.adapters.factory import create_stt_engine, create_tts_engine
from voicechat.agent.client import AgentClient
from voicechat.audio.io import AudioOutput
from voicechat.config import AppConfig
from voicechat.logging_utils import setup_logging
from voicechat.mock_server.app import app as mock_app
from voicechat.orchestrator.session import SessionOrchestrator

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VoiceChat v1 mock app")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_app = sub.add_parser("run-app", help="Run interactive mock voice app")
    run_app.add_argument("--agent-base-url", default=None)
    run_app.add_argument("--session-id", default=None)
    run_app.add_argument(
        "--profile",
        choices=["desktop", "jetson_8gb"],
        default=None,
        help="Runtime profile override (maps to VOICECHAT_RUNTIME_PROFILE).",
    )
    run_app.add_argument("--debug", action="store_true")

    run_server = sub.add_parser("run-mock-agent", help="Run mock agent server")
    run_server.add_argument("--host", default="127.0.0.1")
    run_server.add_argument("--port", type=int, default=8001)

    return parser


async def run_interactive(config: AppConfig) -> None:
    stt = create_stt_engine(config.stt_backend)
    tts = create_tts_engine(config.tts_backend)
    agent = AgentClient(base_url=config.agent_base_url)
    audio_out = AudioOutput()

    orchestrator = SessionOrchestrator(
        stt=stt,
        tts=tts,
        agent_client=agent,
        audio_out=audio_out,
        session_id=config.session_id,
        barge_in_policy=config.barge_in_policy,
    )

    print("VoiceChat mock interactive mode")
    print("Type text to simulate final STT output. Type 'exit' to quit.")

    try:
        while True:
            user_text = await asyncio.to_thread(input, "> ")
            if user_text.strip().lower() in {"exit", "quit"}:
                break
            if not user_text.strip():
                continue
            reply = await orchestrator.handle_transcript(user_text)
            print(f"agent: {reply}")
    finally:
        await orchestrator.shutdown()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.cmd == "run-mock-agent":
        uvicorn.run(mock_app, host=args.host, port=args.port, log_level="info")
        return

    if args.profile:
        os.environ["VOICECHAT_RUNTIME_PROFILE"] = args.profile

    load_dotenv(override=False)
    config = AppConfig.from_env()
    if args.agent_base_url:
        config.agent_base_url = args.agent_base_url
    if args.session_id:
        config.session_id = args.session_id
    config.debug = bool(args.debug or config.debug)

    setup_logging(config.debug)
    logger.info(
        "runtime profile=%s stt_backend=%s tts_backend=%s agent_base_url=%s",
        config.runtime_profile,
        config.stt_backend,
        config.tts_backend,
        config.agent_base_url,
    )
    asyncio.run(run_interactive(config))


if __name__ == "__main__":
    main()
