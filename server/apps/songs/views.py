from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer
from .services import SongService
import json

# Create your views here.
class SongDetailView(APIView):
    def get(self, request, song_id):
        """song by ID"""
        song = SongService.get_song_by_id(song_id)
        serializer = SongSerializer(song)
        return Response(serializer.data)


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
        file = request.FILES.get('file')
        img_upload = request.FILES.get('img_upload')
        video_upload = request.FILES.get('video_upload')
        # Gọi service để tạo bài hát
        song = SongService.create_song(validated_data, file, img_upload, video_upload)
        # Trả về kết quả
        response_serializer = SongSerializer(song)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, song_id):
        """Delete song by id"""
        try:
            song = SongService.delete_song(song_id)
            serializer = SongSerializer(song)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Song.DoesNotExist:
            return Response(
                {"error": "Song not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
    def put(self, request, song_id):
        try:
            # Parse JSON từ trường "data"
            data = json.loads(request.data.get('data', '{}'))
            
            # Tách artists ra khỏi data chính
            artists_data = data.pop('artists', None)
            
            # Validate data bằng serializer 
            serializer = SongSerializer(data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data.copy()

            # Lấy files từ request nếu có
            file_upload = request.FILES.get('file')
            img_upload = request.FILES.get('img_upload')
            mv_upload = request.FILES.get('mv')

            # Gọi service để update bài hát với artists_data riêng
            song = SongService.update_song(
                song_id=song_id,
                data=validated_data,
                artists_data=artists_data,  # Thêm artists_data
                file_upload=file_upload,
                img_upload=img_upload,
                mv_upload=mv_upload
            )
            
            # Trả về kết quả
            response_serializer = SongSerializer(song)
            return Response(response_serializer.data)
        except Song.DoesNotExist:
            return Response(
                {"error": "Song not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class TopSongsView(APIView):
    def get(self, request):
        """Get top 10 songs by play count"""
        songs = SongService.get_top_songs()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

class SongPlayCountView(APIView):
    def put(self, request, song_id):
        """Get play count of a song by id"""
        try:
            song = SongService.update_play_count(song_id)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist:
            return Response(
                {"error": "Song not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class SongPaginationView(APIView):
    def get(self, request, page):
        """Get songs by page"""
        page_size = request.query_params.get('page_size', 8)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 8
            
        songs = SongService.get_song_bypage(page, page_size)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

class SongsByAlbumView(APIView):
    def get(self, request, album_id):
        """Lấy tất cả bài hát theo album ID"""
        songs = SongService.get_songs_by_album(album_id)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)