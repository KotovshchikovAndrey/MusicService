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
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}"
            f"/{self.db_name}"
        )

    def get_test_connection_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}"
            f"/test_{self.db_name}"
        )


class SearchEngineSettings(Settings):
    address: Annotated[str, Field(alias="ELASTIC_SEARCH_ADDRESS")]
    track_index: Annotated[str, Field(alias="ELASTIC_SEARCH_TRACK_INDEX")]


class BrokerSettings(Settings):
    host: Annotated[str, Field(alias="RABBITMQ_HOST")]
    port: Annotated[int, Field(alias="RABBITMQ_PORT")]
    user: Annotated[str, Field(alias="RABBITMQ_USER")]
    password: Annotated[str, Field(alias="RABBITMQ_PASSWORD")]

    albums_to_upload_queue: Annotated[
        str,
        Field(alias="RABBITMQ_ALBUMS_TO_UPLOAD_QUEUE"),
    ]

    email_verification_queue: Annotated[
        str,
        Field(alias="RABBITMQ_EMAIL_VERIFICATION_QUEUE"),
    ]

    def get_connection_url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"


class SmtpSettings(Settings):
    host: Annotated[str, Field(alias="SMTP_HOST")]
    port: Annotated[int, Field(alias="SMTP_PORT")]
    username: Annotated[str, Field(alias="SMTP_USERNAME")]
    password: Annotated[str, Field(alias="SMTP_PASSWORD")]

    use_tls: Annotated[bool, Field(default=True)]


class AuthSettings(Settings):
    access_token_secret: Annotated[str, Field(alias="ACCESS_TOKEN_SECRET")]
    refresh_token_secret: Annotated[str, Field(alias="REFRESH_TOKEN_SECRET")]


class AppSettings(BaseModel):
    server_host: Annotated[str, Field(alias="SERVER_HOST", default="127.0.0.1")]
    server_port: Annotated[int, Field(alias="SERVER_PORT", default=8000)]
    is_debug: Annotated[bool, Field(alias="IS_DEBUG", default=True)]

    database: DatabaseSettings = DatabaseSettings()
    blob_storage: BlobStorageSettings = BlobStorageSettings()
    search_engine: SearchEngineSettings = SearchEngineSettings()
    broker: BrokerSettings = BrokerSettings()
    smtp: SmtpSettings = SmtpSettings()
    auth: AuthSettings = AuthSettings()


settings = AppSettings()
