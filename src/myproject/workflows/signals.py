"""Workflow signals — optionally trigger Temporal workflows on model events."""
import logging
import os

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _is_temporal_post_processing_enabled() -> bool:
    return os.environ.get("ENABLE_TEMPORAL_POST_PROCESSING", "False").lower() in ("true", "1", "yes")


@receiver(post_save, sender="chat.ChatMessage")
def trigger_post_processing(sender, instance, created, **kwargs):
    """Optionally trigger ProcessTaskWorkflow for async post-processing.

    Guarded by ENABLE_TEMPORAL_POST_PROCESSING env var (default False).
    """
    if not created or not _is_temporal_post_processing_enabled():
        return

    try:
        # TODO: Implement actual Temporal client call
        # from temporalio.client import Client
        # client = await Client.connect(os.environ.get("TEMPORALIO_HOST", "localhost:7233"))
        # await client.start_workflow(
        #     ProcessTaskWorkflow.run,
        #     args=[instance.session.user.id, instance.content],
        #     id=f"post-process-{instance.pk}",
        #     task_queue="main-task-queue",
        # )
        logger.info(f"Would trigger ProcessTaskWorkflow for ChatMessage {instance.pk}")
    except Exception:
        logger.exception(f"Failed to trigger workflow for ChatMessage {instance.pk}")
