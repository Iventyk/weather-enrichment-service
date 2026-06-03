from celery import Celery

from app.config.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "weather_enrichment_service",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.weather_tasks"],
)

celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    timezone="UTC",
)
