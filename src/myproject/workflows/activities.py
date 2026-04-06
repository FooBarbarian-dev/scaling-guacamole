"""Temporal activities — auto-discovered by django-temporalio from files matching *activities*.py."""
from temporalio import activity

from django_temporalio.registry import queue_activities


@queue_activities.register("main-task-queue")
@activity.defn
async def send_notification(user_id: int, message: str) -> str:
    """Send a notification to a user. TODO: implement actual sending."""
    # TODO: Replace with real notification logic
    return f"Notification sent to user {user_id}: {message}"
