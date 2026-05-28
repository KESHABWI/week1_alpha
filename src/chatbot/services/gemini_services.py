import logging
from httpx import RequestError, HTTPStatusError
from pydantic import ValidationError

from src.chatbot.clients.httpx_client import httpx_client
from src.chatbot.config.settings import settings
from src.chatbot.schemas.llm_schema import GeminiRequest, GeminiContent, GeminiPart

logger = logging.getLogger(__name__)


class GeminiRateLimitError(Exception):
    """Raised when Gemini returns HTTP 429"""

    pass


async def call_llm_gemini(prompt: str) -> str:
    try:
        payload_dict = {"contents": [{"parts": [{"text": prompt}]}]}
        payload = GeminiRequest(**payload_dict)
        logger.debug("Gemini request validated")
    except ValidationError as e:
        logger.exception("Gemini request validation failed")
        raise Exception(f"Gemini request validation error: {e}")

    url = f"{settings.GEMINI_URL}/models/{settings.GEMINI_MODEL}:generateContent"

    headers = {
        "x-goog-api-key": settings.GEMINI_API_KEY,
        "Content-Type": "application/json",
    }

    logger.debug(
        "Sending Gemini request url=%s model=%s prompt=%s",
        url,
        settings.GEMINI_MODEL,
        prompt,
    )

    try:
        response = await httpx_client.post(url, json=payload.model_dump(), headers=headers)
        logger.debug("Gemini response status=%s", response.status_code)

        if response.status_code == 429:
            raise GeminiRateLimitError("Gemini rate limit reached")

        response.raise_for_status()

        data = response.json()
        logger.debug("Gemini response data=%s", data)

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except RequestError as e:
        logger.exception("Gemini network request failed")
        raise Exception(f"Gemini network error: {e}")

    except HTTPStatusError as e:
        logger.exception("Gemini HTTP error detected")
        raise Exception(f"Gemini HTTP error: {e}")
