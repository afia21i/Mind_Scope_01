from django.db import models
from django.contrib.auth.models import User


class Screening(models.Model):
    SCREENING_TYPES = [
        ("PHQ9", "Depression (PHQ-9)"),
        ("GAD7", "Anxiety (GAD-7)"),
        ("PSS10", "Stress (PSS-10)"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="screenings")
    screening_type = models.CharField(max_length=10, choices=SCREENING_TYPES)
    score = models.IntegerField()
    severity = models.CharField(max_length=50)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.screening_type} ({self.score})"


class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ("😊", "Happy"),
        ("😢", "Sad"),
        ("😡", "Angry"),
        ("😌", "Calm"),
        ("😴", "Tired"),
        ("😟", "Anxious"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mood_entries")
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    influencers = models.TextField(blank=True, help_text="Factors affecting mood")
    notes = models.TextField(blank=True, null=True)
    date_logged = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} ({self.date_logged.date()})"


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_messages")
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.user.username} at {self.timestamp}"


class WellnessTip(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    language = models.CharField(max_length=20, default="English")

    def __str__(self):
        return self.title
