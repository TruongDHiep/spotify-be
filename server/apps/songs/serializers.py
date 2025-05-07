from rest_framework import serializers
from .models import Song
from apps.songs.services import SongService
from apps.albums.serializers import AlbumSerializer
from apps.albums.models import Album
from apps.artists.models import Artist
from apps.artists.serializers import ArtistSerializer

class SongSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=False)
    img_upload = serializers.FileField(write_only=True, required=False)
    video_upload = serializers.FileField(write_only=True, required=False)
    album = AlbumSerializer(read_only=True)  
    album_id = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(), source='album', write_only=True
    )
    artist = ArtistSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), source='artist', write_only=True
    )
    

    class Meta:
        model = Song
        fields = '__all__'  # tất cả field trong model
        # KHÔNG đặt read_only_fields với file_upload, img, mv
