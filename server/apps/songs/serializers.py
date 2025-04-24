from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    file_upload = serializers.FileField(write_only=True, required=False)
    img_upload = serializers.FileField(write_only=True, required=False)
    video_upload = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Song
        fields = '__all__'  # tất cả field trong model
        read_only_fields = ['file_upload', 'img', 'mv']  # Không cho phép user set trực tiếp

    """
    Tùy chỉnh output trả về cho client nếu cần
        def to_representation(self, instance):
        
            rep = super().to_representation(instance)
            return rep
    """

