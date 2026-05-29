from pydantic import BaseModel, Field
from typing import Optional, Annotated


class LLMResponse(BaseModel):
    """Schema for LLM responses, including provider name, response content, and optional latency information."""
    provider: str
    response: str
    latency_ms: Optional[float] = None


class UserInput(BaseModel):
    """Schema for validating user input prompts"""
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


class Message(BaseModel):
    """Schema for individual messages in the conversation history, used in LLM requests"""
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)


class GroqRequest(BaseModel):
    """Schema for Groq LLM request payload with validation rules"""
    model: str = Field(..., min_length=1)
    messages: list[Message] = Field(..., min_length=1)
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=2000, gt=0)
    stream: bool = True


class GeminiPart(BaseModel):
    """Schema for individual parts of Gemini content, which can be text or other 
    types in more complex implementations. For now, we only support text parts."""
    text: str = Field(..., min_length=1)


class GeminiContent(BaseModel):
    """Schema for content blocks in Gemini requests."""
    parts: list[GeminiPart] = Field(..., min_length=1)


class GeminiRequest(BaseModel):
    """Schema for Gemini LLM request payload with validation rules. The 'contents' 
    field is a list of GeminiContent, which allows for more complex message structures in the future."""
    contents: list[GeminiContent] = Field(..., min_length=1)


class OllamaRequest(BaseModel):
    """Schema for Ollama LLM request payload with validation rules. Similar to 
    GroqRequest but tailored for Ollama's expected format."""
    model: str = Field(..., min_length=1)
    messages: list[Message] = Field(..., min_length=1)
    stream: bool = False
