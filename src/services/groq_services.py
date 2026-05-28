from httpx import RequestError, HTTPStatusError

from src.clients.httpx_client import httpx_client
from src.config.settings import settings


class GroqRateLimitError(Exception):
    """Raised when Groq returns HTTP 429"""

    pass


async def call_llm_groq(prompt: str) -> str:

    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
    }

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = await httpx_client.post(
            settings.GROQ_URL, json=payload, headers=headers
        )

        # handle rate limit explicitly
        if response.status_code == 429:
            raise GroqRateLimitError("Groq rate limit reached")

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except RequestError as e:
        # network-level issue (DNS, timeout, connection)
        raise Exception(f"Groq network error: {e}")

    except HTTPStatusError as e:
        # 4xx/5xx HTTP errors (except 429 handled above)
        raise Exception(f"Groq HTTP error: {e}")
