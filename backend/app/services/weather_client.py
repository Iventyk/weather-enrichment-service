import random
from typing import Any

import httpx

from app.config.settings import get_settings

settings = get_settings()


class WeatherClientError(RuntimeError):
    pass


async def fetch_weather(city_name: str) -> dict[str, Any]:
    if not settings.openweather_api_key:
        return _mock_weather(city_name)

    params = {
        "q": city_name,
        "appid": settings.openweather_api_key,
        "units": "metric",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            settings.openweather_base_url, params=params
        )

    if response.status_code == 404:
        raise WeatherClientError(
            f"Weather data for '{city_name}' was not found"
        )

    response.raise_for_status()
    return response.json()


def normalize_weather(payload: dict[str, Any]) -> dict[str, Any]:
    main = payload.get("main", {})
    wind = payload.get("wind", {})
    weather_items = payload.get("weather") or [{}]
    description = weather_items[0].get("description") or "No description"

    temperature = float(main.get("temp", 0.0))
    return {
        "temperature": temperature,
        "humidity": int(main.get("humidity", 0)),
        "wind_speed": float(wind.get("speed", 0.0)),
        "feels_like": float(main.get("feels_like", temperature)),
        "description": description,
        "recommendation": _recommendation(temperature),
    }


def _recommendation(temperature: float) -> str:
    if temperature < 10:
        return "Take a warm jacket"
    if temperature > 25:
        return "Stay hydrated"
    return "Good weather for a walk"


def _mock_weather(city_name: str) -> dict[str, Any]:
    random.seed(city_name.lower())
    temperature = round(random.uniform(-5, 32), 1)
    return {
        "main": {
            "temp": temperature,
            "humidity": random.randint(35, 90),
            "feels_like": round(temperature + random.uniform(-3, 3), 1),
        },
        "wind": {"speed": round(random.uniform(0.5, 12), 1)},
        "weather": [{"description": random.choice(_MOCK_DESCRIPTIONS)}],
    }


_MOCK_DESCRIPTIONS = [
    "clear sky",
    "few clouds",
    "light rain",
    "moderate breeze",
    "overcast clouds",
]
