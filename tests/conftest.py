"""
Shared pytest fixtures for the test suite.

Uses testcontainers to spin up a PostgreSQL container once per session.
The container is reused across all tests — it is NOT recreated per test
or per module. Django's test runner handles per-test transaction rollback.
"""
import os

import pytest


# ──────────────────────────────────────────────────────────────────────
# Testcontainer: session-scoped PostgreSQL
# ──────────────────────────────────────────────────────────────────────

def _start_postgres_container():
    """Start a Postgres testcontainer and return the connection URL.

    Returns None if testcontainers is not installed (falls back to
    whatever DATABASE_URL is configured in test settings).
    """
    try:
        from testcontainers.postgres import PostgresContainer
    except ImportError:
        return None

    pg = (
        PostgresContainer(
            image="postgres:18",
            username="test",
            password="test",
            dbname="test_myproject",
        )
        .with_env("PGDATA", "/var/lib/postgresql/18/docker")
    )
    pg.start()
    url = pg.get_connection_url().replace("psycopg2", "psycopg")
    return pg, url


# Module-level container — started once when conftest is first loaded,
# reused for the entire pytest session. This avoids pytest.skip() in a
# session fixture (which propagates skips to all dependent tests).
_container = None
_container_url = None

if not os.environ.get("TEST_DATABASE_URL"):
    _result = _start_postgres_container()
    if _result is not None:
        _container, _container_url = _result
        os.environ["TEST_DATABASE_URL"] = _container_url


def pytest_sessionfinish(session, exitstatus):
    """Stop the testcontainer when the pytest session ends."""
    global _container
    if _container is not None:
        _container.stop()
        _container = None
    os.environ.pop("TEST_DATABASE_URL", None)


@pytest.fixture(scope="session")
def django_db_setup(django_test_environment):
    """Override pytest-django's DB setup to use our testcontainer.

    pytest-django calls this fixture to create the test database.
    We point DATABASES at the testcontainer URL that was set in env,
    then let Django's normal test DB creation proceed.
    """
    from django.conf import settings

    db_url = os.environ.get("TEST_DATABASE_URL")
    if db_url:
        import environ
        env = environ.Env()
        settings.DATABASES["default"] = env.db_url_config(db_url)


# ──────────────────────────────────────────────────────────────────────
# Convenience fixtures
# ──────────────────────────────────────────────────────────────────────

@pytest.fixture
def user_factory():
    """Factory function for creating test users."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    def _create_user(username="testuser", email="test@example.com", password="testpass123", **kwargs):
        return User.objects.create_user(username=username, email=email, password=password, **kwargs)
    return _create_user


@pytest.fixture
def authenticated_client(user_factory):
    """Django test client logged in as a regular user."""
    from django.test import Client
    user = user_factory()
    client = Client()
    client.login(username="testuser", password="testpass123")
    client.user = user
    return client


@pytest.fixture
def api_client_with_key(user_factory):
    """DRF API client authenticated with an API key."""
    from rest_framework.test import APIClient
    from myproject.accounts.models import APIKey

    user = user_factory(username="apiuser", email="api@example.com")
    raw_key, _ = APIKey.create_key(user=user, name="Test API Key")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Api-Key {raw_key}")
    client.user = user
    return client
