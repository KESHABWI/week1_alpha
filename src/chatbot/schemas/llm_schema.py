from pydantic import BaseModel, Field
from typing import Literal, Optional, Annotated


class LLMResponse(BaseModel):
    provider: str
    response: str
    latency_ms: Optional[float] = None


class UserInput(BaseModel):
    prompt: Annotated[
        str,
        Field(
            ...,
            description="The prompt to send to the LLM",
            json_schema_extra={"example": "What is the capital of France?"},
            min_length=1,
            max_length=10000,
        ),
    ]
    provider: Literal["groq", "gemini", "ollama"]


class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)


class GroqRequest(BaseModel):
    model: str = Field(..., min_length=1)
    messages: list[Message] = Field(..., min_length=1)
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=2000, gt=0)
    stream: bool = True


class GeminiPart(BaseModel):
    text: str = Field(..., min_length=1)


class GeminiContent(BaseModel):
    parts: list[GeminiPart] = Field(..., min_length=1)


class GeminiRequest(BaseModel):
    contents: list[GeminiContent] = Field(..., min_length=1)


class OllamaRequest(BaseModel):
    model: str = Field(..., min_length=1)
    messages: list[Message] = Field(..., min_length=1)
    stream: bool = False
