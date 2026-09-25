"""
English: Application settings loaded from .env.
Roman Urdu: .env se load hone wali application settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "UniNexus AI"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./uninexus.db"
    SECRET_KEY: str = "dev-secret-key"

    # English: LLM gateway configuration.
    # Roman Urdu: LLM gateway ki configuration.
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-flash-latest"
    OLLAMA_MODEL: str = "llama3.2:latest"

    # English: Allow extra env vars to be set without failing validation.
    # Roman Urdu: Extra env vars allow karo taake validation fail na ho.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
