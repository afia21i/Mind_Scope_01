from django.contrib import admin
from .models import Screening, MoodEntry, ChatMessage, WellnessTip


@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ("user", "screening_type", "score", "severity", "date_taken")
    list_filter = ("screening_type", "severity", "date_taken")


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "mood", "date_logged")
    search_fields = ("user__username", "notes")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "response", "timestamp")
    search_fields = ("user__username", "message")


@admin.register(WellnessTip)
class WellnessTipAdmin(admin.ModelAdmin):
    list_display = ("title", "language")
    search_fields = ("title", "content")

