"""API views — chat endpoint and viewsets."""
import logging

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django_ai_assistant.helpers import use_cases

from myproject.chat.models import ChatMessage, ChatSession
from myproject.chat.views import ASSISTANT_ID, _create_session, _ensure_thread

from .serializers import ChatMessageInputSerializer, ChatMessageSerializer, ChatSessionSerializer

logger = logging.getLogger(__name__)


class ChatMessageView(APIView):
    """POST endpoint for sending chat messages via AI Assistant."""

    def post(self, request):
        serializer = ChatMessageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = ChatSession.objects.filter(user=request.user, is_active=True).first()
        if not session:
            session = _create_session(request.user)
        else:
            session = _ensure_thread(session, request.user)

        # Save the user message
        user_message = ChatMessage.objects.create(
            session=session,
            role="user",
            content=serializer.validated_data["message"],
        )

        # Send to Django AI Assistant
        try:
            result = use_cases.create_message(
                assistant_id=ASSISTANT_ID,
                thread=session.ai_thread,
                user=request.user,
                content=serializer.validated_data["message"],
            )
            ai_response = result.get("output", "")
            if not ai_response:
                ai_response = "(No response from assistant)"
        except Exception:
            logger.exception("AI Assistant error")
            ai_response = "Sorry, something went wrong. Please try again."

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
