from functools import lru_cache
from pathlib import Path
from typing_extensions import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.common.enums import LogLevel


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env")

    # environment settings
    env: str = "prod"

    # app settings
    title: str = "piggybankAPI"
    version: str = "0.1.0"
    api_prefix: str = ""
    summary: str = "piggybankAPI is a personal finance management system"
    description: str = ""

    # database settings
    postgres_user: str = "postgres"
    postgres_password: str = "changethis"
    postgres_db: str = "piggybankdb"

    @property
    def async_database_url(self) -> str:
        if self.env == "local":
            return (
                f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@localhost:5432/{self.postgres_db}"
            )
        if self.env == "docker":
            return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@db:5432/{self.postgres_db}"
        else:
            raise ValueError(f"Unknown environment: {self.env}")

    @property
    def sync_database_url(self) -> str:
        if self.env == "local":
            return (
                f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@localhost:5432/{self.postgres_db}"
            )
        if self.env == "docker":
            return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@db:5432/{self.postgres_db}"
        else:
            raise ValueError(f"Unknown environment: {self.env}")

    initial_admin_email: str = "changethis"
    initial_admin_password: str = "changethis"

    # logging settings
    echo_sql: bool = False
    log_level: LogLevel = LogLevel.DEBUG
    log_dir: str = "logs"
    log_filename: str = "backend.log"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # testing settings
    test_database_url: str = "sqlite+aiosqlite:///:memory:"

    # security settings
    algorithm: str = "HS256"
    secret_key: str = "changethis"
    access_token_expire_minutes: int = 15
    refresh_token_expire_hours: int = 24

    @property
    def secure_cookies(self) -> bool:
        if self.env == "prod":
            return True
        return False

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = f"The value of {var_name} is 'changethis'. For security, please change it."
            if self.env == "prod":
                raise ValueError(message)
            else:
                print(f"WARNING: {message}")

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("postgres_password", self.postgres_password)
        self._check_default_secret("initial_admin_email", self.initial_admin_email)
        self._check_default_secret("initial_admin_password", self.initial_admin_password)
        self._check_default_secret("secret_key", self.secret_key)

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
