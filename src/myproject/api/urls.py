"""API URL configuration — DRF router + drf-spectacular URLs."""
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"chat/sessions", views.ChatSessionViewSet, basename="chat-session")

app_name = "api"

urlpatterns = [
    # Schema and docs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"),
    # Chat endpoint
    path("chat/", views.ChatMessageView.as_view(), name="chat-message"),
    # Router URLs
    path("", include(router.urls)),
]
