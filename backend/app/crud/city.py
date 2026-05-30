from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.city import City


def normalize_city_name(name: str) -> str:
    return " ".join(name.strip().split()).title()


async def get_city(session: AsyncSession, city_id: int) -> City | None:
    return await session.get(City, city_id)


async def get_city_by_name(session: AsyncSession, name: str) -> City | None:
    normalized_name = normalize_city_name(name)
    result = await session.execute(
        select(City).where(func.lower(City.name) == normalized_name.lower())
    )
    return result.scalar_one_or_none()


async def create_city(session: AsyncSession, name: str) -> City:
    city = City(name=normalize_city_name(name))
    session.add(city)
    await session.commit()
    await session.refresh(city)
    return city


async def list_cities(session: AsyncSession) -> list[City]:
    result = await session.execute(select(City).order_by(City.name.asc()))
    return list(result.scalars().all())
