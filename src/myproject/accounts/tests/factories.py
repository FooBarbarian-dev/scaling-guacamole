"""Factory Boy factories for accounts models."""
import factory
from django.contrib.auth import get_user_model

from myproject.accounts.models import APIKey

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")


class APIKeyFactory(factory.Factory):
    """Factory that creates API keys via the create_key classmethod.

    Usage: raw_key, api_key = APIKeyFactory.create(user=user, name="test")
    """

    class Meta:
        model = APIKey
        exclude = ["user", "name"]

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Test Key {n}")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = kwargs.pop("user")
        name = kwargs.pop("name", "Test Key")
        return APIKey.create_key(user=user, name=name)
