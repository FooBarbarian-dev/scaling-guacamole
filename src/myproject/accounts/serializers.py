"""DRF serializers for the accounts app."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "uuid", "username", "email", "created_at")
        read_only_fields = ("id", "uuid", "created_at")
