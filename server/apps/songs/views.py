from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer
from .services import SongService
import json


# Create your views here.
class SongListView(APIView):
    def get(self, request):
        """Get all song"""
        songs = SongService.get_songs()
        serializers = SongSerializer(songs,many = True)
        return Response(serializers.data)

    def post(self, request):
        """Create song from multipart with JSON + files"""
        # Parse JSON từ trường "data"
        try:
            data = json.loads(request.data.get('data', '{}'))
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON in 'data'"}, status=400)

        # Validate data bằng serializer
        serializer = SongSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data.copy()

        # Lấy file từ request.FILES
        file_upload = request.FILES.get('file_upload')
        img_upload = request.FILES.get('img_upload')
        video_upload = request.FILES.get('video_upload')

        # Gọi service để tạo bài hát
        song = SongService.create_song(validated_data, file_upload, img_upload, video_upload)

        # Trả về kết quả
        response_serializer = SongSerializer(song)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
