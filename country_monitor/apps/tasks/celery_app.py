# country_monitor/celery_app.py
from __future__ import absolute_import, unicode_literals
from datetime import timedelta
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'country_monitor.config.settings')

app = Celery('country_monitor')

app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(['country_monitor.apps.tasks'])

# app.conf.beat_schedule = {
#     'fetch-countries-every-hour': {
#         'task': 'prueba',
#         'schedule': timedelta(seconds=10),
#     },
# }
# @app.task(name="prueba")
# def add():
#     return os.mkdir("C:\\Users\\aguco\\Desktop\\Proyectos\\Frameworks\\Django\\country_monitor_drf\\country_monitor\\apps\\tasks\\prueba")
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(minute='*'),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)