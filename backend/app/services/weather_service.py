from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.config.settings import get_settings
from backend.app.crud import city as city_crud
from backend.app.crud import weather as weather_crud
from backend.app.models.city import City
from backend.app.models.weather import Weather
from backend.app.schemas.city import CityWithLatestWeather
from backend.app.schemas.weather import WeatherCreate
from backend.app.services.weather_client import WeatherClient, WeatherData


def build_recommendation(temperature: float) -> str:
    if temperature < 10:
        return "Take a warm jacket"
    if temperature > 25:
        return "Stay hydrated"
    return "Good weather for a walk"


async def create_city(session: AsyncSession, name: str) -> City:
    existing_city = await city_crud.get_city_by_name(session, name)
    if existing_city:
        return existing_city
    return await city_crud.create_city(session, name)


async def list_cities_with_latest_weather(
    session: AsyncSession,
) -> list[CityWithLatestWeather]:
    cities = await city_crud.list_cities(session)
    result = []
    for city in cities:
        latest_weather = await weather_crud.get_latest_weather(
            session,
            city.id,
        )
        result.append(
            CityWithLatestWeather.model_validate(
                {
                    "id": city.id,
                    "name": city.name,
                    "created_at": city.created_at,
                    "latest_weather": latest_weather,
                }
            )
        )
    return result


async def refresh_weather(
    session: AsyncSession,
    city_id: int,
    *,
    force: bool = False,
) -> Weather:
    city = await city_crud.get_city(session, city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    latest_weather = await weather_crud.get_latest_weather(session, city_id)
    if latest_weather and not force:
        ttl = timedelta(seconds=get_settings().weather_refresh_ttl_seconds)
        latest_created_at = latest_weather.created_at
        if latest_created_at.tzinfo is None:
            latest_created_at = latest_created_at.replace(tzinfo=UTC)
        if latest_created_at >= datetime.now(UTC) - ttl:
            return latest_weather

    weather_data = await WeatherClient().fetch_current_weather(city.name)
    return await _store_weather(session, city.id, weather_data)


async def get_weather_history(
    session: AsyncSession,
    city_id: int,
) -> list[Weather]:
    city = await city_crud.get_city(session, city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return await weather_crud.list_weather_history(session, city_id)


async def _store_weather(
    session: AsyncSession,
    city_id: int,
    weather_data: WeatherData,
) -> Weather:
    weather_in = WeatherCreate(
        city_id=city_id,
        temperature=weather_data.temperature,
        humidity=weather_data.humidity,
        wind_speed=weather_data.wind_speed,
        feels_like=weather_data.feels_like,
        description=weather_data.description,
        recommendation=build_recommendation(weather_data.temperature),
    )
    return await weather_crud.create_weather(session, weather_in)
