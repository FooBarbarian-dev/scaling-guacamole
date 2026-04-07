"""
Test settings — used exclusively by pytest.

Inherits from base settings but stubs out services that shouldn't be
contacted during tests (Temporal, Redis, AI Assistant). The database
is configured at runtime by conftest.py using testcontainers.
"""
from .base import *  # noqa: F401, F403

# ──────────────────────────────────────────────────────────────────────
# Safety: refuse to boot if someone accidentally points tests at prod
# ──────────────────────────────────────────────────────────────────────
_FORBIDDEN_DB_HOSTS = {"prod", "production", "rds.amazonaws.com", "cloud.google.com"}

_db_host = DATABASES["default"].get("HOST", "")  # noqa: F405
for _fragment in _FORBIDDEN_DB_HOSTS:
    if _fragment in _db_host:
        raise RuntimeError(
            f"Refusing to run tests: DATABASE_URL appears to point at a "
            f"production host ({_db_host!r}). Set DATABASE_URL to a local or "
            f"testcontainer database."
        )

# ──────────────────────────────────────────────────────────────────────
# Core overrides
# ──────────────────────────────────────────────────────────────────────
DEBUG = False
SECRET_KEY = "test-secret-key-not-for-production"  # noqa: S105

# Use a fast password hasher in tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable throttling in tests
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []  # noqa: F405

# ──────────────────────────────────────────────────────────────────────
# Stub external services — tests should not depend on live infra
# ──────────────────────────────────────────────────────────────────────

# Temporal: disable worker configs so django-temporalio doesn't try to connect
DJANGO_TEMPORALIO = {}  # noqa: F405

# AI Assistant: no real LLM calls (tests mock use_cases)
OPENAI_API_KEY = "test-key-not-real"  # noqa: F405

# Email: in-memory backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Cache: local memory instead of Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# ──────────────────────────────────────────────────────────────────────
# Database is set at runtime by conftest.py via testcontainers.
# If conftest hasn't injected a URL yet (e.g. running outside pytest),
# fall back to sqlite for simple smoke checks.
# ──────────────────────────────────────────────────────────────────────
import os  # noqa: E402

if os.environ.get("TEST_DATABASE_URL"):
    import environ  # noqa: E402
    _env = environ.Env()
    DATABASES = {  # noqa: F405
        "default": _env.db_url_config(os.environ["TEST_DATABASE_URL"]),
    }
