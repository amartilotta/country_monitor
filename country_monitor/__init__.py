from __future__ import absolute_import, unicode_literals

from country_monitor.apps.tasks.celery_app import app as celery_app

__all__ = ('celery_app',)
