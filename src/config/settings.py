from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "week1_alpha"

    debug: bool = False

    temperature: float = Field(default=0.7, ge=0, le=2)

    max_tokens: int = Field(default=2000, gt=0)

    HTTP_MAX_CONNECTIONS: int = 100
    HTTP_KEEPALIVE_CONNECTIONS: int = 20

    GROQ_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    GROQ_API_KEY: str
    GROQ_MODEL: str = "openai/gpt-oss-120b"

    GEMINI_URL: str = "https://generativelanguage.googleapis.com/v1beta"
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    OLLAMA_URL: str = "https://ollama.com"
    OLLAMA_API_KEY: str
    OLLAMA_MODEL: str = "gpt-oss:120b"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
