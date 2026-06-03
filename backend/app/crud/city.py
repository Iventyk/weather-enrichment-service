from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.city import City


def _city_by_name_query(name: str) -> Select[tuple[City]]:
    return select(City).where(func.lower(City.name) == name.lower())


async def get_city(db: AsyncSession, city_id: int) -> City | None:
    return await db.get(City, city_id)


async def get_city_by_name(db: AsyncSession, name: str) -> City | None:
    result = await db.execute(_city_by_name_query(name))
    return result.scalar_one_or_none()


async def get_or_create_city(db: AsyncSession, name: str) -> tuple[City, bool]:
    normalized_name = " ".join(name.strip().split())
    city = await get_city_by_name(db, normalized_name)
    if city:
        return city, False

    city = City(name=normalized_name)
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city, True


async def list_cities(db: AsyncSession) -> list[City]:
    result = await db.execute(
        select(City)
        .options(selectinload(City.weather_records))
        .order_by(City.name.asc())
    )
    return list(result.scalars().unique().all())
