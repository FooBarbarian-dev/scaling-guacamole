"""API views — chat endpoint and viewsets."""
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from myproject.chat.models import ChatMessage, ChatSession

from .serializers import ChatMessageInputSerializer, ChatMessageSerializer, ChatSessionSerializer


class ChatMessageView(APIView):
    """POST endpoint for sending chat messages."""

    def post(self, request):
        serializer = ChatMessageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get or create a chat session for the user
        session, _ = ChatSession.objects.get_or_create(
            user=request.user,
            is_active=True,
            defaults={"title": "New Chat"},
        )

        # Save the user message
        user_message = ChatMessage.objects.create(
            session=session,
            role="user",
            content=serializer.validated_data["message"],
        )

        # TODO: Integrate with Django AI Assistant for actual AI response
        ai_response = f"Echo: {user_message.content}"

        assistant_message = ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=ai_response,
        )

        return Response(
            ChatMessageSerializer(assistant_message).data,
            status=status.HTTP_200_OK,
        )


class ChatSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve user's chat sessions."""

    serializer_class = ChatSessionSerializer

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
