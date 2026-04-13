"""
Settings module for myproject.

Reads DJANGO_ENV environment variable to determine which settings module to load.
Defaults to 'development' if not set.
"""
import os

env = os.environ.get("DJANGO_ENV", "development")

if env == "production":
    from .production import *  # noqa: F401, F403
else:
    from .development import *  # noqa: F401, F403
