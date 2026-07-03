from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="VoiceChat Mock Agent", version="0.1.0")


class AgentRequest(BaseModel):
    session_id: str
    text: str
    timestamp: str


class AgentResponse(BaseModel):
    reply_text: str


@app.post("/agent/respond", response_model=AgentResponse)
async def agent_respond(req: AgentRequest) -> AgentResponse:
    # Mock behavior keeps v1 deterministic for test and integration wiring.
    return AgentResponse(reply_text=f"Mock agent reply: {req.text}")


def run() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
