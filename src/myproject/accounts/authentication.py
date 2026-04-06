"""API key authentication backend for DRF."""
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import APIKey


class APIKeyAuthentication(BaseAuthentication):
    """Authenticate requests using the Authorization: Api-Key <key> header."""

    keyword = "Api-Key"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith(f"{self.keyword} "):
            return None

        raw_key = auth_header[len(self.keyword) + 1:]
        api_key = APIKey.verify_key(raw_key)
        if api_key is None:
            raise AuthenticationFailed("Invalid or revoked API key.")

        # Update last_used_at
        APIKey.objects.filter(pk=api_key.pk).update(last_used_at=timezone.now())

        return (api_key.user, api_key)
