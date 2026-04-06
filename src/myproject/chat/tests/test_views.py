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

    def test_htmx_message_post(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.post(
            "/chat/send/",
            {"message": "Hello, world!"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200

    def test_empty_message_returns_empty(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.post(
            "/chat/send/",
            {"message": ""},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        assert response.content == b""
