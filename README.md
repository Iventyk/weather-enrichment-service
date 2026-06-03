# Weather Enrichment Service

A small full-stack test assignment for storing cities, enriching their weather asynchronously, and viewing the latest saved weather in a simple Angular UI.

## Stack

### Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2.0 async
- PostgreSQL
- Redis
- Celery
- httpx
- Pydantic 2

### Frontend

- Angular 21 standalone components
- REST API integration through `HttpClient`
- Nginx container for the production build
- Basic responsive UI with loading and error states

## Quick start with Docker

Run the whole project with one Docker Compose command from the repository root:

```bash
docker compose up --build
```

Optional setup before the first run:

```bash
cp .env .env.local  # optional: keep defaults for Docker
# Put your OpenWeatherMap API key into OPENWEATHERMAP_API_KEY if you have one.
```

Services:

- Frontend: <http://localhost:4200>
- API: <http://localhost:8000>
- API documentation: <http://localhost:8000/docs>
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

If `OPENWEATHERMAP_API_KEY` is empty, the backend uses deterministic mock weather generated from the city name.

## Local frontend development

```bash
cd frontend
npm install
npm start
```

The Angular dev server proxies `/api/*` requests to `http://localhost:8000`, so the frontend can call the backend without hard-coding a different browser URL.

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
- The frontend talks to `/api` and uses the Angular dev proxy or Nginx reverse proxy to reach the backend.
