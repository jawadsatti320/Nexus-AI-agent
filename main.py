from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import asyncio
import json

from agent import NexusAgent
from tools import get_all_tools

app = FastAPI(title="Nexus LLM Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = NexusAgent(tools=get_all_tools())


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    stream: Optional[bool] = False


class ChatResponse(BaseModel):
    response: str
    tool_calls: list
    conversation_id: str
    tokens_used: int


@app.get("/")
async def root():
    return {"status": "Nexus Agent is running", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy", "tools_available": agent.get_tool_names()}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await agent.run(
            message=request.message,
            conversation_id=request.conversation_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def event_generator():
        async for chunk in agent.run_stream(
            message=request.message,
            conversation_id=request.conversation_id
        ):
            yield f"data: {json.dumps(chunk)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


@app.delete("/conversation/{conversation_id}")
async def clear_conversation(conversation_id: str):
    agent.clear_conversation(conversation_id)
    return {"message": "Conversation cleared"}


@app.get("/tools")
async def list_tools():
    return {"tools": agent.get_tool_names()}
