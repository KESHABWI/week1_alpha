from httpx import RequestError, HTTPStatusError

from src.clients.httpx_client import httpx_client
from src.config.settings import settings


class GeminiRateLimitError(Exception):
    """Raised when Gemini returns HTTP 429"""

    pass


async def call_llm_gemini(prompt: str) -> str:

    url = f"{settings.GEMINI_URL}/models/{settings.GEMINI_MODEL}:generateContent"

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    headers = {
        "x-goog-api-key": settings.GEMINI_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = await httpx_client.post(url, json=payload, headers=headers)

        # handle rate limit explicitly
        if response.status_code == 429:
            raise GeminiRateLimitError("Gemini rate limit reached")

        response.raise_for_status()

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except RequestError as e:
        raise Exception(f"Gemini network error: {e}")

    except HTTPStatusError as e:
        raise Exception(f"Gemini HTTP error: {e}")
