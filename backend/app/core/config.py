import secrets
import warnings
from typing import Any, Annotated

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    computed_field,
    model_validator,
)

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

def parse_cors(v: Any) -> list[str]:
    if isinstance(v, str):
        return v.split(",")
    elif isinstance(v, list):
        return v
    raise ValueError


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "TaskLine"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    FRONTEND_URL: str = "http://localhost:3000"
    ENVIRONMENT: str = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [
            str(origin).rstrip("/")
            for origin in self.BACKEND_CORS_ORIGINS
        ] + [self.FRONTEND_URL.rstrip("/")]
    DB_ENGINE: str = "sqlite"
    SQLITE_DATABASE_NAME: str = "taskline.db"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_ENGINE == "sqlite":
            return f"sqlite:///{self.SQLITE_DATABASE_NAME}"
        from urllib.parse import quote_plus
        password = quote_plus(self.DB_PASSWORD)
        return f"postgresql://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    AI_ENABLED: bool = True
    AI_MODEL: str = "gpt-4o-mini"
    AI_DAILY_LIMIT: int = 100

    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str

    def check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis". '
                "Please change it in production"
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, UserWarning)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def enforce_non_default_secrets(self) -> Self:
        self.check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self.check_default_secret("FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD)
        return self


settings = Settings()