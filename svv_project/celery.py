from __future__ import absolute_import

import os

import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'svv_project.settings')

app = celery.Celery('svv_project.celery')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')
