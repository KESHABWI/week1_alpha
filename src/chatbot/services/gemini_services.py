import json
import logging
from httpx import RequestError, HTTPStatusError
from pydantic import ValidationError

from chatbot.clients.httpx_client import httpx_client
from chatbot.config.settings import settings
from chatbot.schemas.llm_schema import GeminiRequest, GeminiContent, GeminiPart

logger = logging.getLogger(__name__)


class GeminiRateLimitError(Exception):
    """Raised when Gemini returns HTTP 429"""

    pass


async def call_llm_gemini(prompt: str) -> str:  
    try:
        payload = GeminiRequest(
            contents=[
                GeminiContent(
                    parts=[
                        GeminiPart(text=prompt)
                    ]
                )
            ]
        )
        logger.debug("Gemini request validated")
    except ValidationError as e:
        logger.exception("Gemini request validation failed")
        raise Exception(f"Gemini request validation error: {e}")

    url = f"{settings.GEMINI_URL}/models/{settings.GEMINI_MODEL}:streamGenerateContent?alt=sse"

    headers = {
        "x-goog-api-key": settings.GEMINI_API_KEY,
        "Content-Type": "application/json",
    }

    logger.debug(
        "Sending Gemini streaming request url=%s model=%s prompt=%s",
        url,
        settings.GEMINI_MODEL,
        prompt,
    )

    full_response = ""

    try:
        async with httpx_client.stream(
            "POST",
            url,
            json=payload.model_dump(),
            headers=headers,
        ) as response:
            if response.status_code == 429:
                raise GeminiRateLimitError("Gemini rate limit reached")

            response.raise_for_status()

            async for line in response.aiter_lines():
                if not line:
                    continue

                if line.startswith("data: "):
                    data_str = line.removeprefix("data: ")

                    try:
                        data = json.loads(data_str)
                        candidates = data.get("candidates", [{}])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [{}])
                            if parts:
                                delta = parts[0].get("text", "")
                                if delta:
                                    full_response += delta
                                    print(delta, end="", flush=True)
                    except json.JSONDecodeError:
                        logger.warning("Bad JSON chunk: %s", line)

        return full_response

    except RequestError as e:
        logger.exception("Gemini network request failed")
        raise Exception(f"Gemini network error: {e}")

    except HTTPStatusError as e:
        logger.exception("Gemini HTTP error detected")
        raise Exception(f"Gemini HTTP error: {e}")
