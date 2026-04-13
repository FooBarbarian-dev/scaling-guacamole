from django.contrib import admin

from .models import ChatMessage, ChatSession


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ("role", "content", "created_at")


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "user__username")
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("session", "role", "content_preview", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("content",)

    @admin.display(description="Content")
    def content_preview(self, obj):
        return obj.content[:100]
