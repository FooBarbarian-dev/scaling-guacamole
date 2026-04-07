from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_session, name="session"),
    path("new/", views.new_session, name="new-session"),
    path("<int:session_id>/", views.chat_session, name="session-detail"),
    path("<int:session_id>/send/", views.send_message, name="send-message"),
]
