from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from src.clients.httpx_client import httpx_client
from src.services.llm_router import call_llm


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting application...")

    yield

    print("Closing HTTP client...")

    await httpx_client.aclose()


app = FastAPI(title="Week1 Alpha", lifespan=lifespan)


class ChatRequest(BaseModel):
    prompt: str


@app.post("/chat")
async def chat(request: ChatRequest):

    response = await call_llm(request.prompt)

    return {"provider_response": response}
