from typing_extensions import Self

from functools import lru_cache
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[3] / ".env")

    # environment settings
    env: str = "docker"

    # database settings
    postgres_user: str = "postgres"
    postgres_password: str = "changethis"
    postgres_db: str = "piggybankdb"

    docker_async_database_url: str = (
        f"postgresql+asyncpg://${postgres_user}:${postgres_password}@db:5432/${postgres_db}"
    )
    docker_sync_database_url: str = (
        f"postgresql+psycopg2://${postgres_user}:${postgres_password}@db:5432/${postgres_db}"
    )

    dev_async_database_url: str = (
        f"postgresql+asyncpg://${postgres_user}:${postgres_password}@localhost:5432/${postgres_db}"
    )
    dev_sync_database_url: str = (
        f"postgresql+psycopg2://${postgres_user}:${postgres_password}@localhost:5432/${postgres_db}"
    )

    initial_admin_email: str = "changethis"
    initial_admin_password: str = "changethis"
    initial_admin_role: str = "admin"
    initial_roles: list[str] = ["admin", "user"]

    # logging settings
    echo_sql: bool = False

    # testing settings
    test_database_url: str = "sqlite+aiosqlite:///:memory:"

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = f"The value of {var_name} is 'changethis'. For security, please change it."
            if self.env == "dev":
                print(message)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("postgres_password", self.postgres_password)
        self._check_default_secret("initial_admin_email", self.initial_admin_email)
        self._check_default_secret("initial_admin_password", self.initial_admin_password)

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
