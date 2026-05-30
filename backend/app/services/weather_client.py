import hashlib
from dataclasses import dataclass

import httpx

from backend.app.config.settings import get_settings


@dataclass(frozen=True)
class WeatherData:
    temperature: float
    humidity: int
    wind_speed: float
    feels_like: float
    description: str


class WeatherClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def fetch_current_weather(self, city_name: str) -> WeatherData:
        if not self.settings.openweathermap_api_key:
            return self._mock_weather(city_name)

        params = {
            "q": city_name,
            "appid": self.settings.openweathermap_api_key,
            "units": "metric",
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                self.settings.openweathermap_base_url,
                params=params,
            )
            response.raise_for_status()
            payload = response.json()

        return WeatherData(
            temperature=float(payload["main"]["temp"]),
            humidity=int(payload["main"]["humidity"]),
            wind_speed=float(payload["wind"].get("speed", 0.0)),
            feels_like=float(payload["main"]["feels_like"]),
            description=payload["weather"][0]["description"],
        )

    def _mock_weather(self, city_name: str) -> WeatherData:
        digest = hashlib.sha256(city_name.lower().encode()).hexdigest()
        seed = int(digest[:8], 16)
        temperature = round((seed % 3500) / 100 - 5, 1)
        humidity = 35 + seed % 60
        wind_speed = round((seed % 1300) / 100, 1)
        feels_like = round(temperature - 1.5 + (seed % 30) / 10, 1)
        description = self._mock_description(temperature)

        return WeatherData(
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            feels_like=feels_like,
            description=description,
        )

    @staticmethod
    def _mock_description(temperature: float) -> str:
        if temperature < 5:
            return "cold and cloudy"
        if temperature > 25:
            return "sunny"
        return "partly cloudy"
