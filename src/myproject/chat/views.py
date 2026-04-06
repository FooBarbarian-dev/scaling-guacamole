"""HTMX views for the chat interface."""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import ChatMessage, ChatSession


@login_required
def chat_session(request):
    """Render the chat page."""
    session, _ = ChatSession.objects.get_or_create(
        user=request.user,
        is_active=True,
        defaults={"title": "New Chat"},
    )
    messages = session.messages.all()
    return render(request, "chat/session.html", {
        "session": session,
        "messages": messages,
    })


@login_required
@require_POST
def send_message(request):
    """Handle HTMX message submission."""
    content = request.POST.get("message", "").strip()
    if not content:
        return HttpResponse("")

    session, _ = ChatSession.objects.get_or_create(
        user=request.user,
        is_active=True,
        defaults={"title": "New Chat"},
    )

    # Save user message
    user_msg = ChatMessage.objects.create(
        session=session,
        role="user",
        content=content,
    )

    # TODO: Integrate with Django AI Assistant for actual AI response
    ai_response = f"Echo: {content}"

    assistant_msg = ChatMessage.objects.create(
        session=session,
        role="assistant",
        content=ai_response,
    )

    # Return both messages as HTMX partial
    return render(request, "chat/partials/message.html", {
        "messages": [user_msg, assistant_msg],
    })
