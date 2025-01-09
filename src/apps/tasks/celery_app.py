from __future__ import absolute_import, unicode_literals
from datetime import timedelta
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('country_monitor')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['apps.tasks'])

app.conf.beat_schedule = {
    'fetch-countries-every-hour': {
        'task': 'fetch_countries',
        'schedule': timedelta(hours=1),
    },
}
