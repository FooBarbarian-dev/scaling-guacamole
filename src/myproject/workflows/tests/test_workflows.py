"""Tests for Temporal workflow and activity definitions."""
import pytest

from myproject.workflows.activities import send_notification
from myproject.workflows.workflows import ProcessTaskWorkflow


class TestWorkflowDefinitions:
    def test_send_notification_activity_is_importable(self):
        assert callable(send_notification)

    def test_process_task_workflow_is_importable(self):
        assert ProcessTaskWorkflow is not None

    def test_process_task_workflow_has_run_method(self):
        assert hasattr(ProcessTaskWorkflow, "run")

    @pytest.mark.asyncio
    async def test_send_notification_returns_string(self):
        result = await send_notification(1, "test message")
        assert isinstance(result, str)
        assert "user 1" in result
