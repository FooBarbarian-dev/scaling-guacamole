"""Custom middleware for request tracking and performance monitoring."""
import logging
import time
import uuid

logger = logging.getLogger(__name__)


class RequestIDMiddleware:
    """Attach a unique request ID to each request for tracing."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.request_id = request_id
        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        return response


class TimingMiddleware:
    """Log request processing time."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.monotonic()
        response = self.get_response(request)
        duration_ms = (time.monotonic() - start_time) * 1000
        logger.info(
            f"{request.method} {request.path} completed in {duration_ms:.1f}ms",
            extra={"request_id": getattr(request, "request_id", "none")},
        )
        return response
