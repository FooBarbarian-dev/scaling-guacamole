"""Smoke tests — verify critical endpoints are reachable."""
import pytest
from django.test import Client


@pytest.mark.django_db
class TestSmokeEndpoints:
    def test_health_check_returns_200(self):
        client = Client()
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_admin_redirects_to_login(self):
        client = Client()
        response = client.get("/admin/")
        assert response.status_code == 302

    def test_swagger_docs_load(self):
        client = Client()
        response = client.get("/api/v1/docs/")
        assert response.status_code == 200

    def test_api_schema_loads(self):
        client = Client()
        response = client.get("/api/v1/schema/")
        assert response.status_code == 200

    def test_redoc_loads(self):
        client = Client()
        response = client.get("/api/v1/redoc/")
        assert response.status_code == 200
