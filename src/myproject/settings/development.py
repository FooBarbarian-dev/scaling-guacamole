"""Development settings — DEBUG=True, relaxed security, dev tools."""
from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

# CORS — allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Django Debug Toolbar
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
INTERNAL_IPS = ["127.0.0.1", "0.0.0.0"]

# Console email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Serve static files via Django in development
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
