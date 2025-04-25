from rest_framework import serializers
from .models import Album
from apps.artists.models import Artist
from apps.artists.serializers import ArtistSerializer

class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)  # Hiển thị thông tin chi tiết của artist (chỉ đọc)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), source='artist', write_only=True  # Gửi ID của artist khi tạo/cập nhật album
    )

    class Meta:
        model = Album
        fields = ['id', 'artist', 'artist_id', 'title', 'avatar', 'release_date', 'description']
        read_only_fields = ['id']