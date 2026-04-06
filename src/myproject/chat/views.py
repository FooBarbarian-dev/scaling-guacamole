"""HTMX views for the chat interface."""
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from django_ai_assistant.helpers import use_cases

from .models import ChatMessage, ChatSession

logger = logging.getLogger(__name__)

ASSISTANT_ID = "project-assistant"


def _get_or_create_session(user):
    """Get the active chat session for a user, creating one with an AI thread if needed."""
    session = ChatSession.objects.filter(user=user, is_active=True).first()
    if session and session.ai_thread:
        return session

    # Create a new AI assistant thread
    thread = use_cases.create_thread(
        name="Chat",
        assistant_id=ASSISTANT_ID,
        user=user,
    )

    if session and not session.ai_thread:
        session.ai_thread = thread
        session.save(update_fields=["ai_thread"])
        return session

    return ChatSession.objects.create(
        user=user,
        title="New Chat",
        ai_thread=thread,
    )


@login_required
def chat_session(request):
    """Render the chat page."""
    session = _get_or_create_session(request.user)
    messages = session.messages.all()
    return render(request, "chat/session.html", {
        "session": session,
        "messages": messages,
    })


@login_required
@require_POST
def send_message(request):
    """Handle HTMX message submission — sends to Django AI Assistant."""
    content = request.POST.get("message", "").strip()
    if not content:
        return HttpResponse("")

    session = _get_or_create_session(request.user)

    # Save user message to our local model
    user_msg = ChatMessage.objects.create(
        session=session,
        role="user",
        content=content,
    )

    # Send to Django AI Assistant and get the response
    try:
        result = use_cases.create_message(
            assistant_id=ASSISTANT_ID,
            thread=session.ai_thread,
            user=request.user,
            content=content,
        )
        ai_response = result.get("output", "")
        if not ai_response:
            ai_response = "(No response from assistant)"
    except Exception:
        logger.exception("AI Assistant error")
        ai_response = "Sorry, something went wrong. Please try again."

    assistant_msg = ChatMessage.objects.create(
        session=session,
        role="assistant",
        content=ai_response,
    )

    # Return both messages as HTMX partial
    return render(request, "chat/partials/message.html", {
        "messages": [user_msg, assistant_msg],
    })
