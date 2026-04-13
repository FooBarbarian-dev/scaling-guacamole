"""Simple health check endpoint for load balancers and Docker HEALTHCHECK."""
from django.http import JsonResponse


def health_check(request):
    """Return 200 OK if the application is running."""
    return JsonResponse({"status": "ok"})
