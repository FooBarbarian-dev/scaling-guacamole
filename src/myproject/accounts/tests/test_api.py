"""Tests for API key authentication."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from myproject.accounts.models import APIKey

User = get_user_model()


@pytest.mark.django_db
class TestAPIKeyAuthentication:
    def test_api_key_auth_works(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        raw_key, _ = APIKey.create_key(user=user, name="Test Key")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Api-Key {raw_key}")
        response = client.get("/api/v1/chat/sessions/")
        assert response.status_code == 200

    def test_missing_key_returns_401(self):
        client = APIClient()
        response = client.get("/api/v1/chat/sessions/")
        assert response.status_code in (401, 403)

    def test_invalid_key_returns_401(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Api-Key invalid-key-here")
        response = client.get("/api/v1/chat/sessions/")
        assert response.status_code in (401, 403)
