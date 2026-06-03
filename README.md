# weather-enrichment-service

A small production-style FastAPI backend that stores cities, enriches them with weather data in Celery background tasks, and exposes current and historical weather through HTTP APIs.

## Stack

- Python 3.13
- FastAPI
- SQLAlchemy 2.0 async
- Pydantic 2
- PostgreSQL
- Redis
- Celery
- httpx
- uvicorn

## Running locally with Docker

```bash
docker compose up --build
```

The API is available at <http://localhost:8000>.

Interactive API docs are available at <http://localhost:8000/docs>.

## Configuration

The service reads configuration from `.env`:

```env
DATABASE_URL=postgresql+asyncpg://weather:weather@postgres:5432/weather
REDIS_URL=redis://redis:6379/0
OPENWEATHER_API_KEY=
```

If `OPENWEATHER_API_KEY` is empty, the service uses a deterministic mock weather response so the assignment can run without external credentials.

## API

### Health check

```bash
curl http://localhost:8000/health
```

### Add city

Stores the city and queues a Celery task to fetch weather.

```bash
curl -X POST http://localhost:8000/cities \
  -H 'Content-Type: application/json' \
  -d '{"name":"Kyiv"}'
```

### List cities with latest weather

```bash
curl http://localhost:8000/cities
```

### Refresh weather manually

```bash
curl -X POST http://localhost:8000/cities/1/refresh
```

### Get weather history

```bash
curl http://localhost:8000/cities/1/history
```

## Notes

- Database tables are created automatically on application startup to keep the test assignment simple.
- Celery uses Redis as both broker and result backend.
- Weather refreshes are de-duplicated with a short time window to avoid repeated snapshots from immediate duplicate tasks.
