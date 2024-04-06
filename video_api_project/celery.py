import logging
import os
import signal

from celery import Celery, Task
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class BaseTask(Task):
    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = True
    retry_backoff_max = 700
    retry_jitter = 10

    def __call__(self, *args, **kwargs):
        signal.signal(signal.SIGTERM,
                      lambda signum, frame: logging.info('SIGTERM received, wait till the task finished'))
        return super().__call__(*args, **kwargs)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_api_project.settings')

app = Celery('video_api_project',
             broker=f'redis://:{os.getenv("REDIS_PASSWORD")}@{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}',
             video_api_project=f'redis://:{os.getenv("REDIS_PASSWORD")}@{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}',)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'fetch-and-store-videos-every-10-seconds': {
        'task': 'video_api.tasks.fetch_and_store_videos',
        'schedule': timedelta(seconds=10),
        'args': (['AIzaSyDpTnhfUvO3aOUEEFZ4ptrw96iKvjS207g', 'AIzaSyC5i62_iHK6fq77TT-EUQjAcjp_xdYUqA4','AIzaSyAejXRbEjbT7K5m-kV8uAUrfk5qhkGnLYc'],), # List of API keys
    },
}

app.Task = BaseTask
app.autodiscover_tasks()
