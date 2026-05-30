import asyncio

from backend.app.config.database import AsyncSessionLocal
from backend.app.core.celery_app import celery_app
from backend.app.services.weather_service import refresh_weather


@celery_app.task(name="weather.refresh_city_weather")
def refresh_city_weather(
    city_id: int,
    force: bool = False,
) -> dict[str, int | str]:
    return asyncio.run(_refresh_city_weather(city_id, force=force))


async def _refresh_city_weather(
    city_id: int,
    *,
    force: bool,
) -> dict[str, int | str]:
    async with AsyncSessionLocal() as session:
        weather = await refresh_weather(session, city_id, force=force)
        return {
            "city_id": city_id,
            "weather_id": weather.id,
            "status": "stored",
        }
