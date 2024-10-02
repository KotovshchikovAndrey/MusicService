from pydantic import BaseModel

from config.settings import settings


class LoggerConfig(BaseModel):
    version: int = 1
    disable_existing_loggers: bool = False

    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s [%(asctime)s] %(module)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }

    handlers: dict = {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
    }

    loggers: dict = {
        "root": {
            "handlers": ["console"],
            "level": "DEBUG" if settings.is_debug else "INFO",
        },
    }
