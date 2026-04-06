"""Template context processors."""


def theme_preference(request):
    """Add theme preference to template context."""
    return {
        "theme": request.COOKIES.get("theme", "light"),
    }


def app_name(request):
    """Add application name to template context."""
    return {
        "app_name": "My Project",  # TODO: Replace with your project name
    }
