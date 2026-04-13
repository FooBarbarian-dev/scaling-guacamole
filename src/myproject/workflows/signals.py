"""Workflow signals — trigger Temporal workflows on model events.

When ENABLE_TEMPORAL_POST_PROCESSING is True, every new ChatMessage
triggers ProcessChatMessageWorkflow via the Temporal server. The
workflow runs asynchronously in the temporal-worker process.
"""
import asyncio
import logging
import os

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _is_temporal_post_processing_enabled() -> bool:
    return os.environ.get("ENABLE_TEMPORAL_POST_PROCESSING", "False").lower() in ("true", "1", "yes")


def _submit_workflow(chat_message_id: int) -> None:
    """Submit ProcessChatMessageWorkflow to the Temporal server.

    Runs the async client call in a new event loop. This is safe to call
    from a synchronous Django signal handler.
    """
    async def _start():
        from django_temporalio.client import init_client
        client = await init_client()
        result = await client.execute_workflow(
            "ProcessChatMessageWorkflow",
            chat_message_id,
            id=f"process-chat-msg-{chat_message_id}",
            task_queue=os.environ.get("TEMPORALIO_TASK_QUEUE", "main-task-queue"),
        )
        logger.info(f"[Temporal] Workflow completed for ChatMessage {chat_message_id}: {result}")

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # We're inside an async context (e.g. ASGI) — schedule as a task
        loop.create_task(_start())
    else:
        # Sync context (e.g. WSGI / manage.py) — run in a new loop
        asyncio.run(_start())


@receiver(post_save, sender="chat.ChatMessage")
def trigger_post_processing(sender, instance, created, **kwargs):
    """Trigger ProcessChatMessageWorkflow when a new ChatMessage is saved.

    Guarded by ENABLE_TEMPORAL_POST_PROCESSING env var (default False).
    """
    if not created or not _is_temporal_post_processing_enabled():
        return

    try:
        _submit_workflow(instance.pk)
    except Exception:
        logger.exception(f"Failed to submit Temporal workflow for ChatMessage {instance.pk}")
