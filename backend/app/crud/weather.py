from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.weather import Weather
from app.schemas.weather import WeatherCreate


async def create_weather(
    db: AsyncSession,
    weather_data: WeatherCreate,
) -> Weather:
    weather = Weather(**weather_data.model_dump())
    db.add(weather)
    await db.commit()
    await db.refresh(weather)
    return weather


async def get_weather_history(
    db: AsyncSession,
    city_id: int,
) -> list[Weather]:
    result = await db.execute(
        select(Weather)
        .where(Weather.city_id == city_id)
        .order_by(Weather.created_at.desc())
    )
    return list(result.scalars().all())


async def get_latest_weather(
    db: AsyncSession,
    city_id: int,
) -> Weather | None:
    result = await db.execute(
        select(Weather)
        .where(Weather.city_id == city_id)
        .order_by(Weather.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def has_recent_weather(
    db: AsyncSession,
    city_id: int,
    seconds: int,
) -> bool:
    threshold = datetime.now(UTC) - timedelta(seconds=seconds)
    result = await db.execute(
        select(Weather.id)
        .where(Weather.city_id == city_id, Weather.created_at >= threshold)
        .limit(1)
    )
    return result.scalar_one_or_none() is not None
