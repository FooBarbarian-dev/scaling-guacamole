"""API serializers for chat messages and sessions."""
from rest_framework import serializers

from myproject.chat.models import ChatMessage, ChatSession


class ChatMessageInputSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=4096)


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ("id", "role", "content", "created_at")
        read_only_fields = ("id", "role", "content", "created_at")


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ("id", "title", "is_active", "created_at", "messages")
        read_only_fields = fields
