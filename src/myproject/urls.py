"""Root URL configuration for myproject."""
from django.contrib import admin
from django.urls import include, path

from .health import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health-check"),
    path("api/v1/", include("myproject.api.urls")),
    path("chat/", include("myproject.chat.urls")),
    path("accounts/", include("myproject.accounts.urls")),
    path("ai-assistant/", include("django_ai_assistant.urls")),
]
