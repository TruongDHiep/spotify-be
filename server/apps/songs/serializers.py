from rest_framework import serializers
from .models import Song
from apps.songs.services import SongService
class SongSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=False)
    img_upload = serializers.FileField(write_only=True, required=False)
    video_upload = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Song
        fields = '__all__'  # tất cả field trong model
        # KHÔNG đặt read_only_fields với file_upload, img, mv
