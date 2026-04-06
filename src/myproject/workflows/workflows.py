"""Temporal workflows — auto-discovered by django-temporalio from files matching *workflows*.py."""
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from .activities import send_notification

from django_temporalio.registry import queue_workflows


@queue_workflows.register("main-task-queue")
@workflow.defn
class ProcessTaskWorkflow:
    """Example workflow that sends a notification."""

    @workflow.run
    async def run(self, user_id: int, message: str) -> str:
        return await workflow.execute_activity(
            send_notification,
            args=[user_id, message],
            schedule_to_close_timeout=timedelta(seconds=30),
        )
