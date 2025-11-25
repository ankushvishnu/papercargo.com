from celery import Celery
from app.core.settings import settings

celery = Celery(
    "papercargo",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
celery.conf.task_routes = {"app.tasks.worker_tasks.*": {"queue": "papercargo_tasks"}}
