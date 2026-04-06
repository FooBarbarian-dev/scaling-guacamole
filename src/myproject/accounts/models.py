"""User and API key models."""
import hashlib
import secrets
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with UUID and timestamps."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return self.username


class APIKey(models.Model):
    """API key for programmatic access. The raw key is shown once at creation."""

    prefix = models.CharField(max_length=8, editable=False, db_index=True)
    hashed_key = models.CharField(max_length=128, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys")
    name = models.CharField(max_length=255, help_text="A label for this API key")
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "API key"
        verbose_name_plural = "API keys"

    def __str__(self) -> str:
        return f"{self.prefix}... ({self.name})"

    @classmethod
    def create_key(cls, user: User, name: str) -> tuple[str, "APIKey"]:
        """Generate a new API key. Returns (raw_key, api_key_instance).

        The raw key is only available at creation time. Store it securely.
        """
        raw_key = secrets.token_urlsafe(48)
        prefix = raw_key[:8]
        hashed = hashlib.sha256(raw_key.encode()).hexdigest()
        api_key = cls.objects.create(
            prefix=prefix,
            hashed_key=hashed,
            user=user,
            name=name,
        )
        return raw_key, api_key

    @classmethod
    def verify_key(cls, raw_key: str) -> "APIKey | None":
        """Look up an API key by its raw value. Returns None if not found or revoked."""
        hashed = hashlib.sha256(raw_key.encode()).hexdigest()
        try:
            api_key = cls.objects.select_related("user").get(hashed_key=hashed, revoked=False)
            return api_key
        except cls.DoesNotExist:
            return None
