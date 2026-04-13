"""Production settings — security hardened, proper static/media handling."""
from .base import *  # noqa: F401, F403

DEBUG = False

ALLOWED_HOSTS = env("ALLOWED_HOSTS")  # noqa: F405

# Security
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# WhiteNoise for static files (fallback; nginx is primary)
MIDDLEWARE.insert(2, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Static files
STATIC_ROOT = Path("/app/staticfiles")  # noqa: F405

# CORS — explicit origins only in production
CORS_ALLOW_ALL_ORIGINS = False

# Database connection pooling
DATABASES["default"]["CONN_MAX_AGE"] = 600  # noqa: F405
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True  # noqa: F405

# Cache backend: Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL"),  # noqa: F405
    }
}
