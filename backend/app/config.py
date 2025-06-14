from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "docker"
    postgres_user: str
    docker_async_database_url: str
    docker_sync_database_url: str
    dev_async_database_url: str
    dev_sync_database_url: str
    echo_sql: bool = True

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
