# weather-enrichment-service

A small FastAPI backend that stores cities, fetches current weather in Celery background tasks, enriches the data with a simple recommendation, and exposes latest and historical weather APIs.

## Stack

- Python 3.13
- FastAPI
- SQLAlchemy 2.0 async
- PostgreSQL
- Redis
- Celery
- httpx
- Pydantic 2

## Quick start

```bash
cp .env .env.local  # optional: keep defaults for Docker
# Put your OpenWeatherMap API key into OPENWEATHERMAP_API_KEY if you have one.
docker compose up --build
```

The API is available at <http://localhost:8000> and the interactive documentation at <http://localhost:8000/docs>.

If `OPENWEATHERMAP_API_KEY` is empty, the service uses deterministic mock weather generated from the city name.

## API

### Add a city

Stores the city and immediately queues a Celery task to fetch weather.

```bash
curl -X POST http://localhost:8000/cities \
  -H "Content-Type: application/json" \
  -d '{"name": "London"}'
```

### List cities with latest weather

```bash
curl http://localhost:8000/cities
```

### Refresh weather manually

Queues a Celery task for the selected city.

```bash
curl -X POST http://localhost:8000/cities/1/refresh
```

### Get weather history

```bash
curl http://localhost:8000/cities/1/history
```

### Health check

```bash
curl http://localhost:8000/health
```

## Development notes

- Tables are created automatically on application startup for this assignment.
- Celery tasks are idempotent for normal enrichment runs by reusing a recent weather snapshot within `WEATHER_REFRESH_TTL_SECONDS`.
- Manual refresh forces a new snapshot.
- OpenWeatherMap calls are isolated in `backend/app/services/weather_client.py` so the provider can be replaced without touching API or database code.
