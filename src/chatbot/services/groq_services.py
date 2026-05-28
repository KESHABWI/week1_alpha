import logging
from httpx import RequestError, HTTPStatusError
from pydantic import ValidationError

from src.chatbot.clients.httpx_client import httpx_client
from src.chatbot.config.settings import settings
from src.chatbot.schemas.llm_schema import GroqRequest, Message

logger = logging.getLogger(__name__)


class GroqRateLimitError(Exception):
    """Raised when Groq returns HTTP 429"""

    pass


async def call_llm_groq(prompt: str) -> str:
    try:
        payload_dict = {
            "model": settings.GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": settings.temperature,
            "max_tokens": settings.max_tokens,
        }
        payload = GroqRequest(**payload_dict)
        logger.debug("Groq request validated: model=%s", payload.model)
    except ValidationError as e:
        logger.exception("Groq request validation failed")
        raise Exception(f"Groq request validation error: {e}")

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    logger.debug(
        "Sending Groq request url=%s model=%s prompt=%s",
        settings.GROQ_URL,
        settings.GROQ_MODEL,
        prompt,
    )

    try:
        response = await httpx_client.post(
            settings.GROQ_URL, json=payload.model_dump(), headers=headers
        )

        logger.debug("Groq response status=%s", response.status_code)

        if response.status_code == 429:
            raise GroqRateLimitError("Groq rate limit reached")

        response.raise_for_status()

        data = response.json()
        logger.debug("Groq response data=%s", data)

        return data["choices"][0]["message"]["content"]

    except RequestError as e:
        logger.exception("Groq network request failed")
        raise Exception(f"Groq network error: {e}")

    except HTTPStatusError as e:
        logger.exception("Groq HTTP error detected")
        raise Exception(f"Groq HTTP error: {e}")
