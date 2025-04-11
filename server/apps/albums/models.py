from django.db import models
from apps.artists.models import Artist

class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255)
    avatar = models.TextField()
    release_date = models.DateField()
    description = models.TextField(blank=True)
