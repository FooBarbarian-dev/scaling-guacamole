"""Chat models for storing conversation sessions and messages."""
from django.conf import settings
from django.db import models

from myproject.core.models import TimeStampedModel


class ChatSession(TimeStampedModel):
    """A chat conversation session belonging to a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions",
    )
    title = models.CharField(max_length=255, default="New Chat")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "chat session"
        verbose_name_plural = "chat sessions"

    def __str__(self) -> str:
        return f"{self.title} ({self.user.username})"


class ChatMessage(TimeStampedModel):
    """A single message within a chat session."""

    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    ]

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()

    class Meta:
        ordering = ["created_at"]
        verbose_name = "chat message"
        verbose_name_plural = "chat messages"

    def __str__(self) -> str:
        return f"[{self.role}] {self.content[:50]}"
