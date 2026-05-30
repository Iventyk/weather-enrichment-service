from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.config.database import get_session
from backend.app.schemas.city import (
    CityCreate,
    CityRead,
    CityWithLatestWeather,
)
from backend.app.schemas.weather import WeatherRead
from backend.app.services import weather_service
from backend.app.tasks.weather_tasks import refresh_city_weather

router = APIRouter(tags=["weather"])


@router.post(
    "/cities",
    response_model=CityRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_city(
    city_in: CityCreate,
    session: AsyncSession = Depends(get_session),
) -> CityRead:
    city = await weather_service.create_city(session, city_in.name)
    refresh_city_weather.delay(city.id)
    return CityRead.model_validate(city)


@router.get("/cities", response_model=list[CityWithLatestWeather])
async def get_cities(
    session: AsyncSession = Depends(get_session),
) -> list[CityWithLatestWeather]:
    return await weather_service.list_cities_with_latest_weather(session)


@router.post("/cities/{city_id}/refresh", status_code=status.HTTP_202_ACCEPTED)
async def refresh_city(city_id: int) -> dict[str, str]:
    task = refresh_city_weather.delay(city_id, True)
    return {"task_id": task.id, "status": "queued"}


@router.get("/cities/{city_id}/history", response_model=list[WeatherRead])
async def get_city_history(
    city_id: int,
    session: AsyncSession = Depends(get_session),
) -> list[WeatherRead]:
    history = await weather_service.get_weather_history(session, city_id)
    return [WeatherRead.model_validate(weather) for weather in history]
