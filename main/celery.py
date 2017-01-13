from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
INCLUDED_TASKS = [
    'core.tasks',
]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery(
    'healworld_worker', broker=settings.BROKER_URL, include=INCLUDED_TASKS)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('django.conf:settings')


