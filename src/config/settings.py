import typing as tp

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    server_host: tp.Annotated[str, Field(alias="SERVER_HOST", default="127.0.0.1")]
    server_port: tp.Annotated[int, Field(alias="SERVER_PORT", default=8000)]
    is_debug: tp.Annotated[bool, Field(alias="IS_DEBUG", default=True)]

    audio_play_chunk_size: tp.Annotated[int, Field(default=1024)]

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        env_nested_delimiter = "__"


settings = AppSettings()
