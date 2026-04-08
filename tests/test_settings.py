"""Tests for settings loading — verify DJANGO_ENV selects the correct module."""
from unittest.mock import patch

import pytest


class TestSettingsInit:
    def test_development_is_default(self):
        """With no DJANGO_ENV, settings.__init__ should load development settings."""
        import importlib
        with patch.dict("os.environ", {}, clear=False):
            # Remove DJANGO_ENV if present
            import os
            os.environ.pop("DJANGO_ENV", None)
            mod = importlib.import_module("myproject.settings")
            mod = importlib.reload(mod)
            assert mod.DEBUG is True

    def test_production_env_loads_production_settings(self):
        """With DJANGO_ENV=production, settings.__init__ should load production."""
        import importlib
        with patch.dict("os.environ", {"DJANGO_ENV": "production"}):
            mod = importlib.import_module("myproject.settings")
            mod = importlib.reload(mod)
            assert mod.DEBUG is False
            assert mod.SECURE_SSL_REDIRECT is True
            assert mod.SESSION_COOKIE_SECURE is True
            assert mod.CSRF_COOKIE_SECURE is True


class TestProductionSettings:
    def test_security_headers_enabled(self):
        from myproject.settings import production
        assert production.DEBUG is False
        assert production.SECURE_SSL_REDIRECT is True
        assert production.SECURE_HSTS_SECONDS == 31536000
        assert production.SECURE_HSTS_INCLUDE_SUBDOMAINS is True
        assert production.SESSION_COOKIE_SECURE is True
        assert production.CSRF_COOKIE_SECURE is True

    def test_whitenoise_in_middleware(self):
        from myproject.settings import production
        assert "whitenoise.middleware.WhiteNoiseMiddleware" in production.MIDDLEWARE

    def test_cors_wildcard_disabled(self):
        from myproject.settings import production
        assert production.CORS_ALLOW_ALL_ORIGINS is False

    def test_database_connection_pooling(self):
        from myproject.settings import production
        assert production.DATABASES["default"]["CONN_MAX_AGE"] == 600
        assert production.DATABASES["default"]["CONN_HEALTH_CHECKS"] is True

    def test_redis_cache_configured(self):
        from myproject.settings import production
        assert production.CACHES["default"]["BACKEND"] == "django.core.cache.backends.redis.RedisCache"


class TestDevelopmentSettings:
    def test_debug_enabled(self):
        from myproject.settings import development
        assert development.DEBUG is True

    def test_cors_wildcard_enabled(self):
        from myproject.settings import development
        assert development.CORS_ALLOW_ALL_ORIGINS is True

    def test_debug_toolbar_installed(self):
        from myproject.settings import development
        assert "debug_toolbar" in development.INSTALLED_APPS

    def test_console_email_backend(self):
        from myproject.settings import development
        assert development.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend"


class TestTestSettings:
    def test_debug_disabled(self):
        from myproject.settings import test
        assert test.DEBUG is False

    def test_throttling_disabled(self):
        from myproject.settings import test
        assert test.REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] == []

    def test_temporal_disabled(self):
        from myproject.settings import test
        assert test.DJANGO_TEMPORALIO == {}

    def test_locmem_cache(self):
        from myproject.settings import test
        assert test.CACHES["default"]["BACKEND"] == "django.core.cache.backends.locmem.LocMemCache"
