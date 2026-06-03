from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "weather-enrichment-service"
    database_url: str = Field(
        default="postgresql+asyncpg://weather:weather@postgres:5432/weather",
        validation_alias="DATABASE_URL",
    )
    redis_url: str = Field(
        default="redis://redis:6379/0",
        validation_alias="REDIS_URL",
    )
    openweathermap_api_key: str | None = Field(
        default=None,
        validation_alias="OPENWEATHERMAP_API_KEY",
    )
    openweathermap_base_url: str = Field(
        default="https://api.openweathermap.org/data/2.5/weather",
        validation_alias="OPENWEATHERMAP_BASE_URL",
    )
    weather_refresh_ttl_seconds: int = Field(
        default=600,
        validation_alias="WEATHER_REFRESH_TTL_SECONDS",
    )
    cors_allowed_origins: str = Field(
        default="http://localhost:4200,http://127.0.0.1:4200",
        validation_alias="CORS_ALLOWED_ORIGINS",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_allowed_origins.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
