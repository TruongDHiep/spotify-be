from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import Playlist_SongService
from .models import Playlist, PlaylistSong
from apps.songs.models import Song
from django.shortcuts import get_object_or_404
from rest_framework import status



# Create your views here.
class PlaylistSongsListView(APIView):
    def get(self, request, playlist_id):
        """Get all songs in a playlist"""
        from apps.songs.serializers import SongSerializer
        
        songs = Playlist_SongService.get_songs_by_playlist(playlist_id)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
    

    def post(self, request, playlist_id, song_id):
        """Thêm bài hát vào playlist"""
        try:
            playlist_song = Playlist_SongService.add_song_to_playlist(playlist_id, song_id)
            return Response(
                {"message": "Song added to playlist successfully"},
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, playlist_id, song_id):
        """Xóa một bài hát khỏi playlist"""
        try:
            result = Playlist_SongService.remove_song_from_playlist(playlist_id, song_id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)