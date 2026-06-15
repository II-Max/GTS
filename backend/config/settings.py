"""
GTS (Go to Success) - Application Settings
Centralized configuration management using environment variables.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


class Settings:
    """Application settings loaded from environment variables."""

    # === Firebase ===
    CRED_PATH: str = str(BASE_DIR / os.getenv("CRED_PATH", "service-account.json"))
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
    LOG_DIR: str = str(BASE_DIR / os.getenv("LOG_DIR", "logs"))
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")  # "json" or "text"

    # === AI (DeepSeek - uu tien) ===
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # === AI (Grok - xAI) ===
    GROK_API_KEY: str = os.getenv("GROK_API_KEY", "")

    # === Server ===
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "5000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # CORS: thu hep mac dinh, chi cho phep domain production va localhost
    _raw_origins = os.getenv("ALLOWED_ORIGINS", "")
    ALLOWED_ORIGINS: list = (
        [o.strip() for o in _raw_origins.split(",") if o.strip()]
        if _raw_origins
        else [
            "https://gtsv2-a93c5.web.app",
            "https://gtsv2-a93c5.firebaseapp.com",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]
    )

    # === Authentication ===
    # QUAN TRONG: Phai set JWT_SECRET_KEY trong .env — khong duoc dung gia tri mac dinh
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = int(os.getenv("JWT_EXPIRY_HOURS", "24"))

    # === OAuth Providers ===
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")

    def __init__(self):
        if not self.JWT_SECRET_KEY:
            import secrets
            import logging
            self.JWT_SECRET_KEY = secrets.token_hex(32)
            logging.getLogger("neo").warning(
                "JWT_SECRET_KEY chua duoc set trong .env! "
                "Da tao key ngau nhien — JWT tokens se het han khi server restart. "
                "Hay them JWT_SECRET_KEY=<your-secret> vao file .env ngay!"
            )

        if not self.DB_URL:
            import logging
            logging.getLogger("neo").warning("DB_URL chua duoc set trong .env!")


settings = Settings()
