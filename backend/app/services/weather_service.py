from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.crud import city as city_crud
from app.crud import weather as weather_crud
from app.schemas.city import CityWithWeather
from app.schemas.weather import WeatherCreate, WeatherRead
from app.services import weather_client

settings = get_settings()


async def add_city(db: AsyncSession, name: str) -> CityWithWeather:
    city, created = await city_crud.get_or_create_city(db, name)
    if created:
        _enqueue_refresh(city.id)

    latest_weather = await weather_crud.get_latest_weather(db, city.id)
    return CityWithWeather(
        id=city.id,
        name=city.name,
        created_at=city.created_at,
        latest_weather=latest_weather,
    )


async def list_cities(db: AsyncSession) -> list[CityWithWeather]:
    cities = await city_crud.list_cities(db)
    return [
        CityWithWeather(
            id=city.id,
            name=city.name,
            created_at=city.created_at,
            latest_weather=(
                city.weather_records[0] if city.weather_records else None
            ),
        )
        for city in cities
    ]


async def refresh_city(db: AsyncSession, city_id: int) -> bool:
    city = await city_crud.get_city(db, city_id)
    if not city:
        return False

    _enqueue_refresh(city.id)
    return True


async def get_city_history(
    db: AsyncSession,
    city_id: int,
) -> list[WeatherRead] | None:
    city = await city_crud.get_city(db, city_id)
    if not city:
        return None

    return await weather_crud.get_weather_history(db, city_id)


async def fetch_and_store_weather(
    db: AsyncSession,
    city_id: int,
) -> bool:
    city = await city_crud.get_city(db, city_id)
    if not city:
        return False

    has_recent = await weather_crud.has_recent_weather(
        db,
        city_id,
        settings.weather_refresh_dedup_seconds,
    )
    if has_recent:
        return True

    payload = await weather_client.fetch_weather(city.name)
    normalized = weather_client.normalize_weather(payload)
    await weather_crud.create_weather(
        db,
        WeatherCreate(city_id=city.id, **normalized),
    )
    return True


def _enqueue_refresh(city_id: int) -> None:
    from app.tasks.weather_tasks import fetch_weather_for_city

    fetch_weather_for_city.delay(city_id)
