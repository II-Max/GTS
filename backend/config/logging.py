"""
NEO Online Judge - Logging Configuration
Structured logging with JSON format, rotating files, and console output.
"""

import os
import sys
import logging
import logging.config as log_config
from datetime import datetime
from pathlib import Path

from backend.config.settings import settings


def setup_logging() -> logging.Logger:
    """Configure and return the application logger."""
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y%m%d")

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(filename)s %(lineno)d",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
                "formatter": "standard",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": logging.DEBUG,
                "formatter": "json" if settings.LOG_FORMAT == "json" else "detailed",
                "filename": str(log_dir / f"judge_{today}.log"),
                "maxBytes": 10_485_760,  # 10 MB
                "backupCount": 10,
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": logging.ERROR,
                "formatter": "detailed",
                "filename": str(log_dir / f"errors_{today}.log"),
                "maxBytes": 10_485_760,
                "backupCount": 5,
            },
        },
        "loggers": {
            "neo": {
                "level": "DEBUG",
                "handlers": ["console", "file", "error_file"],
                "propagate": False,
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
    }

    log_config.dictConfig(config)
    return logging.getLogger("neo")
