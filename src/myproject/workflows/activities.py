"""Temporal activities — auto-discovered by django-temporalio from files matching *activities*.py.

Activities run inside the Temporal worker process. They have full access to
Django's ORM, logging, and anything else — they're just regular async Python
functions executed by the worker.
"""
import logging

from temporalio import activity

from django_temporalio.registry import queue_activities

logger = logging.getLogger(__name__)


@queue_activities.register("main-task-queue")
@activity.defn
async def log_chat_message(chat_message_id: int) -> str:
    """Log details about a chat message for post-processing.

    This demonstrates a real Temporal activity that:
    1. Receives a ChatMessage PK from the workflow
    2. Loads the object from the Django ORM
    3. Does work (here: logging — replace with moderation, analytics, etc.)
    4. Returns a result string
    """
    from myproject.chat.models import ChatMessage

    try:
        msg = await ChatMessage.objects.select_related("session", "session__user").aget(pk=chat_message_id)
    except ChatMessage.DoesNotExist:
        logger.warning(f"ChatMessage {chat_message_id} not found — may have been deleted")
        return f"ChatMessage {chat_message_id} not found"

    username = msg.session.user.username
    role = msg.role
    preview = msg.content[:80]

    logger.info(
        f"[Temporal] Processed ChatMessage {msg.pk}: "
        f"user={username}, role={role}, content={preview!r}"
    )

    return f"Processed message {msg.pk} from {username} ({role})"
