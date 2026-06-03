from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
