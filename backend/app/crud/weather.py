from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.weather import Weather
from backend.app.schemas.weather import WeatherCreate


async def create_weather(
    session: AsyncSession,
    weather_in: WeatherCreate,
) -> Weather:
    weather = Weather(**weather_in.model_dump())
    session.add(weather)
    await session.commit()
    await session.refresh(weather)
    return weather


async def get_latest_weather(
    session: AsyncSession,
    city_id: int,
) -> Weather | None:
    result = await session.execute(
        select(Weather)
        .where(Weather.city_id == city_id)
        .order_by(Weather.created_at.desc(), Weather.id.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def list_weather_history(
    session: AsyncSession,
    city_id: int,
) -> list[Weather]:
    result = await session.execute(
        select(Weather)
        .where(Weather.city_id == city_id)
        .order_by(Weather.created_at.desc(), Weather.id.desc())
    )
    return list(result.scalars().all())
