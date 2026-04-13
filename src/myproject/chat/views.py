"""HTMX views for the chat interface."""
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from django_ai_assistant.helpers import use_cases

from .models import ChatMessage, ChatSession

logger = logging.getLogger(__name__)

ASSISTANT_ID = "project-assistant"


def _create_session(user):
    """Create a new chat session with a linked AI assistant thread."""
    thread = use_cases.create_thread(
        name="Chat",
        assistant_id=ASSISTANT_ID,
        user=user,
    )
    return ChatSession.objects.create(
        user=user,
        title="New Chat",
        ai_thread=thread,
    )


def _ensure_thread(session, user):
    """Ensure a session has an AI thread, creating one if missing."""
    if session.ai_thread:
        return session
    thread = use_cases.create_thread(
        name="Chat",
        assistant_id=ASSISTANT_ID,
        user=user,
    )
    session.ai_thread = thread
    session.save(update_fields=["ai_thread"])
    return session


@login_required
def chat_session(request, session_id=None):
    """Render the chat page for a specific session or the most recent one."""
    sessions = ChatSession.objects.filter(user=request.user).order_by("-created_at")

    if session_id:
        session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
    elif sessions.exists():
        session = sessions.first()
    else:
        session = _create_session(request.user)
        return redirect("chat:session-detail", session_id=session.pk)

    session = _ensure_thread(session, request.user)
    chat_messages = session.messages.all()

    return render(request, "chat/session.html", {
        "session": session,
        "sessions": sessions,
        "chat_messages": chat_messages,
    })


@login_required
def new_session(request):
    """Create a new chat session and redirect to it."""
    # Mark all existing active sessions as inactive
    ChatSession.objects.filter(user=request.user, is_active=True).update(is_active=False)
    session = _create_session(request.user)
    return redirect("chat:session-detail", session_id=session.pk)


@login_required
@require_POST
def send_message(request, session_id):
    """Handle HTMX message submission — sends to Django AI Assistant."""
    content = request.POST.get("message", "").strip()
    if not content:
        return HttpResponse("")

    session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
    session = _ensure_thread(session, request.user)

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
