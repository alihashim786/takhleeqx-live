"""
TakhleeqX Configuration — Centralized settings loaded from environment variables.
Uses Pydantic Settings for validation and type safety.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # OpenAI
    OPENAI_API_KEY: str

    # Creatomate (Video Generation)
    CREATOMATE_API_KEY: str | None = None
    CREATOMATE_TEMPLATE_ID: str | None = None

    # JWT Authentication
    JWT_SECRET: str = "takhleeqx-default-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Database
    DATABASE_URL: str = "sqlite:///./takhleeqx.db"

    # Application
    APP_NAME: str = "TakhleeqX"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True

    # Image generation
    IMAGE_OUTPUT_DIR: str = "generated_images"

    # Email Notifications
    RESEND_API_KEY: str | None = None
    ADMIN_EMAIL: str | None = None

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
