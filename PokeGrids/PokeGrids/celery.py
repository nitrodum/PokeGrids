from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PokeGrids.settings')
# create a Celery instance and configure it using the settings from Django
celery_app = Celery('PokeGrids')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()

@celery_app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')