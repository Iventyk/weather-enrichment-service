from celery import Celery

from backend.app.config.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "weather_enrichment_service",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["backend.app.tasks.weather_tasks"],
)

celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
