"""
NEO Online Judge - Application Settings
Centralized configuration management using environment variables.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


class Settings:
    """Application settings loaded from environment variables."""

    # === Firebase ===
    CRED_PATH: str = os.getenv("CRED_PATH", "service-account.json")
    DB_URL: str = os.getenv("DB_URL", "")

    # === OpenAI / AI ===
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-4o-mini")
    AI_TEMPERATURE: float = float(os.getenv("AI_TEMPERATURE", "0.7"))
    AI_MAX_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", "1000"))
    AI_TIMEOUT: int = int(os.getenv("AI_TIMEOUT", "20"))

    # === Judge Engine ===
    JUDGE_TIMEOUT: int = int(os.getenv("JUDGE_TIMEOUT", "3"))
    POLL_INTERVAL: float = float(os.getenv("POLL_INTERVAL", "1.5"))
    MAX_SUBMISSIONS_PER_MIN: int = int(os.getenv("MAX_SUBMISSIONS_PER_MIN", "10"))

    # === Redis (optional queue) ===
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    USE_QUEUE: bool = os.getenv("USE_QUEUE", "false").lower() == "true"

    # === Logging ===
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")  # "json" or "text"

    # === Server ===
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "5000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # === Authentication ===
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "neo-judge-secret-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = int(os.getenv("JWT_EXPIRY_HOURS", "24"))

    # === OAuth Providers ===
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "AIzaSyAQ79PPCmufVgJ312WxRXkFNG4rBb322SU")
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")


settings = Settings()
