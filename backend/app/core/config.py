from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "UniNexus AI"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./uninexus.db"
    SECRET_KEY: str = "dev-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()

# Resolve absolute path to project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
