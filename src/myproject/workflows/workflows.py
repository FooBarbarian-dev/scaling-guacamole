"""Temporal workflows — auto-discovered by django-temporalio from files matching *workflows*.py.

Workflows are deterministic orchestrators. They should NOT import Django
directly — all Django/IO work goes in activities. Use
`workflow.unsafe.imports_passed_through()` to import activity references.
"""
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from .activities import log_chat_message

from django_temporalio.registry import queue_workflows


@queue_workflows.register("main-task-queue")
@workflow.defn
class ProcessChatMessageWorkflow:
    """Workflow triggered when a new chat message is saved.

    Currently runs a single activity (log_chat_message) but is structured
    so you can chain additional steps: moderation, summarisation, etc.
    """

    @workflow.run
    async def run(self, chat_message_id: int) -> str:
        result = await workflow.execute_activity(
            log_chat_message,
            args=[chat_message_id],
            schedule_to_close_timeout=timedelta(seconds=30),
        )
        workflow.logger.info(f"ProcessChatMessageWorkflow completed: {result}")
        return result
