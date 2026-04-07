"""Tests for chat views."""
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from django_ai_assistant.models import Thread

from myproject.chat.models import ChatSession

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
        response = client.get("/chat/", follow=True)
        assert response.status_code == 200

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_chat_page_contains_api_link(self, mock_thread):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/", follow=True)
        content = response.content.decode()
        assert "/api/v1/docs/" in content

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_chat_page_contains_theme_toggle(self, mock_thread):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/", follow=True)
        content = response.content.decode()
        assert 'data-theme="light"' in content
        assert 'data-theme="dark"' in content
        assert 'data-theme="colorblind"' in content

    @patch("myproject.chat.views.use_cases.create_message", side_effect=_mock_create_message)
    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_htmx_message_post(self, mock_thread, mock_msg):
        user = User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        # Load chat page to create a session (follows redirect)
        client.get("/chat/", follow=True)
        session = ChatSession.objects.filter(user=user).first()
        response = client.post(
            f"/chat/{session.pk}/send/",
            {"message": "Hello, world!"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "Hello, world!" in content
        assert "Mocked response to: Hello, world!" in content

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_empty_message_returns_empty(self, mock_thread):
        user = User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        client.get("/chat/", follow=True)
        session = ChatSession.objects.filter(user=user).first()
        response = client.post(
            f"/chat/{session.pk}/send/",
            {"message": ""},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        assert response.content == b""

    @patch("myproject.chat.views.use_cases.create_message", side_effect=Exception("LLM down"))
    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_ai_error_returns_error_message(self, mock_thread, mock_msg):
        user = User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        client.get("/chat/", follow=True)
        session = ChatSession.objects.filter(user=user).first()
        response = client.post(
            f"/chat/{session.pk}/send/",
            {"message": "Hello"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "Sorry, something went wrong" in content


@pytest.mark.django_db
class TestSessionManagement:
    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_new_session_creates_and_redirects(self, mock_thread):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.get("/chat/new/")
        assert response.status_code == 302
        assert ChatSession.objects.count() == 1

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_can_switch_between_sessions(self, mock_thread):
        user = User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        # Create two sessions
        client.get("/chat/new/", follow=True)
        client.get("/chat/new/", follow=True)
        sessions = ChatSession.objects.filter(user=user).order_by("pk")
        assert sessions.count() == 2
        # Access each one
        resp1 = client.get(f"/chat/{sessions[0].pk}/")
        assert resp1.status_code == 200
        resp2 = client.get(f"/chat/{sessions[1].pk}/")
        assert resp2.status_code == 200

    @patch("myproject.chat.views.use_cases.create_thread", side_effect=_mock_create_thread)
    def test_session_list_shown_in_sidebar(self, mock_thread):
        user = User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        client.get("/chat/new/", follow=True)
        client.get("/chat/new/", follow=True)
        response = client.get("/chat/", follow=True)
        content = response.content.decode()
        assert "session-list" in content
        assert content.count("session-link") >= 2
