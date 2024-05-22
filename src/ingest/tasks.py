import os
from celery import Celery

celery = Celery("tasks", backend=os.getenv("CELERY_BROKER_URL"), broker=os.getenv("CELERY_RESULT_BACKEND"))

@celery.task
def add(x, y):
    return x + y
