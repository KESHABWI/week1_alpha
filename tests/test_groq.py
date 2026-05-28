import pytest
from src.chatbot.services.groq_services import call_llm_groq


@pytest.mark.asyncio
async def test_groq_basic():
    prompt = "Hi, write a short sentence starting with 'Hello from Groq!'"
    response = await call_llm_groq(prompt)

    print("\n🔥 Groq Response:\n", response)

    assert isinstance(response, str)
    assert len(response) > 0
