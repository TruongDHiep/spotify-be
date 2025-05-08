from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import Playlist_SongService
from .models import Playlist, PlaylistSong
from apps.songs.models import Song
from django.shortcuts import get_object_or_404
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


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

class RemoveSongFromPlaylistView(APIView):
    def delete(self, request, playlist_id, song_id):
        """Xóa một bài hát khỏi playlist"""
        try:
            result = Playlist_SongService.remove_song_from_playlist(playlist_id, song_id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class PlaylistSongsAddMultipleView(APIView):
    def post(self, request):
        playlist_id = request.data.get('playlist_id')
        song_ids = request.data.get('song_ids', [])

        if not isinstance(song_ids, list) or not song_ids:
            return Response({"error": "song_ids must be a non-empty list"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            added_songs = Playlist_SongService.add_multiple_songs_to_playlist(playlist_id, song_ids)
            logger.info(f"Successfully added {len(added_songs)} songs to playlist {playlist_id}.")
            return Response({'added': len(added_songs)}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error adding songs to playlist: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PlaylistSongsListViewAdmin(APIView):

    def get(self, request, playlist_id):
        from apps.songs.serializers import SongSerializer
        songs = Playlist_SongService.get_songs_by_playlist(playlist_id)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def post(self, request, playlist_id, song_id):
        try:
            playlist_song = Playlist_SongService.add_song_to_playlist_admin(playlist_id, song_id)
            return Response(
                {"message": "Song added to playlist successfully"},
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, playlist_id, song_id):
        try:
            result = Playlist_SongService.remove_song_from_playlist(playlist_id, song_id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



    
