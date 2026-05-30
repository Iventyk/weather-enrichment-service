from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WeatherBase(BaseModel):
    temperature: float
    humidity: int
    wind_speed: float
    feels_like: float
    description: str
    recommendation: str


class WeatherRead(WeatherBase):
    id: int
    city_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WeatherCreate(WeatherBase):
    city_id: int
