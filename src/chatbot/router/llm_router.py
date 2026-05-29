import logging
import time
import httpx
from pydantic import ValidationError

from chatbot.services.groq_services import call_llm_groq
from chatbot.services.gemini_services import call_llm_gemini
from chatbot.services.ollama_services import call_llm_ollama

from chatbot.schemas.llm_schema import LLMResponse, UserInput

logger = logging.getLogger(__name__)


async def call_llm(prompt: str, provider: str):
    try:
        validated_input = UserInput(prompt=prompt, provider=provider)
        logger.info("User input validated: length=%d", len(validated_input.prompt))
    except ValidationError as e:
        logger.exception("User input validation failed")
        raise Exception(f"Invalid prompt: {e}")

    logger.info("call_llm received prompt")
    start = time.time()

    try:
        result = await call_llm_groq(prompt)
        latency_ms = round((time.time() - start) * 1000, 2)
        logger.info("Groq provided response in %sms", latency_ms)

        return LLMResponse(
            provider="groq",
            response=result,
            latency_ms=latency_ms,
        )

    except (httpx.RequestError, httpx.HTTPError) as exc:
        logger.warning("Groq failed, trying Gemini: %s", exc)
        try:
            result = await call_llm_gemini(prompt)
            latency_ms = round((time.time() - start) * 1000, 2)
            logger.info("Gemini provided response in %sms", latency_ms)

            return LLMResponse(
                provider="gemini",
                response=result,
                latency_ms=latency_ms,
            )

        except Exception as exc2:
            logger.warning("Gemini failed, trying Ollama: %s", exc2)
            result = await call_llm_ollama(prompt)
            latency_ms = round((time.time() - start) * 1000, 2)
            logger.info("Ollama provided response in %sms", latency_ms)

            return LLMResponse(
                provider="ollama",
                response=result,
                latency_ms=latency_ms,
            )
