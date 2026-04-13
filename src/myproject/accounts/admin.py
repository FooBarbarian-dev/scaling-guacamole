from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import APIKey, User


class APIKeyInline(admin.TabularInline):
    model = APIKey
    extra = 0
    readonly_fields = ("prefix", "created_at", "last_used_at")
    fields = ("prefix", "name", "revoked", "created_at", "last_used_at")
    # Never show the hashed key in admin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "uuid", "is_staff", "created_at")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "uuid")
    inlines = [APIKeyInline]


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ("prefix", "name", "user", "revoked", "created_at", "last_used_at")
    list_filter = ("revoked", "created_at")
    search_fields = ("prefix", "name", "user__username")
    readonly_fields = ("prefix", "hashed_key", "created_at", "last_used_at")
    # The hashed_key is shown as readonly but is NOT the raw key
