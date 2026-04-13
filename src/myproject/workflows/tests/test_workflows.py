"""Tests for Temporal workflow and activity definitions."""
from unittest.mock import AsyncMock, patch

import pytest

from myproject.workflows.activities import log_chat_message
from myproject.workflows.workflows import ProcessChatMessageWorkflow


class TestWorkflowDefinitions:
    def test_log_chat_message_activity_is_importable(self):
        assert callable(log_chat_message)

    def test_process_chat_message_workflow_is_importable(self):
        assert ProcessChatMessageWorkflow is not None

    def test_process_chat_message_workflow_has_run_method(self):
        assert hasattr(ProcessChatMessageWorkflow, "run")


@pytest.mark.django_db
class TestLogChatMessageActivity:
    @pytest.mark.asyncio
    async def test_logs_existing_message(self):
        from django.contrib.auth import get_user_model
        from myproject.chat.models import ChatMessage, ChatSession

        User = get_user_model()
        user = await User.objects.acreate(username="temporal_test", password="test")
        session = await ChatSession.objects.acreate(user=user, title="Test")
        msg = await ChatMessage.objects.acreate(
            session=session, role="user", content="Hello from Temporal test"
        )

        result = await log_chat_message(msg.pk)
        assert "temporal_test" in result
        assert str(msg.pk) in result

    @pytest.mark.asyncio
    async def test_handles_missing_message(self):
        result = await log_chat_message(999999)
        assert "not found" in result


class TestSignalGuard:
    def test_disabled_by_default(self):
        from myproject.workflows.signals import _is_temporal_post_processing_enabled
        assert not _is_temporal_post_processing_enabled()

    @patch.dict("os.environ", {"ENABLE_TEMPORAL_POST_PROCESSING": "true"})
    def test_enabled_when_env_set(self):
        from myproject.workflows.signals import _is_temporal_post_processing_enabled
        assert _is_temporal_post_processing_enabled()


@pytest.mark.django_db
class TestSignalTrigger:
    @patch("myproject.workflows.signals._submit_workflow")
    @patch.dict("os.environ", {"ENABLE_TEMPORAL_POST_PROCESSING": "true"})
    def test_signal_fires_on_new_chat_message(self, mock_submit):
        from django.contrib.auth import get_user_model
        from myproject.chat.models import ChatMessage, ChatSession

        User = get_user_model()
        user = User.objects.create_user(username="sig_test", password="test")
        session = ChatSession.objects.create(user=user, title="Test")
        msg = ChatMessage.objects.create(
            session=session, role="user", content="trigger test"
        )
        mock_submit.assert_called_once_with(msg.pk)

    @patch("myproject.workflows.signals._submit_workflow")
    def test_signal_does_not_fire_when_disabled(self, mock_submit):
        from django.contrib.auth import get_user_model
        from myproject.chat.models import ChatMessage, ChatSession

        User = get_user_model()
        user = User.objects.create_user(username="sig_test2", password="test")
        session = ChatSession.objects.create(user=user, title="Test")
        ChatMessage.objects.create(
            session=session, role="user", content="should not trigger"
        )
        mock_submit.assert_not_called()
