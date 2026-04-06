"""Tests for chat views."""
import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.mark.django_db
class TestChatSession:
    def test_chat_page_requires_login(self):
        client = Client()
        response = client.get("/chat/")
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_chat_page_loads_for_authenticated_user(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/")
        assert response.status_code == 200

    def test_chat_page_contains_api_link(self):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/")
        content = response.content.decode()
        assert "/api/v1/docs/" in content

    def test_chat_page_contains_theme_toggle(self):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/")
        content = response.content.decode()
        assert 'data-theme="light"' in content
        assert 'data-theme="dark"' in content
        assert 'data-theme="colorblind"' in content

    def test_htmx_message_post(self):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.post(
            "/chat/send/",
            {"message": "Hello, world!"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "Hello, world!" in content
        assert "Echo: Hello, world!" in content

    def test_empty_message_returns_empty(self):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.post(
            "/chat/send/",
            {"message": ""},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        assert response.content == b""
