import pytest
from src.chatbot.services.ollama_services import call_llm_ollama


@pytest.mark.asyncio
async def test_ollama_basic():

    prompt = "Hi, write a short poem about AI"

    response = await call_llm_ollama(prompt)

    print("\n🧠 Ollama Response:\n", response)

    assert isinstance(response, str)
    assert len(response) > 0
