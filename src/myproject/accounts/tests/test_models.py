"""Tests for accounts models."""
import pytest
from django.contrib.auth import get_user_model

from myproject.accounts.models import APIKey

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.uuid is not None
        assert user.check_password("testpass123")

    def test_user_str(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        assert str(user) == "testuser"

    def test_user_has_timestamps(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        assert user.created_at is not None
        assert user.updated_at is not None


@pytest.mark.django_db
class TestAPIKeyModel:
    def test_create_api_key(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        raw_key, api_key = APIKey.create_key(user=user, name="Test Key")
        assert raw_key is not None
        assert len(raw_key) > 0
        assert api_key.prefix == raw_key[:8]
        assert api_key.user == user
        assert api_key.name == "Test Key"
        assert not api_key.revoked

    def test_verify_valid_key(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        raw_key, api_key = APIKey.create_key(user=user, name="Test Key")
        verified = APIKey.verify_key(raw_key)
        assert verified is not None
        assert verified.pk == api_key.pk

    def test_verify_invalid_key(self):
        result = APIKey.verify_key("nonexistent-key")
        assert result is None

    def test_revoked_key_rejected(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        raw_key, api_key = APIKey.create_key(user=user, name="Test Key")
        api_key.revoked = True
        api_key.save()
        result = APIKey.verify_key(raw_key)
        assert result is None
