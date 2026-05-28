import pytest
from src.chatbot.services.gemini_services import call_llm_gemini


@pytest.mark.asyncio
async def test_gemini_basic():
    prompt = "Hi, respond with exactly 'Hello from Gemini!'"
    response = await call_llm_gemini(prompt)

    print("\n✨ Gemini Response:\n", response)

    assert isinstance(response, str)
    assert len(response) > 0
    assert "Gemini" in response
