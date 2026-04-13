"""Tests for accounts views."""
import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.mark.django_db
class TestLoginView:
    def test_login_page_loads(self):
        client = Client()
        response = client.get("/accounts/login/")
        assert response.status_code == 200

    def test_login_success(self):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        response = client.post(
            "/accounts/login/",
            {"username": "testuser", "password": "testpass123"},
        )
        assert response.status_code == 302

    def test_unauthenticated_redirect(self):
        client = Client()
        response = client.get("/chat/")
        assert response.status_code == 302
        assert "/accounts/login/" in response.url


@pytest.mark.django_db
class TestLogoutView:
    def test_logout(self):
        User.objects.create_user(username="testuser", password="testpass123")
        client = Client()
        client.login(username="testuser", password="testpass123")
        response = client.post("/accounts/logout/")
        assert response.status_code == 302
