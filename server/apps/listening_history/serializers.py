from rest_framework import serializers
from .models import ListeningHistory
from apps.songs.serializers import SongSerializer
from apps.songs.models import Song

class ListeningHistorySerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)  # Để hiển thị thông tin bài hát khi GET
    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        source='song',
        write_only=True  # Chỉ dùng để nhận ID khi POST
    )

    class Meta:
        model = ListeningHistory
        fields = ['song', 'song_id']

    def to_representation(self, instance):
        # Trả về trực tiếp thông tin của bài hát khi GET
        return SongSerializer(instance.song).data

    