from typing import Annotated
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class BlobStorageSettings(Settings):
    address: Annotated[str, Field(alias="S3_ADDRESS")]
    access_key_id: Annotated[str, Field(alias="S3_ACCESS_KEY_ID")]
    secret_key: Annotated[str, Field(alias="S3_SECRET_KEY")]
    bucket_name: Annotated[str, Field(alias="S3_BUCKET_NAME")]

    use_ssl: Annotated[bool, Field(default=False)]
    chunk_size: Annotated[int, Field(default=1024)]


class DatabaseSettings(Settings):
    host: Annotated[str, Field(alias="POSTGRES_HOST")]
    port: Annotated[int, Field(alias="POSTGRES_PORT")]
    user: Annotated[str, Field(alias="POSTGRES_USER")]
    password: Annotated[str, Field(alias="POSTGRES_PASSWORD")]
    db_name: Annotated[str, Field(alias="POSTGRES_DB_NAME")]

    def get_connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class AppSettings(BaseModel):
    server_host: Annotated[str, Field(alias="SERVER_HOST", default="127.0.0.1")]
    server_port: Annotated[int, Field(alias="SERVER_PORT", default=8000)]
    is_debug: Annotated[bool, Field(alias="IS_DEBUG", default=True)]

    database: DatabaseSettings = DatabaseSettings()
    blob_storage: BlobStorageSettings = BlobStorageSettings()


settings = AppSettings()
