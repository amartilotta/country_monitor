import requests
from celery.signals import worker_ready

from apps.country.models import Country
from apps.tasks.celery_app import app
from apps.country.services import CountryService


@app.task(name="fetch_countries")
def fetch_countries():
    print("⌛ REGISTRANDO PAISES...")
    CountryService.fetch_countries()


@worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
        print("⚠️ Adding initial tasks!")
        sender.app.send_task("fetch_countries", connection=conn)
