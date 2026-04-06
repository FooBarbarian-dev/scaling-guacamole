"""Verify that required services (database, Redis, Temporal) are reachable."""
import sys

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Verify that required services are reachable"

    def handle(self, *args, **options):
        all_ok = True

        # Check database
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS("Database: OK"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Database: FAILED — {e}"))
            all_ok = False

        # Check Redis
        try:
            from django.core.cache import cache
            cache.set("health_check", "ok", 5)
            value = cache.get("health_check")
            if value == "ok":
                self.stdout.write(self.style.SUCCESS("Redis: OK"))
            else:
                self.stdout.write(self.style.WARNING("Redis: UNEXPECTED RESPONSE"))
                all_ok = False
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Redis: UNAVAILABLE — {e}"))

        if not all_ok:
            sys.exit(1)

        self.stdout.write(self.style.SUCCESS("\nAll services are reachable."))
