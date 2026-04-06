"""Factory Boy factories for chat models."""
import factory
from django.contrib.auth import get_user_model

from myproject.chat.models import ChatMessage, ChatSession

User = get_user_model()


class ChatSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatSession

    user = factory.LazyFunction(lambda: User.objects.create_user(
        username=factory.Faker("user_name").evaluate(None, None, {"locale": None}),
        password="testpass123",
    ))
    title = factory.Faker("sentence", nb_words=3)
    is_active = True


class ChatMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatMessage

    session = factory.SubFactory(ChatSessionFactory)
    role = "user"
    content = factory.Faker("paragraph")
