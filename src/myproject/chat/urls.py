from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_session, name="session"),
    path("send/", views.send_message, name="send-message"),
]
