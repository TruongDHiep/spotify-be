from django.db import models
from apps.users.models import User
from apps.songs.models import Song

class ListeningHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_histories')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='listened_by')
    listened_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-listened_at']

