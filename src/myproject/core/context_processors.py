"""Template context processors."""
from django.contrib.messages import get_messages


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


def django_messages(request):
    """Expose Django messages framework under a non-colliding name.

    The default 'messages' context variable collides with any view that
    also passes 'messages' in its context (e.g. chat messages).
    """
    return {
        "django_messages": get_messages(request),
    }
