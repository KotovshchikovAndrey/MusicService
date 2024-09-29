from pydantic import BaseModel


class LoggerConfig(BaseModel):
    LOG_FORMAT: str = "%(levelprefix)s %(asctime)s - %(module)s - %(message)s"
    LOG_LEVEL: str = "INFO"

    version: int = 1
    disable_existing_loggers: bool = False

    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }

    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }

    loggers: dict = {
        "root": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
    }
