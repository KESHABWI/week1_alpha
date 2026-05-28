import asyncio
from ollama import Client

from src.config.settings import settings


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

        def sync_call():
            return client.chat(
                model=settings.OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=False,
            )

        response = await asyncio.to_thread(sync_call)

        return response["message"]["content"]

    except Exception as e:
        error_msg = str(e).lower()

        # rate limit
        if "429" in error_msg or "rate limit" in error_msg:
            raise OllamaRateLimitError("Ollama rate limit reached")

        # auth error
        if "401" in error_msg or "unauthorized" in error_msg:
            raise OllamaAuthError("Ollama authentication failed")

        raise Exception(f"Ollama error: {e}")
