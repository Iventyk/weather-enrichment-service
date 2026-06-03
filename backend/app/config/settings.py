from functools import lru_cache

from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "weather-enrichment-service"
    debug: bool = False

    database_url: str = Field(
        default="postgresql+asyncpg://weather:weather@postgres:5432/weather",
    )
    redis_url: str = "redis://redis:6379/0"

    openweather_api_key: str | None = None
    openweather_base_url: str = (
        "https://api.openweathermap.org/data/2.5/weather"
    )
    weather_refresh_dedup_seconds: int = 60
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default=["http://localhost:4200"],
    )

    @staticmethod
    def _split_csv(value: str) -> list[str]:
        return [item.strip() for item in value.split(",") if item.strip()]

    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return cls._split_csv(value)
        return value

    @field_validator("cors_origins", mode="before")
    @classmethod
    def validate_cors_origins(cls, value: str | list[str]) -> list[str]:
        return cls.parse_cors_origins(value)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
