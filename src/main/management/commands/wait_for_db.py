import time

from psycopg2 import OperationalError as Psycopg2Error

from typing import Any
from django.core.management import BaseCommand
from django.db import OperationalError

class Command(BaseCommand):
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        """Entrypoint for command"""
        self.stdout.write('Waiting for database... ')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write(
                    self.style.WARNING('Database unavailable, waiting 1 second...'))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))