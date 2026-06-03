# Weather Enrichment Service

A simple full-stack test assignment that stores cities, enriches them with weather data in asynchronous Celery tasks, and displays the latest weather in an Angular UI.

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
- Nginx for the production Docker image

## Run the project with Docker

Create a `.env` file in the project root if it does not exist:

```env
APP_NAME=weather-enrichment-service
DEBUG=false
DATABASE_URL=postgresql+asyncpg://weather:weather@postgres:5432/weather
REDIS_URL=redis://redis:6379/0
OPENWEATHER_API_KEY=
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5/weather
WEATHER_REFRESH_DEDUP_SECONDS=60
```

Start the whole stack with one Docker command:

```bash
docker compose up --build
```

Services will be available at:

- Frontend: <http://localhost:4200>
- Backend API: <http://localhost:8000>
- Interactive API docs: <http://localhost:8000/docs>
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

Stop the stack with:

```bash
docker compose down
```

Stop the stack and remove the PostgreSQL volume with:

```bash
docker compose down -v
```

## Weather API configuration

Set `OPENWEATHER_API_KEY` in `.env` to use OpenWeather data.

If `OPENWEATHER_API_KEY` is empty, the backend uses deterministic mock weather data. This keeps the project easy to run for the test assignment without external credentials.

## API examples

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

## Local frontend development

If you want to run Angular outside Docker, install dependencies and start the development server:

```bash
cd frontend
npm install
npm start
```

The Angular development server uses `proxy.conf.json` to forward `/api` requests to `http://localhost:8000`.

## Notes

- Database tables are created automatically on backend startup to keep the assignment simple.
- Celery uses Redis as both broker and result backend.
- Weather refreshes are de-duplicated with a short time window to avoid repeated snapshots from immediate duplicate tasks.
- The frontend shows loading and error states for city loading, city creation, and manual refresh actions.
