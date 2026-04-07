"""Smoke tests — verify critical endpoints are reachable."""
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from django_ai_assistant.models import Thread

User = get_user_model()


def _mock_create_thread(name, assistant_id, user, **kwargs):
    return Thread.objects.create(name=name, assistant_id=assistant_id, created_by=user)


@pytest.mark.django_db
class TestSmokeEndpoints:
    def test_health_check_returns_200(self):
        client = Client()
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_admin_redirects_to_login(self):
        client = Client()
        response = client.get("/admin/")
        assert response.status_code == 302

    def test_swagger_docs_load(self):
        client = Client()
        response = client.get("/api/v1/docs/")
        assert response.status_code == 200

    def test_api_schema_loads(self):
        client = Client()
        response = client.get("/api/v1/schema/")
        assert response.status_code == 200

    def test_redoc_loads(self):
        client = Client()
        response = client.get("/api/v1/redoc/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestNavbarRendering:
    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_authenticated_navbar_contains_api_link(self, mock_thread):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/", follow=True)
        content = response.content.decode()
        assert "/api/v1/docs/" in content
        assert ">API<" in content

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_authenticated_navbar_contains_theme_toggle_buttons(self, mock_thread):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/", follow=True)
        content = response.content.decode()
        assert "theme-toggle-btn" in content
        assert 'data-theme="light"' in content
        assert 'data-theme="dark"' in content
        assert 'data-theme="colorblind"' in content

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_base_template_includes_htmx_fallback(self, mock_thread):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/", follow=True)
        content = response.content.decode()
        assert "htmx.min.js" in content
        assert "unpkg.com/htmx.org" in content
