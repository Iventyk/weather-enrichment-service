from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.weather import WeatherRead


class CityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class CityRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CityWithWeather(CityRead):
    latest_weather: WeatherRead | None = None
