"""
Base settings shared across all environments.

All configuration is read from environment variables via django-environ
with sane defaults for development.
"""
from pathlib import Path

import environ

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1", "0.0.0.0"]),
    CORS_ALLOWED_ORIGINS=(list, ["http://localhost:3000", "http://localhost:8000"]),
    CORS_ALLOW_CREDENTIALS=(bool, True),
    AI_ASSISTANT_OPENAI_API_BASE=(str, "https://api.openai.com/v1"),
    AI_ASSISTANT_OPENAI_API_KEY=(str, ""),  # TODO: Set your API key
    AI_ASSISTANT_MODEL=(str, "gpt-4o"),  # TODO: Set your model name
    TEMPORALIO_HOST=(str, "localhost:7233"),
    TEMPORALIO_TASK_QUEUE=(str, "main-task-queue"),
    ENABLE_TEMPORAL_POST_PROCESSING=(bool, False),
    REDIS_URL=(str, "redis://localhost:6379/0"),
)

# Read .env file if it exists
environ.Env.read_env(env_file=".env", overrides=False)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY", default="django-insecure-change-me-in-production")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "django_extensions",
    "rest_framework",
    "drf_spectacular",
    "django_htmx",
    "corsheaders",
    "django_ai_assistant",
    "django_temporalio.apps.DjangoTemporalioConfig",
    # Project apps
    "myproject.core",
    "myproject.accounts",
    "myproject.api",
    "myproject.chat",
    "myproject.workflows",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "myproject.core.middleware.RequestIDMiddleware",
    "myproject.core.middleware.TimingMiddleware",
]

ROOT_URLCONF = "myproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "myproject.core.context_processors.theme_preference",
                "myproject.core.context_processors.app_name",
                "myproject.core.context_processors.django_messages",
            ],
        },
    },
]

WSGI_APPLICATION = "myproject.wsgi.application"

# Database
DATABASES = {
    "default": env.db("DATABASE_URL", default="postgres://myproject:myproject@localhost:5432/myproject"),
}

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserCommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR.parent.parent / "staticfiles"

# Media files
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.parent.parent / "mediafiles"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login URLs
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/chat/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "myproject.accounts.authentication.APIKeyAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "myproject.api.throttling.AnonBurstThrottle",
        "myproject.api.throttling.UserBurstThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/min",
        "user": "60/min",
        "burst": "120/min",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# drf-spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "My Project API",  # TODO: Replace with your API title
    "DESCRIPTION": "API documentation for My Project",  # TODO: Replace with your API description
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# CORS
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = env("CORS_ALLOW_CREDENTIALS")

# AI Assistant
OPENAI_API_KEY = env("AI_ASSISTANT_OPENAI_API_KEY")

# django-temporalio
from temporalio.worker import WorkerConfig  # noqa: E402

DJANGO_TEMPORALIO = {
    "CLIENT_CONFIG": {
        "target_host": env("TEMPORALIO_HOST"),
    },
    "BASE_MODULE": "myproject.workflows",
    "WORKER_CONFIGS": {
        "main": WorkerConfig(
            task_queue=env("TEMPORALIO_TASK_QUEUE"),
        ),
    },
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} [request_id:{request_id}] {message}",
            "style": "{",
            "defaults": {"request_id": "none"},
        },
        "simple": {
            "format": "[{asctime}] {levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "myproject": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
