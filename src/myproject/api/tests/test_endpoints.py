"""Tests for API endpoints."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from myproject.accounts.models import APIKey

User = get_user_model()


@pytest.mark.django_db
class TestChatEndpoint:
    def test_chat_with_auth_returns_200(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post("/api/v1/chat/", {"message": "Hello"}, format="json")
        assert response.status_code == 200
        assert "content" in response.data

    def test_chat_without_auth_returns_401_or_403(self):
        client = APIClient()
        response = client.post("/api/v1/chat/", {"message": "Hello"}, format="json")
        assert response.status_code in (401, 403)

    def test_chat_sessions_list(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get("/api/v1/chat/sessions/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestSchemaEndpoints:
    def test_swagger_ui_loads(self):
        client = APIClient()
        response = client.get("/api/v1/docs/")
        assert response.status_code == 200

    def test_schema_loads(self):
        client = APIClient()
        response = client.get("/api/v1/schema/")
        assert response.status_code == 200

    def test_redoc_loads(self):
        client = APIClient()
        response = client.get("/api/v1/redoc/")
        assert response.status_code == 200
