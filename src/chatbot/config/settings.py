from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from functools import lru_cache


class Settings(BaseSettings):
    """Configuration settings for the chatbot application, including API keys, model names, logging configuration, and HTTP client settings. Validates required fields and provides defaults where appropriate."""
    app_name: str = "week1_alpha"

    debug: bool = False

    temperature: float = Field(default=0.7, ge=0, le=2)

    max_tokens: int = Field(default=2000, gt=0)

    LOG_LEVEL: str = "CRITICAL"
    LOG_FILE_PATH: str = "logs/week1_alpha.log"

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

    @field_validator("GROQ_API_KEY", "GEMINI_API_KEY", "OLLAMA_API_KEY")
    @classmethod
    def validate_api_keys(cls, v: str, info) -> str:
        if not v or not v.strip():
            field_name = info.field_name
            raise ValueError(f"{field_name} is missing or empty. Check your .env file.")
        return v

    @field_validator("GROQ_URL", "GEMINI_URL", "OLLAMA_URL")
    @classmethod
    def validate_urls(cls, v: str, info) -> str:
        if not v.startswith(("http://", "https://")):
            field_name = info.field_name
            raise ValueError(f"{field_name} must start with http:// or https://")
        return v


@lru_cache
def get_settings():
    """Get cached settings instance for efficient access across the application."""
    return Settings()


settings = get_settings()
