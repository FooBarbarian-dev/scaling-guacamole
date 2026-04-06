"""Shared pytest fixtures for the test suite."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from myproject.accounts.models import APIKey

User = get_user_model()


@pytest.fixture
def user_factory():
    """Factory function for creating test users."""
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
    user = user_factory(username="apiuser", email="api@example.com")
    raw_key, _ = APIKey.create_key(user=user, name="Test API Key")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Api-Key {raw_key}")
    client.user = user
    return client
