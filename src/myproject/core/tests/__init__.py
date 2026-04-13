"""Tests for management commands."""
from io import StringIO

import pytest
from django.core.management import call_command


@pytest.mark.django_db
class TestSeedDb:
    def test_creates_test_user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        out = StringIO()
        call_command("seed_db", stdout=out)
        output = out.getvalue()

        assert User.objects.filter(username="testuser").exists()
        assert "Created test user" in output

    def test_idempotent_on_second_run(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        call_command("seed_db", stdout=StringIO())
        call_command("seed_db", stdout=StringIO())

        assert User.objects.filter(username="testuser").count() == 1


@pytest.mark.django_db
class TestHealthCheck:
    def test_reports_database_ok(self):
        """health_check should report the database as OK since we have a test DB."""
        out = StringIO()
        # Should not raise SystemExit — the DB (testcontainer) is reachable
        call_command("health_check", stdout=out)
        output = out.getvalue()
        assert "Database: OK" in output
