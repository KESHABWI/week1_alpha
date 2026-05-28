import time
import httpx

from src.services.groq_services import call_llm_groq
from src.services.gemini_services import call_llm_gemini
from src.services.ollama_services import call_llm_ollama

from src.schemas.llm_schema import LLMResponse


async def call_llm(prompt: str):

    start = time.time()

    try:
        result = await call_llm_groq(prompt)

        return LLMResponse(
            provider="groq",
            response=result,
            latency_ms=round((time.time() - start) * 1000, 2),
        )

    except (httpx.RequestError, httpx.HTTPError):
        try:
            result = await call_llm_gemini(prompt)

            return LLMResponse(
                provider="gemini",
                response=result,
                latency_ms=round((time.time() - start) * 1000, 2),
            )

        except Exception:
            result = await call_llm_ollama(prompt)

            return LLMResponse(
                provider="ollama",
                response=result,
                latency_ms=round((time.time() - start) * 1000, 2),
            )
