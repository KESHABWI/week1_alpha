from pydantic import BaseModel
from typing import Optional


class LLMResponse(BaseModel):
    provider: str
    response: str
    latency_ms: Optional[float] = None
