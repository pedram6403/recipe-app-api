import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """djangocommand to pause execution until db is unavailable"""
    def handle(self, *args, **options):
        self.stdout.write('waiting for db ...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database is unavailable, wait for a second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('database is available!'))
