"""Tests for chat views."""
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from django_ai_assistant.models import Thread

User = get_user_model()


def _mock_create_thread(name, assistant_id, user, **kwargs):
    """Create a real Thread object for tests."""
    return Thread.objects.create(name=name, assistant_id=assistant_id, created_by=user)


def _mock_create_message(assistant_id, thread, user, content, **kwargs):
    """Return a fake AI response for tests."""
    return {"output": f"Mocked response to: {content}"}


@pytest.mark.django_db
class TestChatSession:
    def test_chat_page_requires_login(self):
        client = Client()
        response = client.get("/chat/")
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_chat_page_loads_for_authenticated_user(self, mock_thread):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/")
        assert response.status_code == 200

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_chat_page_contains_api_link(self, mock_thread):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/")
        content = response.content.decode()
        assert "/api/v1/docs/" in content

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_chat_page_contains_theme_toggle(self, mock_thread):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/")
        content = response.content.decode()
        assert 'data-theme="light"' in content
        assert 'data-theme="dark"' in content
        assert 'data-theme="colorblind"' in content

    @patch("myproject.chat.views.use_cases.create_message", side_effect=_mock_create_message)
    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_htmx_message_post(self, mock_thread, mock_msg):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        # Load the chat page first to create the session
        client.get("/chat/")
        response = client.post(
            "/chat/send/",
            {"message": "Hello, world!"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "Hello, world!" in content
        assert "Mocked response to: Hello, world!" in content

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_empty_message_returns_empty(self, mock_thread):
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

    @patch("myproject.chat.views.use_cases.create_message", side_effect=Exception("LLM down"))
    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_ai_error_returns_error_message(self, mock_thread, mock_msg):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        client.get("/chat/")
        response = client.post(
            "/chat/send/",
            {"message": "Hello"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "Sorry, something went wrong" in content
