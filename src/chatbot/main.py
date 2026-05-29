# from contextlib import asynccontextmanager

# from fastapi import FastAPI
# from pydantic import BaseModel

# from chatbot.clients.httpx_client import httpx_client
# from chatbot.router.llm_router import call_llm


# @asynccontextmanager
# async def lifespan(app: FastAPI):

#     print("Starting application...")

#     yield

#     print("Closing HTTP client...")

#     await httpx_client.aclose()


# app = FastAPI(title="Week1 Alpha", lifespan=lifespan)


# class ChatRequest(BaseModel):
#     prompt: str

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Chat API"}

# @app.post("/chat")
# async def chat(request: ChatRequest):

#     response = await call_llm(request.prompt)

#     return {"provider_response": response}


import asyncio
import logging
import sys
import argparse
from pydantic import ValidationError

from chatbot.config.logging_config import setup_logging
from chatbot.config.settings import get_settings
from chatbot.router.llm_router import call_llm

logger = logging.getLogger(__name__)

def arg_parse():
    parser =argparse.ArgumentParser(description="LLM Chatbot CLI")

    parser.add_argument("--provider",type=str,choices=["groq","gemini","ollama"],default="groq",help="Select LLM provider to use")
    return parser.parse_args()

def validate_configuration() -> bool:
    """Validate application configuration at startup."""
    try:
        get_settings()
        logger.info("Configuration validated successfully")
        return True
    except ValidationError as e:
        print("\n❌ Configuration Error:")
        for error in e.errors():
            field = error.get("loc", ("unknown",))[0]
            msg = error.get("msg", "Unknown error")
            print(f"  - {field}: {msg}")
        print("\nPlease check your .env file and try again.\n")
        logger.exception("Configuration validation failed")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error during configuration: {e}\n")
        logger.exception("Unexpected configuration error")
        return False


async def chat_loop(provider: str) -> None:
    logger.info("Starting LLM chat loop")
    print("\n--- Alpha LLM Chat ---")
    print('Type "exit" to quit')

    history = []

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            logger.info("Exiting LLM chat loop")
            print("Goodbye, Have a nice day")
            break

        history.append({"role": "user", "content": user_input})

        logger.info("Received user prompt: %s", user_input)
        try:
            print("AI: ", end="", flush=True)
            AI_response = await call_llm(str(history), provider=provider)
            history.append({"role": "AI", "content": AI_response.response})
            print()  # Newline after streaming completes
            logger.info(
                "Responding with provider=%s latency_ms=%s",
                AI_response.provider,
                AI_response.latency_ms,
            )
        except ValueError as e:
            logger.exception("Validation error")
            print(
                f"\n❌ Validation Error: {e}\nPlease check your input and try again.\n"
            )
        except Exception as e:
            logger.exception("Error during API call")
            print(f"\n❌ Error: {e}\nPlease try again.\n")


if __name__ == "__main__":
    setup_logging()

    args = arg_parse()
    provider = args.provider
    logger.info("Selected LLM provider: %s", provider)
    print(f"Selected provider: {provider}")

    if not validate_configuration():
        sys.exit(1)

    asyncio.run(chat_loop(provider))
