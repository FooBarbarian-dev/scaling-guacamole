"""Verify all app modules import cleanly without errors."""
import importlib

import pytest

APP_MODULES = [
    "myproject.core",
    "myproject.core.apps",
    "myproject.core.models",
    "myproject.core.middleware",
    "myproject.core.context_processors",
    "myproject.accounts",
    "myproject.accounts.apps",
    "myproject.accounts.models",
    "myproject.accounts.views",
    "myproject.accounts.forms",
    "myproject.accounts.serializers",
    "myproject.accounts.permissions",
    "myproject.accounts.authentication",
    "myproject.accounts.signals",
    "myproject.api",
    "myproject.api.apps",
    "myproject.api.views",
    "myproject.api.serializers",
    "myproject.api.throttling",
    "myproject.chat",
    "myproject.chat.apps",
    "myproject.chat.models",
    "myproject.chat.views",
    "myproject.workflows",
    "myproject.workflows.apps",
    "myproject.health",
]


@pytest.mark.parametrize("module_path", APP_MODULES)
def test_import(module_path):
    """Each app module should import without raising ImportError."""
    mod = importlib.import_module(module_path)
    assert mod is not None
