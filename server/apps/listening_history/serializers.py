from rest_framework import serializers
from .models import ListeningHistory
from apps.songs.serializers import SongSerializer

class ListeningHistorySerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    
    class Meta:
        model = ListeningHistory
        fields = ['id', 'user', 'song', 'listened_at']
        read_only_fields = ['user', 'listened_at']
