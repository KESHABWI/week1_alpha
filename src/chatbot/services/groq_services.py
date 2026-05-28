import json
import logging

from httpx import RequestError, HTTPStatusError
from pydantic import ValidationError

from src.chatbot.clients.httpx_client import httpx_client
from src.chatbot.config.settings import settings
from src.chatbot.schemas.llm_schema import GroqRequest

logger = logging.getLogger(__name__)


class GroqRateLimitError(Exception):
    """Raised when Groq returns HTTP 429"""


async def call_llm_groq(prompt: str) -> str:
    """
    Streaming Groq LLM call (prints tokens live + returns full response)
    """

    # ------------------ VALIDATION ------------------
    try:
        payload_dict = {
            "model": settings.GROQ_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": settings.temperature,
            "max_tokens": settings.max_tokens,
            "stream": True,
        }

        payload = GroqRequest(**payload_dict)

    except ValidationError as e:
        logger.exception("Groq request validation failed")
        raise Exception(f"Validation error: {e}")

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    logger.debug("Sending Groq streaming request...")

    full_response = ""

    # ------------------ STREAM REQUEST ------------------
    try:
        async with httpx_client.stream(
            "POST",
            settings.GROQ_URL,
            json=payload.model_dump(),
            headers=headers,
        ) as response:

            # Rate limit check
            if response.status_code == 429:
                raise GroqRateLimitError("Groq rate limit reached")

            response.raise_for_status()

            # ------------------ STREAM LINES ------------------
            async for line in response.aiter_lines():

                if not line:
                    continue

                # DEBUG (VERY IMPORTANT)
                # print("RAW:", line)

                if line.startswith("data: "):
                    data_str = line.removeprefix("data: ")

                    if data_str == "[DONE]":
                        break

                    try:
                        data = json.loads(data_str)

                        # SAFE extraction (Groq/OpenAI variants)
                        choice = data.get("choices", [{}])[0]

                        delta = (
                            choice.get("delta", {}).get("content")
                            or choice.get("message", {}).get("content")
                            or ""
                        )

                        if delta:
                            full_response += delta

                            # 🔥 LIVE CLI OUTPUT
                            print(delta, end="", flush=True)

                    except json.JSONDecodeError:
                        logger.warning("Bad JSON chunk: %s", line)

        return full_response

    except RequestError as e:
        logger.exception("Network error")
        raise Exception(f"Network error: {e}")

    except HTTPStatusError as e:
        logger.exception("HTTP error")
        raise Exception(f"HTTP error: {e}")