from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("country_monitor")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["apps.tasks"])

app.conf.beat_schedule = {
    "fetch-countries-every-hour": {
        "task": "fetch_countries",
        "schedule": crontab(minute="0", hour="*"),
        "options": {
            "expires": (
                120
            ),  # Prevents multiple tasks from running if it takes a long time
        },
    },
}
