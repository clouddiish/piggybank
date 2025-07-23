from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[3] / ".env")

    # environment settings
    env: str = "docker"

    # database settings
    postgres_user: str
    postgres_password: str
    postgres_db: str = "piggybankdb"

    docker_async_database_url: str
    docker_sync_database_url: str

    dev_async_database_url: str
    dev_sync_database_url: str

    initial_admin_email: str
    initial_admin_password: str
    initial_admin_role: str = "admin"
    initial_roles: list[str] = ["admin", "user"]

    # logging settings
    echo_sql: bool = False

    # testing settings
    test_database_url: str = "sqlite+aiosqlite:///:memory:"


@lru_cache
def get_settings() -> Settings:
    return Settings()
