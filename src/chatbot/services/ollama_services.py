import asyncio
import logging
from ollama import Client
from pydantic import ValidationError

from src.chatbot.config.settings import settings
from src.chatbot.schemas.llm_schema import OllamaRequest

logger = logging.getLogger(__name__)


class OllamaRateLimitError(Exception):
    """Raised when Ollama returns rate limit error"""

    pass


class OllamaAuthError(Exception):
    """Raised when Ollama authentication fails"""

    pass


client = Client(
    host=settings.OLLAMA_URL,
    headers={"Authorization": f"Bearer {settings.OLLAMA_API_KEY}"},
)


async def call_llm_ollama(prompt: str) -> str:
    try:
        payload_dict = {
            "model": settings.OLLAMA_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
        payload = OllamaRequest(**payload_dict)
        logger.debug("Ollama request validated: model=%s", payload.model)
    except ValidationError as e:
        logger.exception("Ollama request validation failed")
        raise Exception(f"Ollama request validation error: {e}")

    logger.debug(
        "Sending Ollama request model=%s prompt=%s",
        settings.OLLAMA_MODEL,
        prompt,
    )

    try:

        def sync_call():
            return client.chat(
                model=settings.OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=False,
            )

        response = await asyncio.to_thread(sync_call)
        logger.debug("Ollama response data=%s", response)

        return response["message"]["content"]

    except Exception as e:
        logger.exception("Ollama request failed")
        error_msg = str(e).lower()

        if "429" in error_msg or "rate limit" in error_msg:
            raise OllamaRateLimitError("Ollama rate limit reached")

        if "401" in error_msg or "unauthorized" in error_msg:
            raise OllamaAuthError("Ollama authentication failed")

        raise Exception(f"Ollama error: {e}")
