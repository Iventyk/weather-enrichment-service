from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.city import CityCreate, CityWithWeather
from app.schemas.weather import WeatherRead
from app.services import weather_service

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post(
    "",
    response_model=CityWithWeather,
    status_code=status.HTTP_201_CREATED,
)
async def create_city(
    city_data: CityCreate,
    db: AsyncSession = Depends(get_db),
) -> CityWithWeather:
    return await weather_service.add_city(db, city_data.name)


@router.get("", response_model=list[CityWithWeather])
async def get_cities(
    db: AsyncSession = Depends(get_db),
) -> list[CityWithWeather]:
    return await weather_service.list_cities(db)


@router.post("/{city_id}/refresh", status_code=status.HTTP_202_ACCEPTED)
async def refresh_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    queued = await weather_service.refresh_city(db, city_id)
    if not queued:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return {"status": "queued"}


@router.get("/{city_id}/history", response_model=list[WeatherRead])
async def get_city_history(
    city_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[WeatherRead]:
    history = await weather_service.get_city_history(db, city_id)
    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return history
