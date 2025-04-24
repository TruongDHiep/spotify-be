from rest_framework import serializers
from .models import PlaylistSong

class PlaylistSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistSong
        fields = '__all__'
        read_only_fields = ['id']