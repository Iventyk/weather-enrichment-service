import asyncio

from app.config.database import AsyncSessionLocal
from app.core.celery_app import celery_app
from app.services.weather_service import fetch_and_store_weather


@celery_app.task(
    name="weather.fetch_for_city",
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def fetch_weather_for_city(city_id: int) -> bool:
    return asyncio.run(_fetch_weather_for_city(city_id))


async def _fetch_weather_for_city(city_id: int) -> bool:
    async with AsyncSessionLocal() as db:
        return await fetch_and_store_weather(db, city_id)
