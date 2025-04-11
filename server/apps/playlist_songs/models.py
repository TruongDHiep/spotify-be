from django.db import models
from apps.playlists.models import Playlist
from apps.songs.models import Song

# Create your models here.
class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)