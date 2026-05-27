from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache
from pydantic import Field

class Settings(BaseSettings):
    app_name: str="week1_alpha"

    debug: bool = False

    temperature: float = Field(
        default=0.7,
        ge=0,
        le=2
    )

    max_tokens: int = Field(
        default=2000,
        gt=0
    )

    GROQ_API_KEY : str
    GROQ_MODEL : str = "openai/gpt-oss-120b"

    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings():
    return Settings()

settings= get_settings()
