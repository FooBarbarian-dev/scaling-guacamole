"""Seed the database with example development data."""
from django.core.management.base import BaseCommand

from myproject.accounts.models import User


class Command(BaseCommand):
    help = "Seed the database with example development data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Create example users
        if not User.objects.filter(username="testuser").exists():
            User.objects.create_user(
                username="testuser",
                email="test@example.com",
                password="testpass123",
            )
            self.stdout.write(self.style.SUCCESS("Created test user: testuser / testpass123"))
        else:
            self.stdout.write("Test user already exists, skipping.")

        self.stdout.write(self.style.SUCCESS("Database seeding complete."))
