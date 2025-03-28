from typing import Literal

from databases import DatabaseURL
from pydantic_settings import BaseSettings as PydanticBaseSettings, SettingsConfigDict


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class Config(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str

    # Database settings
    DATABASE_URL: DatabaseURL | str
    ASYNC_DATABASE_URL: DatabaseURL | str
    DATABASE_MIN_CONNECTIONS: int = 10
    DATABASE_MAX_CONNECTIONS: int = 20
    DATABASE_TIMEOUT: int = 30
    DATABASE_MAX_INACTIVE_CONNECTION_LIFETIME: int = 180


settings = Config()
