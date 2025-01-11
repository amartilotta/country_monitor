from celery.signals import worker_ready
from apps.country.services import CountryService
from apps.tasks.celery_app import app
from django.core.cache import cache

@app.task(name="fetch_countries")
def fetch_countries():
    """
    Celery task to fetch and register countries from the external API.

    This task ensures that it does not run concurrently by using a cache lock.
    """
    lock_id = "fetch_countries_lock"
    timeout = 3600  # 1 hora

    if cache.get(lock_id):
        print("⚠️ Task is already running, skipping execution.")
        return

    cache.set(lock_id, True, timeout)
    try:
        print("⌛ Registering countries...")
        CountryService.fetch_countries()
    finally:
        cache.delete(lock_id)

@worker_ready.connect
def at_start(sender, **k):
    """
    Signal handler that runs when the Celery worker is ready.

    This function adds the initial task to fetch countries.

    :param sender: The sender of the signal.
    :param **k: Additional keyword arguments.
    """
    with sender.app.connection() as conn:
        print("⚠️ Adding initial tasks!")
        sender.app.send_task("fetch_countries", connection=conn)
