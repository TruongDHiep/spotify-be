from django.db import models
from apps.artists.models import Artist
from apps.albums.models import Album
from apps.genres.models import Genre

# Create your models here.
class Song(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=200)
    duration = models.DurationField()

    artist_owner = models.ForeignKey(
    'artists.Artist',
    on_delete=models.SET_NULL,
    null=True,
    related_name='owned_songs'
)
    
    artists = models.ManyToManyField(
    'artists.Artist',
    related_name='featured_songs',
    blank=True
)
    img = models.TextField(blank=True)
    file_upload = models.TextField(blank=True)
    description = models.TextField(blank=True)
    
    mv = models.TextField(blank=True)
    play_count = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

