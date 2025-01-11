from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("country_monitor")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["apps.tasks"])

app.conf.beat_schedule = {
    "fetch-countries-every-hour": {
        "task": "fetch_countries",
        "schedule": timedelta(hours=1),
        "options": {
            "expires": (
                60 * 60
            ),  # Prevents multiple tasks from running if it takes a long time
        },
    },
}
