# Weather Enrichment Service

A simple full-stack service for storing cities and enriching them with weather data asynchronously.
The backend stores cities in PostgreSQL, queues weather refresh jobs with Celery and Redis, and exposes a REST API.
The Angular frontend lets users add cities, view the latest weather, and trigger manual refreshes.

## Stack

### Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2.0 async
- Pydantic 2
- PostgreSQL
- Redis
- Celery
- httpx
- uvicorn

### Frontend

- Angular
- TypeScript
- REST API integration
- Basic responsive UI with loading and error states

## Run with Docker

Create a `.env` file in the repository root if you want to override the defaults:

```env
DATABASE_URL=postgresql+asyncpg://weather:weather@postgres:5432/weather
REDIS_URL=redis://redis:6379/0
OPENWEATHER_API_KEY=
CORS_ORIGINS=http://localhost:4200
```

Start the full stack:

```bash
docker compose up --build
```

Open the application:

- Frontend: <http://localhost:4200>
- Backend API: <http://localhost:8000>
- Interactive API docs: <http://localhost:8000/docs>

Stop the stack:

```bash
docker compose down
```

Remove database and frontend dependency volumes if you need a clean reset:

```bash
docker compose down -v
```

## Configuration

The backend reads configuration from `.env`:

| Variable | Default | Description |
| --- | --- | --- |
| `DATABASE_URL` | `postgresql+asyncpg://weather:weather@postgres:5432/weather` | PostgreSQL connection URL. |
| `REDIS_URL` | `redis://redis:6379/0` | Redis URL for Celery broker and result backend. |
| `OPENWEATHER_API_KEY` | empty | OpenWeather API key. If empty, deterministic mock weather is used. |
| `CORS_ORIGINS` | `http://localhost:4200` | Comma-separated list of allowed frontend origins. |

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
