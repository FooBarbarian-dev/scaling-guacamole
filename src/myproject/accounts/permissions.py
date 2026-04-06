"""Custom DRF permissions."""
from rest_framework.permissions import BasePermission


class HasValidAPIKey(BasePermission):
    """Allow access only to requests authenticated with a valid API key."""

    def has_permission(self, request, view) -> bool:
        return (
            hasattr(request, "auth")
            and request.auth is not None
            and hasattr(request.auth, "prefix")
        )
